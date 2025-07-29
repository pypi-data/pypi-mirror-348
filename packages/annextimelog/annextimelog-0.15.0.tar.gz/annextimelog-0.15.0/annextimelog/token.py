from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import re
import inspect
import itertools
import warnings
import functools
import shlex
import logging
from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import (
    cast,
    Optional,
    Set,
    Dict,
    Union,
    List,
    Tuple,
    Iterator,
    ClassVar,
    FrozenSet,
)

# internal modules
from annextimelog.datetime import datetime, datetime as dt, timedelta, timedelta as td
from annextimelog.log import stderr


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Token(ABC):
    string: str = field(compare=False, default="", kw_only=True)
    is_condition: Optional[bool] = field(default=None, kw_only=True)

    @property
    def pretty(self) -> str:
        return str(self)

    @property
    def roundtrip(self) -> Union[Token | None]:
        for f in (
            lambda: type(self).from_str(str(self)),
            lambda: Token.from_str(str(self)),
        ):
            if t := f():
                return t
        return None

    @classmethod
    def recursive_subclasses(cls):
        yield cls
        for subcls in cls.__subclasses__():
            yield from subcls.recursive_subclasses()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Token, None]:
        """
        Recurse into subclasses and try their from_str() constructors.
        This exact method is inherited if it'string not overwritten (classmethods can't be abstractmethods...)
        """
        for subcls in cls.__subclasses__():
            if from_str := getattr(subcls, "from_str", None):
                try:
                    if token := from_str(string, **kwargs):
                        return token
                except Exception as e:
                    logger.error(
                        f"Calling {subcls.__name__}.from_str({string!r}) didn't work: {e.__class__.__name__} {e}"
                    )
        if cls is Token or str(cls) == str(Token):  # dirty hack: only in base class
            # fall back to just setting a tag
            return AddToField(
                string=string, field="tag", values=frozenset([string]), **kwargs
            )
        return None

    @staticmethod
    def join(tokens: Sequence[Token]) -> str:
        return shlex.join(t.string for t in tokens)

    @staticmethod
    def jointypes(tokens: Sequence[Token]) -> str:
        return "·".join(t.__class__.__name__ for t in tokens)

    @classmethod
    def joinpretty(cls, tokens: Sequence[Token]) -> str:
        return f"{cls.join(tokens)!r} [{cls.jointypes(tokens)}]"

    @classmethod
    def sort_into(
        cls, tokens: Sequence[Token], *categories: type[Token]
    ) -> List[List[Token]]:
        parts = [cast(List[Token], []) for c in categories]
        unhandled: List[Token] = []
        for token in tokens:
            nexttoken = False
            for i, category in enumerate(categories):
                if isinstance(token, category):
                    parts[i].append(token)
                    nexttoken = True
                    break
            if nexttoken:
                continue
            unhandled.append(token)
        return parts + [unhandled]

    @classmethod
    def split_by_trigger(
        cls,
        tokens: Sequence[Token],
        *triggers: type[Token],
        prohibited: Optional[Set[type[Token]]] = None,
        allow_repeat=False,
    ) -> List[List[Token]]:
        prohibited = prohibited or set()
        triggerparts = [cast(List[Token], []) for trigger in triggers]
        unhandled: List[Token] = []
        next_is = None
        found_triggers: Dict[int, Set[Token]] = dict()
        for token in tokens:
            if any(isinstance(token, t) for t in prohibited):
                raise ValueError(
                    f"in this context (splitting by {'/'.join(t.__name__ for t in triggers)}), "
                    f"{token.string!r} is prohibited"
                )
            is_trigger = False
            for i, trigger in enumerate(triggers):
                if isinstance(token, trigger):
                    already_had = ", ".join(
                        f"{t.string!r}" for t in found_triggers.get(i, set())
                    )
                    if next_is == i:
                        logger.info(
                            f"Superfluous {trigger.__name__} {token.string!r} "
                            f"(there was already {already_had})"
                        )
                    elif not allow_repeat and i in found_triggers:
                        raise ValueError(
                            f"There was already a {trigger.__name__} like {token.string!r} ({already_had}), repetition is not allowed"
                        )
                    next_is = i
                    is_trigger = True
                    if i not in found_triggers:
                        found_triggers[i] = set()
                    found_triggers[i].add(token)
                    break
            if is_trigger:  # don't include the triggers
                continue
            if next_is is None:
                unhandled.append(token)
            else:
                triggerparts[next_is].append(token)
        return triggerparts + [unhandled]

    @classmethod
    def reduce(
        cls,
        tokens: Sequence[Union[Token | None]],
        config: Optional[Dict[str, str]] = None,
        to: Optional[Sequence[type[Token]]] = None,
        **kwargs,
    ) -> Iterator[Token]:
        """
        Given a sequence of tokens, reduce it down by iteratively/recursively
        translate parts of it and dropping irrelevant elements.

        Args:
            tokens: the tokens
            config: the annextimelog git config dict
            **kwargs: further target attributes for Tokens, e.g. is_condition=...

        Steps:
            - sort into conditions and actions, recurse into those
            - sort into time-related tokens and the rest
            - recurse into time-related tokens to reduce into a single TimeFrame
        """
        config = config or dict()
        conf = dict(config=config)
        is_condition = kwargs.get("is_condition", None)
        cond = dict(is_condition=is_condition)
        now = dt.now().replace(microsecond=0)
        wss = dict(
            weekstartssunday=config.get(
                "annextimelog.weekstartssunday", "false"
            ).lower()
            == "true"
        )

        ### Preparation: consume all tokens into list and irrelevant ones ###
        tokens_: List[Token] = []
        for token in tokens:
            match token:
                case None | Noop():
                    logger.debug(f"Ignoring token {token!r}")
                case _:
                    tokens_.append(token)
        tokens = tokens_
        tokenstr = Token.join(tokens)
        ss = dict(string=(s := tokenstr), **kwargs)

        if not tokens:
            logger.debug(f"No tokens left, we're done.")
            yield from tokens
            return

        if logger.getEffectiveLevel() < logging.DEBUG:
            frame = inspect.currentframe()
            recursion_level = (
                len(
                    [f for f in inspect.getouterframes(frame) if f.function == "reduce"]
                )
                - 1
            )
            logger.debug(
                f"Attempting reduce({is_condition=},{to=}) ({recursion_level=}) of {len(tokens)} tokens {tokenstr!r} 👇"
            )
            stderr.log(tokens)

        # to=TokenClass given
        wanted: Sequence[type[Token]] = to or cast(Sequence[type[Token]], set())
        if wanted:
            # try to reduce the tokens
            result = list(cls.reduce(tokens, to=None, **cond, **conf))
            # check if it's reduces to exactly one matching token
            if len(result) == 1 and any(isinstance(result[0], c) for c in wanted):
                logger.debug(f"{tokenstr!r} does reduce down to {result[0]!r}")
                yield from result
            else:
                raise ValueError(
                    f"Couldn't reduce {tokenstr!r} into a single {' or '.join(t.__name__ for t in wanted)} "
                    f"(instead it reduces to {len(result)} tokens {Token.joinpretty(result)})"
                )
            return

        def reduce_fail_msg(problemtokens):
            return (
                f"Don't know how to interpret or reduce time-related tokens {Token.joinpretty(problemtokens)} (from {Token.join(tokens)!r}). "
                f"If you think this combination does makes sense, consider opening an issue (https://gitlab.com/nobodyinperson/annextimelog/-/issues/new) to discuss."
            )

        ### Step 1: Separate actions from conditions ###
        if None in (conds := set(t.is_condition for t in tokens)) or len(conds) > 1:
            next_is_condition: Optional[bool] = is_condition
            if next_is_condition is not None:
                logger.debug(
                    f"Because {is_condition=}, the following will be {'conditions' if is_condition else 'actions'}"
                )
            match is_condition:
                case None:
                    actions, conditions, unknown = Token.split_by_trigger(
                        tokens, ActionFollowingKeyword, ConditionFollowingKeyword
                    )
                case True:
                    conditions, unknown = Token.split_by_trigger(
                        tokens,
                        ConditionFollowingKeyword,
                        prohibited={ActionFollowingKeyword},
                    )
                    actions = []
                case False:
                    actions, unknown = Token.split_by_trigger(
                        tokens,
                        ActionFollowingKeyword,
                        prohibited={ConditionFollowingKeyword},
                    )
                    conditions = []
            if unknown:
                match bool(actions), bool(conditions):
                    case True, False:
                        logger.debug(
                            f"These previously unknown tokens {unknown} are conditions"
                        )
                        conditions.extend(unknown)
                    case False, True:
                        logger.debug(
                            f"These previously unknown tokens {unknown} are actions"
                        )
                        actions.extend(unknown)
                    case _ if is_condition is True:
                        logger.debug(
                            f"Assuming the unknown tokens {unknown} to be conditions, because {is_condition=}"
                        )
                        conditions.extend(unknown)
                    case _ if is_condition is False:
                        logger.debug(
                            f"Assuming the unknown tokens {unknown} to be actions, because {is_condition=}"
                        )
                        actions.extend(unknown)
                    case _ if any(
                        (
                            (
                                isinstance(t, FieldModifier)
                                and getattr(t, "field", "") == "id"
                            )
                            or isinstance(t, Property)
                        )
                        for t in unknown
                    ) and is_condition is None:
                        logger.info(
                            f"As it's unclear whether tokens {Token.join(unknown)!r} are actions or conditions in this context (no 'set', 'if', etc.), but there are tokens concerning the ID or are a property (starting with a dot), we use those as conditions and the rest as actions."
                        )
                        for token in unknown:
                            match token:
                                case FieldModifier(field="id") | Property():
                                    conditions.append(token)
                                case _:
                                    actions.append(token)

                    case _:
                        raise ValueError(
                            f"Don't know whether tokens {Token.joinpretty(unknown)} are actions or conditions in this context (no 'set', 'if', etc. and {is_condition=})."
                        )
            actions = [t.evolve(is_condition=False) for t in actions]
            conditions = [t.evolve(is_condition=True) for t in conditions]
            logger.debug(
                f"Found {len(conditions)} {conditions = } and {len(actions)} {actions = }"
            )
            if actions:
                logger.debug(
                    f"Reducing {len(actions)} actions {shlex.join(t.string for t in actions)!r}"
                )
                yield from cls.reduce(actions, config=config, is_condition=False)
            if conditions:
                logger.debug(
                    f"Reducing {len(conditions)} conditions {shlex.join(t.string for t in conditions)!r}"
                )
                yield from cls.reduce(conditions, config=config, is_condition=True)
            return

        ### no token is time-related, nothing more to do here
        if not any(isinstance(t, TimeToken) for t in tokens):
            logger.debug(
                f"None of the {len(tokens)} tokens {tokenstr!r} are time-related, so we're done!"
            )
            yield from tokens
            return

        ### all tokens are time-related, convert them to a TimeFrame
        if all(isinstance(t, TimeToken) for t in tokens):
            logger.debug(
                f"All {len(tokens)} tokens {tokenstr!r} are time-related, reducing them down"
            )
            sincetokens, untiltokens, unknowntokens = Token.split_by_trigger(
                tokens, TimeKeywordSince, TimeKeywordUntil
            )
            if logger.getEffectiveLevel() < logging.DEBUG:
                logger.debug(f"{sincetokens = }")
                logger.debug(f"{untiltokens = }")
                logger.debug(f"{unknowntokens = }")
            if unknowntokens and isinstance(tokens[-1], TimeKeywordUntil):
                logger.debug(
                    f"Last token of {Token.join(tokens)!r} is an 'until' (so open interval), meaning *since* {Token.join(unknowntokens)}"
                )
                sincetokens.extend(unknowntokens)
                unknowntokens.clear()
            if sincetokens or untiltokens:
                match bool(sincetokens), bool(untiltokens):
                    case True, False if unknowntokens:
                        logger.debug(
                            f"It's *since* {Token.join(sincetokens)!r}, so *until* {Token.join(unknowntokens)!r}"
                        )
                        untiltokens.extend(unknowntokens)
                    case False, True if unknowntokens:
                        logger.debug(
                            f"It's *until* {Token.join(untiltokens)!r}, so *since* {Token.join(unknowntokens)!r}"
                        )
                        sincetokens.extend(unknowntokens)
                framekwargs: Dict[str, Optional[datetime]] = dict(start=None, end=None)
                rangetokens: Dict[str, Optional[Token]] = dict(since=None, until=None)
                for key, tokens_ in dict(since=sincetokens, until=untiltokens).items():
                    rangetokens[key] = next(
                        cls.reduce(
                            tokens_,
                            to={Time, Duration, TimeFrame},  # type: ignore[arg-type]
                            **kwargs,
                        ),
                        None,
                    )
                    if not rangetokens[key]:
                        continue
                    match key, rangetokens[key]:
                        # don't handle Duration() here yet!
                        case "since", Time(time=t):
                            framekwargs["start"] = t
                        case ["since", Number() as nt] if (
                            tt := Time.from_str(nt.string)
                        ):
                            match tt:
                                case Time(time=t):
                                    framekwargs["end"] = t
                                case TimeFrame(start=t1, end=t2):
                                    framekwargs["end"] = t2 or t1
                        case "until", Time(time=t):
                            framekwargs["end"] = t
                        case ["until", Number() as nt] if (
                            tt := Time.from_str(nt.string)
                        ):
                            match tt:
                                case Time(time=t):
                                    framekwargs["end"] = t
                                case TimeFrame(start=t1, end=t2):
                                    framekwargs["end"] = t2 or t1
                        case "since", TimeFrame(start=t1, end=t2):
                            framekwargs["start"] = t1 or t2
                        case "until", TimeFrame(start=t1, end=t2):
                            framekwargs["end"] = t2 or t1
                logger.debug(f"{rangetokens = }")
                match rangetokens["since"], rangetokens["until"]:
                    case Duration(), Duration():
                        raise ValueError(f"What does {tokenstr!r} mean? 🤔")
                    case Duration(duration=d), _:
                        framekwargs["start"] = (framekwargs["end"] or now) - d
                    case _, Duration(duration=d):
                        framekwargs["end"] = (framekwargs["start"] or now) + d
                logger.debug(f"{framekwargs = }")
                yield TimeFrame(**framekwargs, **ss)  # type: ignore[arg-type]
                return

            logger.debug(
                f"None of the {len(tokens)} tokens {tokenstr!r} is associated to 'since' or 'until', so we're close to the bottom!"
            )

            # interpret the time-related tokens
            match unknowntokens:  # this is where the magic happens 🪄
                # these can't be simplified
                case [TimeFrame()] | [Time()] | [Duration()]:
                    yield from tokens
                case [Time(time=t1), Time(time=t2)]:
                    yield TimeFrame(start=t1, end=t2, **ss)
                case [TimeFrame(start=s1, end=e1), TimeFrame(start=s2, end=e2)]:
                    yield TimeFrame(start=s1 or e1, end=e2 or s1, **ss)
                # if it's a plain number, try to interpret it as a time like '2024' or '04.2023'
                case [Number() as number] if (t_ := Time.from_str(number.string)):
                    yield t_
                # 14 2h        15 for 2h
                case [Integer(value=n), Duration(duration=d)] if 0 <= n < 24:
                    t = dt.now().replace(hour=n, minute=0, second=0, microsecond=0)
                    yield TimeFrame(start=t, end=t + d, **ss)
                # 14:00 2h        15:14 for 3h
                case [Time(time=t), Duration(duration=d)]:
                    yield TimeFrame(start=t, end=t + d, **ss)
                # 10min2sec ago
                case [Duration(duration=d), TimeKeyword(name="ago")]:
                    yield Time(now - d, **ss)
                # long duration form:   1 hour   |    2 weeks   (but not '2 months' - unclear what that means)
                case [Integer(value=n), TimeKeywordUnit(name=unit) as ut] if (
                    d := td.tryargs(**{f"{unit}s": n})  # type: ignore[assignment]
                ):
                    yield Duration(duration=d, **ss)
                case [  # 10 min ago
                    Integer(value=n),
                    TimeKeywordUnit(name=unit) as ut,
                    TimeKeyword(name="ago"),
                ]:
                    match unit:
                        case "year" | "month" | "week":
                            Δt = now.this("day") - now.this(ut.name)
                            yield Time(now.this(unit, offset=-n) + Δt, **ss)
                        case _:
                            yield Time(now - td(**{f"{unit}s": n}), **ss)
                case [  # in 2h
                    TimeKeyword(name="in"),
                    Duration(duration=d),
                ]:
                    yield Time(now + d, **ss)
                case [  # in 4 weeks
                    TimeKeyword(name="in" | "after"),
                    Integer(value=n),
                    TimeKeywordUnit(name=unit) as ut,
                ]:
                    match unit:
                        case "year" | "month" | "week":
                            Δt = now.next("day") - now.this(ut.name)
                            yield Time(now.this(unit, offset=n) + Δt, **ss)
                        case _:
                            yield Time(now + td(**{f"{unit}s": n}), **ss)
                case [
                    Time(time=t),
                    Duration(duration=d),
                ]:  # 10:00 [for] 2h
                    yield TimeFrame(start=t, end=t + d, **ss)
                case [  # last 2h, next 10min
                    TimeKeywordIter() as w,
                    Duration(duration=d),
                ]:
                    yield TimeFrame(
                        start=now + w.n * d,
                        end=now + (w.n + 1) * d,
                        **ss,
                    )
                case [TimeKeywordUnit() as ut]:  # month, week, hour, etc...
                    yield TimeFrame(
                        start=now.this(ut.name, 0, **wss),
                        end=now.this(ut.name, 1, **wss),
                        **ss,
                    )
                case [  # last month, this week, next hour, etc.
                    TimeKeywordIter() as w,
                    TimeKeywordUnit() as ut,
                ]:
                    yield TimeFrame(
                        start=now.this(ut.name, w.n, **wss),
                        end=now.this(ut.name, w.n + 1, **wss),
                        **ss,
                    )
                # January  Feb  March nov dec ...
                case [TimeKeywordMonth() as mt]:
                    yield TimeFrame(start=mt.start(), end=mt.end(), **ss)
                # last december    next feb
                case [TimeKeywordIter() as it, TimeKeywordMonth() as mt]:
                    yield TimeFrame(
                        start=mt.start(offset=it.n), end=mt.end(offset=it.n), **ss
                    )
                case [  # this Monday
                    TimeKeywordIter() as i,
                    TimeKeywordDay() as day,
                ]:
                    yield TimeFrame(
                        start=now.this(day.name, offset=i.n, **wss),
                        end=now.this(day.name, offset=i.n, **wss) + td(days=1),
                        **ss,
                    )
                case [  # Friday 12[:00]
                    TimeKeywordDay() as day,
                    Time() | Number() as ttnt,
                    # a bit inefficient to re-convert the Time() here, but it reduces duplication
                ] if isinstance((tt := Time.from_str(ttnt.string)), Time):
                    yield Time(
                        time=now.this(day.name, **wss).replace(
                            hour=tt.time.hour,
                            minute=tt.time.minute,
                            second=tt.time.second,
                        ),
                        **ss,
                    )
                case [  # next Monday 10[:00]
                    TimeKeywordIter() as i,
                    TimeKeywordDay() as day,
                    Time() | Number() as ttnt,
                    # a bit inefficient to re-convert the Time() here, but it reduces duplication
                ] if isinstance((tt := Time.from_str(ttnt.string)), Time):
                    yield Time(
                        time=now.this(day.name, offset=i.n, **wss).replace(
                            hour=tt.time.hour,
                            minute=tt.time.minute,
                            second=tt.time.second,
                        ),
                        **ss,
                    )
                case [TimeKeywordDay() as day]:  # Monday Tueday Wed Fri ...
                    yield TimeFrame(start=day.start(**wss), end=day.end(**wss), **ss)
                case [
                    TimeKeywordDay() as day,
                    TimeKeywordIter() as i,
                    TimeKeywordUnit() as u,
                ]:  # Monday next week
                    p = now.this(u.name, offset=i.n)  # 'next week'
                    yield TimeFrame(
                        start=p.this(day.name),  # day in that week
                        end=p.this(day.name)
                        + td(days=1),  # end of that day / start of next day
                        **ss,
                    )
                case [TimeKeywordPeriod() as w]:
                    yield TimeFrame(start=w.start, end=w.end, **ss)
                case _:
                    logger.debug(msg := reduce_fail_msg(unknowntokens))
                    raise ValueError(msg)
            return
        else:  ### separation into time-related tokens and other tokens needed ###
            timetokens: List[TimeToken] = []
            othertokens: List[Token] = []
            # sort out the time-related tokens
            for token in tokens:
                match token:
                    case TimeToken():
                        if logger.getEffectiveLevel() < logging.DEBUG:
                            logger.debug(f"{token!r} is a TimeToken")
                        timetokens.append(token)
                    case _:
                        if logger.getEffectiveLevel() < logging.DEBUG:
                            logger.debug(f"{token!r} is NOT a TimeToken")
                        othertokens.append(token)
            logger.debug(
                f"{tokenstr!r} is split into {len(timetokens)} time-related tokens {timetokens} "
                f"and {len(othertokens)} other tokens {othertokens}"
            )
            if timetokens:
                yield from cls.reduce(timetokens, config=config, **kwargs)
            yield from othertokens

    @classmethod
    def from_strings(
        cls,
        strings: Union[str | Sequence[str]],
        reduce: bool = True,
        config: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Sequence[Union[Token | None]]:
        match strings:
            case str():
                strings = shlex.split(given := strings)
                logger.debug(f"from_strings({given!r}): split into {strings}")
        tokens = [cls.from_str(s) for s in strings]
        if reduce:
            tokens = list(cls.reduce(tokens, config=config, **kwargs))
        elif kwargs:
            warnings.warn(f"from_strings(): unused {kwargs = } with {reduce = }")
        return tokens

    def evolve(self, **kwargs) -> Token:
        return dataclasses.replace(self, **kwargs)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @staticmethod
    def recurse_into_subclasses(decorated_fun):
        @classmethod
        @functools.wraps(decorated_fun)
        def wrapper(cls, *args, **kwargs):
            for subcls in cls.__subclasses__():
                if method := getattr(subcls, decorated_fun.__name__, None):
                    if token := method(*args, **kwargs):
                        return token
            return decorated_fun(cls, *args, **kwargs)

        return wrapper


@dataclass(frozen=True)
class Noop(Token):
    FILLERWORDS = set(
        sorted(
            """
        the about beside near to above between of towards across beyond off under after by
        on underneath against despite onto unlike along down opposite among
        during out up around except outside upon as over via past with at for before
        round within behind inside without below into than beneath like through
        """.split()
        )
    )

    @property
    def pretty(self) -> str:
        return f"{self.string!r}: do nothing"

    @Token.recurse_into_subclasses
    def from_str(cls, string: str, **kwargs) -> Union[Token, None]:
        if re.fullmatch(r"\s*", string) or string.lower() in cls.FILLERWORDS:
            return cls(string=string, **kwargs)  # type: ignore[operator]
        return None

    def __str__(self) -> str:
        return ""


@dataclass(frozen=True)
class ConditionCombinationKeyword(Noop):
    KEYWORDS = "and or not".split()

    @classmethod
    def from_str(
        cls, string: str, **kwargs
    ) -> Union[ConditionCombinationKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            logger.warning(
                f"{string!r} does not actually alter how conditions are met or actions are performed (yet! Maybe it will in a future release...)"
            )
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class ConditionFollowingKeyword(Token):
    KEYWORDS = "where while if but although despite when given".split()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[ConditionFollowingKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class ActionFollowingKeyword(Token):
    KEYWORDS = "do then set change modify mod edit update".split()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[ActionFollowingKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class TimeToken(Token):
    pass


@dataclass(frozen=True)
class Number(TimeToken):
    value: float


@dataclass(frozen=True)
class Integer(Number):
    value: int

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Optional[Integer]:
        try:
            return cls(value=int(string), string=string)
        except Exception:
            return None

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Float(Number):
    value: float

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Optional[Float]:
        try:
            return cls(value=float(string), string=string)
        except Exception:
            return None

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class TimeKeyword(TimeToken):
    name: str
    KEYWORDS: ClassVar = set("ago in after".split())

    @Token.recurse_into_subclasses
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, name=string, **kwargs)  # type: ignore[operator]
        return None

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class TimeKeywordIter(TimeKeyword):
    KEYWORDS: ClassVar[Dict[str, int]] = {
        "this": 0,
        "next": 1,
        "coming": 1,
        "following": 1,
        "last": -1,
        "prev": -1,
        "previous": -1,
    }

    @property
    def n(self) -> int:
        return self.KEYWORDS.get(self.name, 0)


@dataclass(frozen=True)
class TimeKeywordUnit(TimeKeyword):
    KEYWORDS: ClassVar = tuple("second minute hour day week month year".split())

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordUnit, None]:
        for kw in cls.KEYWORDS:
            if string.lower() in {kw, f"{kw}s"} or (
                kw in "second minute month"
                and len(string) >= 3
                and kw.startswith(string)
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    @property
    def one_smaller(self) -> TimeKeywordUnit:
        smallerunit = self.KEYWORDS[0]
        for smaller, unit in zip(self.KEYWORDS, list(self.KEYWORDS)[1:]):
            logger.debug(f"{smaller = }, {unit = }, {self.name = }")
            if unit == self.name:
                smallerunit = smaller
                break
        return cast(TimeKeywordUnit, self.evolve(name=smallerunit, string=smallerunit))


@dataclass(frozen=True)
class TimeKeywordPeriod(TimeKeyword):
    KEYWORDS: ClassVar = {"today": 0, "yesterday": -1, "tomorrow": 1}

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordPeriod, None]:
        for kw in cls.KEYWORDS:
            if string.lower() == kw or (
                len(string) >= 3 and kw.startswith(string.lower())
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    @property
    def n(self) -> int:
        return self.KEYWORDS.get(self.name, 0)

    @property
    def start(self) -> datetime:
        return dt.now().this("day", offset=self.KEYWORDS.get(self.name, 0))

    @property
    def end(self) -> datetime:
        return dt.now().this("day", offset=self.KEYWORDS.get(self.name, 0) + 1)


@dataclass(frozen=True)
class TimeKeywordDay(TimeKeyword):
    # TODO: Can't use datetime.WEEKDAYS for some reason!?
    KEYWORDS: ClassVar = (
        "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    )

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordDay, None]:
        for kw in cls.KEYWORDS:
            if (
                string.lower() == kw.lower()  # monday tuesday wednesday ...
                # mon tues thursd fr ...
                or (len(string) >= 2 and kw.lower().startswith(string.lower()))
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    def start(self, **kwargs) -> datetime:
        return dt.now().this(self.name, **kwargs)

    def end(self, **kwargs) -> datetime:
        return self.start(**kwargs) + timedelta(days=1)


@dataclass(frozen=True)
class TimeKeywordMonth(TimeKeyword):
    KEYWORDS: ClassVar = "January February March April May June July August September October November December".split()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Optional[TimeKeywordMonth]:
        for kw in cls.KEYWORDS:
            if (
                string.lower() == kw.lower()  # janua february march decemb...
                # jan feb mar...
                or (len(string) >= 3 and kw.lower().startswith(string.lower()))
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    def start(self, **kwargs) -> datetime:
        return dt.now().this(self.name, **kwargs)

    def end(self, **kwargs) -> datetime:
        return self.start(**kwargs).next("month")


@dataclass(frozen=True)
class TimeKeywordUntil(TimeKeyword):
    KEYWORDS = set("until til till to -".split())


@dataclass(frozen=True)
class TimeKeywordSince(TimeKeyword):
    KEYWORDS = set("since starting from".split())


@dataclass(frozen=True)
class Time(TimeToken):
    """
    A specification of a point in time, such as:

        10     # 10:00 today
        y10    # yesterday 10:00
        yy10   # day before yesterday 10:00
        t10    # tomorrow 10:00
        tt10   # day after tomorrow 10:00
        2023-12-30T13:13:40+0200    # full ISO format
        13:13:40 # partial full ISO format
        ...
    """

    time: datetime

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Optional[Union[Time, TimeFrame]]:
        if string is None:
            return None
        offset = timedelta(days=0)
        if m := re.search(r"^(?P<prefix>[yt]+)(?P<rest>.*)$", string):
            offset = timedelta(
                days=sum(dict(y=-1, t=1).get(c, 0) for c in m.group("prefix"))
            )
            if string := m.group("rest"):
                pass
                # logger.debug(
                #     f"{string!r} starts with {m.group('prefix')!r}, so thats as an {offset = }"
                # )
            else:
                logger.debug(f"{string!r} means an {offset = } from today")
                return cls(
                    string=string,
                    time=dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    + offset,
                    **kwargs,
                )

        # Try the bigger periods
        for period, formats in dict(
            year="%Y".split(),
            month="%Y-%m    %Y/%m   %m.%Y   %Y%m".split(),
            day="%Y-%m-%d   %Y/%m/%d   %d.%m.%Y".split(),
        ).items():
            for fmt in formats:
                try:
                    r = dt.strptime(string, fmt)
                except Exception as e:
                    continue
                if not r:
                    continue
                return TimeFrame(
                    string=string, start=r.this(period), end=r.next(period)
                )

        # Try full time specifications
        if re.fullmatch(r"\d{3}", string):
            # prepend zero to '100', otherwise interpreted as 10:00
            string = f"0{string}"
        result = None
        todaystr = dt.now().strftime(todayfmt := "%Y-%m-%d")
        for i, f in enumerate(
            (
                lambda s: dt.now() if s == "now" else None,
                dt.fromisoformat,
                # lambda s: dt.fromisoformat(f"{todaystr} {s}"),
                # Python<3.11 fromisoformat is limited, we implement the basic formats here
                # so we need to do it manually...
                lambda s: dt.strptime(s, "%Y-%m-%dT%H:%M%z"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H:%M%z"),
                lambda s: dt.strptime(s, "%Y-%m-%dT%H:%M:%S"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H:%M:%S"),
                lambda s: dt.strptime(s, "%Y-%m-%dT%H:%M:%S%z"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H:%M:%S%z"),
                # conflicts with just year, e.g. '2024'
                # lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H%M"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H:%M"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H%M"),
            )
        ):
            try:
                if result := f(string):
                    break
            except Exception as e:
                pass
        if result:
            result += offset
            return Time(string=string, time=result)

        return None

    def __str__(self) -> str:
        return self.time.strftime("%Y-%m-%dT%H:%M:%S%z")


@dataclass(frozen=True)
class TimeStart(Time):
    def __str__(self):
        return f"start={self.time.isoformat()}"


@dataclass(frozen=True)
class TimeEnd(Time):
    def __str__(self):
        return f"end={self.time.isoformat()}"


@dataclass(frozen=True)
class TimeFrame(TimeToken):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeFrame, None]:
        if m := re.fullmatch(r"[({\[](?P<start>.*);(?P<end>.*)[)}\]]", string.strip()):
            if not (start := Time.from_str(s := m.group("start"))) and s:
                return None
            if not (end := Time.from_str(s := m.group("end"))) and s:
                return None
            return cls(
                string=string,
                start=getattr(start, "time", None),
                end=getattr(end, "time", None),
                **kwargs,
            )
        return None

    def __str__(self):
        return f"[{';'.join((t.isoformat() if t else '') for t in (self.start, self.end))}]"


@dataclass(frozen=True)
class Duration(TimeToken):
    """
    A duration specified in the following format:

        10min
        2h30m
        1week2days3hours4minutes5seconds
        1w2d3h4m5s
        ...
    """

    duration: timedelta

    UNITS = ["weeks", "days", "hours", "minutes", "seconds"]

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Duration, None]:
        durations: List[timedelta] = []
        matches: int = 0
        s = string
        while s:
            if m := re.match(
                rf"[^\da-z]*(?P<number>\d+(?:\.\d+)?)[^\da-z]*(?P<unit>[a-z]+)[^\da-z]*",
                s,
                flags=re.IGNORECASE,
            ):
                number, unit = m.groups()
                if kwarg := next(
                    (u for u in cls.UNITS if u.startswith(unit.lower())), None
                ):
                    durations.append(timedelta(**{kwarg: float(number)}))
                s = s[m.span()[-1] :]  # drop this match and go on
                continue
            else:
                return None
        if not durations:
            return None
        return cls(string=string, duration=sum(durations, start=timedelta(0)), **kwargs)

    def __str__(self) -> str:
        parts: List[Tuple[int, str]] = []
        duration = self.duration
        for unit in sorted(self.UNITS, key=lambda u: timedelta(**{u: 1}), reverse=True):
            unitdelta = timedelta(**{unit: 1})
            if abs(duration) < abs(unitdelta):
                continue
            unitblocks = duration // unitdelta
            parts.append((unitblocks, unit))
            duration -= unitblocks * unitdelta  # type: ignore[assignment]
        return "".join(f"{n}{u[0]}" for n, u in parts if n)


@dataclass(frozen=True)
class Property(Token):
    KEYWORDS: ClassVar = set(
        "open openstart openend hasend hasstart closed timepoint empty".split()
    )

    name: str

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Property, None]:
        for kw in cls.KEYWORDS:
            if f".{kw}" == string.lower():
                return cls(string=string, name=kw, **kwargs)
        return None

    def __str__(self) -> str:
        return f".{self.name}"


@dataclass(frozen=True)
class FieldModifier(Token):
    """
    A metadata field modifier such as:

        field=value          # set 'field' to (only) 'value'
        field+=value         # add 'value' to 'field'
        field=bla,bli,blubb  # set 'field' to given three values
        field+=bla,bli,blubb # add multiple values to 'field'
        field-=value         # remove 'value' from 'field'
        field-=bla,bli,blubb # remove multiple values from 'field'
        field+/=a,b,c/d,e,f  # different separator (this adds 'a,b,c' and 'd,e,f' to 'field')
    """

    field: str

    # don't want to put too many in here, syntax might be needed later
    SEPARATORS: ClassVar = ",;:"
    # we don't allow a dot in front (reserved for Property() token), otherwise
    # this is what git annex supports
    FIELD_NAME_REGEX: ClassVar = re.compile(r"^(?!\.)[\w_.-]+$", re.IGNORECASE)

    @classmethod
    def from_str(
        cls, string: str, **kwargs
    ) -> Union[FieldModifier, TimeStart, TimeEnd, Noop, None]:
        # short form
        if m := re.search(r"^(?P<symbol>[@:=])(?P<value>.*)$", string.strip()):
            field = {"@": "location", ":": "note", "=": "title"}.get(
                m.group("symbol"), ""
            )
            kwargs = dict(
                string=string, field=field, values=set([m.group("value")]), **kwargs
            )
            return SetField(**kwargs)
        # long form
        if m := re.search(
            rf"(?P<field>\S+?)(?P<operator>[+-]?)(?P<sep>[{cls.SEPARATORS}]?)=(?P<values>.*)",
            string,
        ):
            field, operator, sep, givenvalues = m.groups()
            if not cls.FIELD_NAME_REGEX.fullmatch(field):
                logger.warning(f"{field!r} is an invalid metadata field name")
                return None
            if not sep and re.search(r"\s+", givenvalues):
                values = [givenvalues.strip()]
            else:
                sep = sep or ","
                values = [
                    v.strip()
                    for v in re.split(rf"(?:{re.escape(sep)})+", givenvalues)
                    if v
                ]
            values = cast(List[str], values)
            match field.lower():
                case "start" | "end" as field_:
                    # start='in 10min', separated by whitespace, not comma like other fields
                    values = shlex.split(m.group("values"))
                    if operator in "-+".split():
                        logger.warning(
                            f"Ignoring {operator = !r} in {string} (start and end field are special)"
                        )
                        operator = ""
                    if not values:
                        return SetField(field_, frozenset(), string=string)
                    try:
                        timetokens: List[TimeToken] = []
                        othertokens: List[Token] = []
                        logger.debug(
                            f"{string!r}: Determining what {field_} time {shlex.join(values)!r} means"
                        )
                        for token in Token.from_strings(
                            list(values), is_condition=False
                        ):
                            match token:
                                case TimeToken():
                                    timetokens.append(token)
                                case t if t:
                                    othertokens.append(token)
                                    logger.warning(
                                        f"While parsing {values} (from {string!r}): Ignoring {token.string!r} as it is not time-related"
                                    )
                    except ValueError as e:
                        raise ValueError(
                            f"While parsing {values} (from {string!r}): {e}"
                        )
                    time: Optional[datetime] = None
                    match timetokens:
                        case [Time(time=time_)]:
                            time = time_
                        case [TimeFrame(start=start, end=end)]:
                            match field_:
                                case "start":
                                    time = start or end
                                case "end":
                                    time = end or start
                    if not time:
                        raise ValueError(
                            f"{values} (from {string!r}) doesn't parse to an interpretable time "
                            f"(but to {timetokens} and ignored elements {othertokens})"
                        )
                    match field_:
                        case "start":
                            return TimeStart(time=time, string=string)
                        case "end":
                            return TimeEnd(time=time, string=string)
                case (
                    "tags"
                ):  # git annex uses field 'tag' for tags, for convenience adjust it here
                    field = "tag"
                # aliases for the location field
                case str() as f if "location".startswith(
                    f
                ) or f in "at in where".split():
                    field = "location"
            valueset = frozenset(values)
            match operator:
                case "+":
                    return AddToField(field=field, values=valueset, string=string)
                case "-":
                    return RemoveFromField(field=field, values=valueset, string=string)
                case _ if values:
                    return SetField(field=field, values=valueset, string=string)
                case _:
                    return UnsetField(field=field, string=string)
        return None


@dataclass(frozen=True)
class FieldValueModifier(FieldModifier):
    values: FrozenSet[str]

    def __post_init__(self):
        object.__setattr__(self, "values", frozenset(self.values))

    @property
    def separator(self) -> Union[str, None]:
        for sep in self.SEPARATORS:
            if not any(sep in v for v in self.values):
                return sep
        return None

    @property
    def values_joined(self) -> Tuple[str, str]:
        if sep := self.separator:
            return sep, sep.join(map(str.strip, self.values))
        else:
            it = iter(self.SEPARATORS)
            sep, repl = (next(it, "") for i in range(2))
            logger.warning(
                f"Don't know what separator to use for the values in {self!r}. "
                f"None of {self.SEPARATORS!r} is safe to use they're all present in the values and we don't have an escaping mechanism. "
                f"Falling back to {sep!r} and replacing all its occurrences with {repl!r}."
            )
            return sep, sep.join(v.replace(sep, repl).strip() for v in self.values)


@dataclass(frozen=True)
class UnsetField(FieldModifier):
    def __str__(self) -> str:
        return f"{self.field}="


@dataclass(frozen=True)
class SetField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}{sep if sep != ',' else ''}={joined}"


@dataclass(frozen=True)
class AddToField(FieldValueModifier):
    def __str__(self):
        if (
            len(self.values) == 1
            and self.field.lower() in ["tag", "tags"]
            and isinstance(Token.from_str(value := next(iter(self.values))), AddToField)
        ):
            # shortcut for tags that are not interpreted as another token
            return f"{value}"
        else:
            sep, joined = self.values_joined
            return f"{self.field}+{sep if sep != ',' else ''}={joined}"


@dataclass(frozen=True)
class RemoveFromField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}-{sep if sep != ',' else ''}={joined}"
