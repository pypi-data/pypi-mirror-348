# system modules
import logging
import itertools
import unittest
import shlex
from datetime import timezone
from unittest import TestCase
from unittest.mock import patch

# internal modules
from annextimelog.repo import Event
from annextimelog.token import *
from annextimelog.utils import Range, RangeMerger
from annextimelog.datetime import datetime, datetime as dt, timedelta as td, timedelta

logger = logging.getLogger(__name__)


def today(**kwargs):
    return dt.now().replace(
        **{**dict(hour=0, minute=0, second=0, microsecond=0), **kwargs}
    )


def days(n):
    return timedelta(days=n)


class RangeTest(TestCase):
    def test_range_overlaps(self):
        self.assertTrue(Range(1, 2).overlaps(Range(2, 3)))
        self.assertTrue(Range(2, 3).overlaps(Range(2, 3)))
        self.assertFalse(Range(1, 10).overlaps(Range(20, 30)))

    def test_range_extend(self):
        self.assertEqual(Range(1, 2).extend(Range(2, 3)), Range(1, 3))
        self.assertEqual(Range(1, 2).extend(Range(4, 5)), Range(1, 5))
        self.assertEqual(Range(-10, 20).extend(Range(0, 1)), Range(-10, 20))

    def test_range_merger(self):
        m = RangeMerger()
        m.add(Range(1, 2))
        m.add(Range(2, 3))
        self.assertListEqual(m.ranges, [Range(1, 3)])
        m.add(Range(10, 20))
        self.assertListEqual(m.ranges, [Range(1, 3), Range(10, 20)])
        m.add(Range(2, 11))
        m.collapse()
        self.assertListEqual(m.ranges, [Range(1, 20)])
        self.assertEqual(m.total, 19)


class DatetimeTest(TestCase):
    WEEKDAYS: Dict[Union[int, str], Union[int, str]] = dict(
        zip("Mon Tue Wed Thu Fri Sat Sun".split(), itertools.count(0))
    )
    WEEKDAYS.update({v: k for k, v in WEEKDAYS.items()})

    def test_pretty_duration(self):
        for kw, units, s in [
            (dict(hours=1, minutes=30), "h", "1.5h"),
            (dict(hours=1, minutes=30), "wdhms", "1h30m"),
            (dict(hours=1.5, minutes=1), "wdhms", "1h31m"),
            (dict(hours=1.5, minutes=1.2), "wdhms", "1h31m12s"),
        ]:
            with self.subTest(
                msg := f"timedelta(**{kw}).pretty_duration({units!r}) should be {s!r}"
            ):
                self.assertEqual(
                    (r := str(td(**kw).pretty_duration(units))),
                    s,
                    msg=f"{msg}, not {r!r}",
                )

    def test_this(self):
        for parts in [
            "2023-12-04T10:30  hour 2023-12-04T09:00 2023-12-04T10:00 2023-12-04T11:00",
            "2024-01-01T00:15   day 2023-12-31T00:00 2024-01-01T00:00 2024-01-02T00:00",
            "2025-02-15T15:34  week 2025-02-03T00:00 2025-02-10T00:00 2025-02-17T00:00",
            "2024-05-18T22:52 month 2024-04-01T00:00 2024-05-01T00:00 2024-06-01T00:00",
            "2024-05-18T22:52  year 2023-01-01T00:00 2024-01-01T00:00 2025-01-01T00:00",
            "2024-05-18T22:52 march 2023-03-01T00:00 2024-03-01T00:00 2025-03-01T00:00",
        ]:
            d, u, p, t, n = parts.split()
            d = dt.fromisoformat(d)
            for m, s in dict(prev=p, this=t, next=n).items():
                with self.subTest(desc := f"{d!r}.{m}({u!r})"):
                    self.assertEqual(
                        (r := getattr(d, m)(u)),
                        dt.fromisoformat(s),
                        f"{desc} should be {s}, but is {r}",
                    )
                if u in {"week"}:
                    for weekstartssunday in {True, False}:
                        with self.subTest(
                            desc := f"{d!r}.{m}({u!r},{weekstartssunday = })"
                        ):
                            self.assertEqual(
                                (
                                    r := d.this(
                                        u, weekstartssunday=weekstartssunday
                                    ).weekday()
                                ),
                                self.WEEKDAYS[
                                    day := "Sun" if weekstartssunday else "Mon"
                                ],
                                f"{desc} should be a {day} but is a {self.WEEKDAYS[r]}",
                            )

    def test_this_weekday_stays_that_weekday(self):
        for t, method, (day, nth_day) in itertools.product(
            "2023-01-04 2024-06-18 2025-08-31".split(),
            "prev this next".split(),
            self.WEEKDAYS.items(),
        ):
            if not isinstance(day, str):
                continue
            t = dt.fromisoformat(t)
            with self.subTest(call := f"{t}.{method}({day!r})"):
                self.assertEqual(
                    (r := getattr(t, method)(day)).weekday(),
                    nth_day,
                    msg=f"{call} ({r}) should be a {day}, but is a {self.WEEKDAYS[nth_day]}",
                )
                match method:
                    case "prev":
                        self.assertLess(r, t, msg=f"{call} ({r}) should be before {t}")
                    case "this":
                        self.assertLessEqual(
                            abs(r - t),
                            timedelta(days=(dd := 7)),
                            msg=f"{call} ({r}) shouldn't be more than {dd} days away from {t}",
                        )
                    case "next":
                        self.assertGreater(
                            r, t, msg=f"{call} ({r}) should be after than {t}"
                        )


class TokenTest(TestCase):
    def test_timekeywordunit_one_smaller(self):
        for smaller, bigger in zip(
            TimeKeywordUnit.KEYWORDS, TimeKeywordUnit.KEYWORDS[1:]
        ):
            self.assertEqual(
                TimeKeywordUnit(bigger).one_smaller, TimeKeywordUnit(smaller)
            )
        self.assertEqual(
            TimeKeywordUnit("second").one_smaller, TimeKeywordUnit("second")
        )

    def test_fieldmodifier(self):
        for s, r in {
            "a": AddToField("tag", {"a"}),
            "tag+=until": AddToField("tag", {"until"}),
            "tag+=a,b,c": AddToField("tag", {"a", "b", "c"}),
            "tags+=a,b,c": AddToField("tag", {"a", "b", "c"}),
            "tags-=a,b,c": RemoveFromField("tag", {"a", "b", "c"}),
            "tags=a,b,c": SetField("tag", {"a", "b", "c"}),
            "tags=": UnsetField("tag"),
            "field=": UnsetField("field"),
            "@home": SetField("location", {"home"}),
            "at=home": SetField("location", {"home"}),
            "in=Berlin,Germany": SetField("location", {"Berlin", "Germany"}),
            "where+=in town": AddToField("location", {"in town"}),
            "note=long sentence, with comma": SetField(
                "note", {"long sentence, with comma"}
            ),
            "note,=words with spaces,still separated by comma": SetField(
                "note", {"words with spaces", "still separated by comma"}
            ),
            "id=bla": SetField("id", {"bla"}),
            "id-=bla": RemoveFromField("id", {"bla"}),
            "id+=bla": AddToField("id", {"bla"}),
            "id=": UnsetField("id"),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(Token.from_str(s), r)

    def test_fieldmodifier_multiple(self):
        self.assertNotEqual(
            SetField.from_str(str(t := SetField("f", set(SetField.SEPARATORS)))),
            t,
            msg="when values contain all separators, stringification shouldn't round-trip, but here it does!?",
        )

    def test_duration(self):
        for s, kw in {
            "10m": dict(minutes=10),
            "10m+2h": dict(minutes=10, hours=2),
            "2h 10m": dict(minutes=10, hours=2),
            "2h30m": dict(hours=2, minutes=30),
            "   1   w   2  days 3 hour  4 min 5 sec": dict(
                weeks=1, days=2, hours=3, minutes=4, seconds=5
            ),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(
                    Token.from_str(s), Duration(string=s, duration=timedelta(**kw))
                )

    def test_from_string_roundtrip(self):
        for s in [
            "10:00",
            "until",
            "bla",
            "10min",
            "10m2h",
            "10.5h",
            "1.5d5.3h",
            "field=value",
            "field+=value",
            "field=",
            "field-=value",
            "tag+=until",
            "tag+=until,bla",
            "field+;=10:00;yesterday",
            "start=10:00",
            "end=10:00",
            "end=",
            "[;]",
            "[10:00;]",
            "[;10:30]",
            "[8;10]",
            "2",
            "2024",
            "2.4",
            "dec" "January",
            "Feb",
            "",
        ]:
            with self.subTest(string=s):
                token = Token.from_str(s)
                self.assertEqual(token.roundtrip, token)

    @staticmethod
    def strip_microseconds(tokens):
        for token in tokens:
            match token:
                case Time(time=time):
                    yield token.evolve(time=time.replace(microsecond=0))
                case TimeFrame(start=t1, end=t2):
                    yield t.evolve(
                        start=t1.replace(microsecond=0),
                        end=t2.replace(microsecond=0),
                    )
                case _:
                    yield token

    def test_from_strings_reduced(self):
        now = dt.now()
        for input, shouldbe in {
            "10min ago": [Time(now - td(minutes=10))],
            "in 2h": [Time(now + td(hours=2))],
            "10:00": [Time(today(hour=10))],
            "bla blubb": [AddToField("tag", {"bla"}), AddToField("tag", {"blubb"})],
            "in 1 hour": [Time(now + td(hours=1))],
        }.items():
            with self.subTest(f"Token.from_strings({input!r}) should be {shouldbe}"):
                tokens = Token.from_strings(
                    shlex.split(input), reduce=True, **(kw := dict(is_condition=True))
                )
                shouldbe = [t.evolve(**kw) for t in shouldbe]
                shouldbe = list(self.strip_microseconds(shouldbe))
                tokens = list(self.strip_microseconds(tokens))
                self.assertSequenceEqual(
                    tokens,
                    shouldbe,
                    f"Token.from_strings({input!r}) should be {shouldbe} but is {tokens}",
                )

    def test_from_strings_unreduced(self):
        now = dt.now()
        for input, shouldbe in {
            "2.5": [Float(2.5)],
            ".open": [Property("open")],
            ".closed": [Property("closed")],
            ".timepoint": [Property("timepoint")],
        }.items():
            with self.subTest(
                f"Token.from_strings({input!r},reduce=False) should be {shouldbe}"
            ):
                tokens = Token.from_strings(shlex.split(input), reduce=False)
                shouldbe = list(self.strip_microseconds(shouldbe))
                tokens = list(self.strip_microseconds(tokens))
                self.assertSequenceEqual(
                    tokens,
                    shouldbe,
                    f"Token.from_strings({input!r},reduce=False) should be {shouldbe} but is {tokens}",
                )

    def test_timeframe_from_strings(self):
        now = dt.now()
        for input, (start, end) in {
            "y10:00 - now": (today(hour=10) - days(1), now),
            "y10:00 until now": (today(hour=10) - days(1), now),
            "til 5min ago": (None, now - td(minutes=5)),
            "y10:00 until 10min ago": (
                today(hour=10) - days(1),
                now - td(minutes=10),
            ),
            "2h ago - now": (now - td(hours=2), now),
            "2h ago til 1h ago": (now - td(hours=2), now - td(hours=1)),
            "1h since 10:00": (t := today(hour=10), today(hour=11)),
            "1h until 10:00": (t := today(hour=9), today(hour=10)),
            "1h since 2h ago": (now - td(hours=2), now - td(hours=1)),
            "1h until 2h ago": (now - td(hours=3), now - td(hours=2)),
            # "15min": (now - td(minutes=15), now), # handled in Event.apply() instead
            "this day": (today(), today() + days(1)),
            "until this day": (None, today() + days(1)),
            "since this hour": (now.this("hour"), None),
            "since yesterday": (today() - days(1), None),
            "until today": (None, today() + days(1)),
            "until tomorrow": (None, today() + days(2)),
            "2024": (dt(2024, 1, 1), dt(2025, 1, 1)),
            "2024-04": (dt(2024, 4, 1), dt(2024, 5, 1)),
            "2024-04-04": (dt(2024, 4, 4), dt(2024, 4, 5)),
            "04.2025": (dt(2025, 4, 1), dt(2025, 5, 1)),
            "12.2025": (dt(2025, 12, 1), dt(2026, 1, 1)),
            "14 for 2h": (today(hour=14), today(hour=16)),
            "15:30 for 30min": ((t := today(hour=15, minute=30)), t + td(minutes=30)),
            "10 min ago - in 10 min": (now - td(minutes=10), now + td(minutes=10)),
            "jan - dec": (
                today().replace(month=1, day=1),
                today().replace(year=now.year + 1, month=1, day=1),
            ),
            "november": (
                today().replace(month=11, day=1),
                today().replace(month=12, day=1),
            ),
        }.items():
            with self.subTest(input=input):
                tokens = Token.from_strings(
                    shlex.split(input), reduce=True, is_condition=True
                )
                token = next((t for t in tokens if isinstance(t, TimeFrame)), None)
                self.assertEqual(
                    bool(a := getattr(token, "start", None)),
                    bool(b := start),
                    msg=f"start should be {b} but is {a}",
                )
                self.assertEqual(
                    bool(a := getattr(token, "end", None)),
                    bool(b := end),
                    msg=f"end should be {b} but is {a}",
                )
                if start:
                    self.assertTrue(
                        abs(token.start - start).total_seconds() < 5,
                        msg=f"start should be {start} but is {token.start}",
                    )
                if end:
                    self.assertTrue(
                        abs(token.end - end).total_seconds() < 5,
                        msg=f"end should be {end} but is {token.end}",
                    )

    def test_from_strings_actions_conditions(self):
        for cmdline, (actions, conditions) in {
            # "bla": ({AddToField("tag", {"bla"})}, set()),
            "set @home if thistag": (
                {SetField("location", {"home"})},
                {SetField("tag", {"thistag"})},
            ),
            "when id=asdf tag1 update @home": (
                {SetField("location", {"home"})},
                {SetField("id", {"asdf"}), AddToField("tag", {"tag1"})},
            ),
            # "a b c ": (3, 0),
            "if a b c": (0, 3),
            "set if a b c": (0, 3),
            "if a b c set": (0, 3),
            "set tag1 until now": (2, 0),
            "until now set end=yesterday": (1, 1),
            "since yesterday @guz update myfield+=value @home": (2, 2),
            "today note=this mod location=home": (1, 2),
        }.items():
            with self.subTest(
                f"{cmdline!r} should yield {len(actions) if hasattr(actions,'__len__') else actions} actions "
                f"and {len(conditions) if hasattr(conditions,'__len__') else conditions} conditions"
            ):
                tokens = Token.from_strings(shlex.split(cmdline))
                unhandled, actions_, conditions_ = set(), set(), set()
                for token in tokens:
                    match token:
                        case Token(is_condition=True):
                            conditions_.add(token)
                        case Token(is_condition=False):
                            actions_.add(token)
                        case _:
                            unhandled.add(token)
                self.assertFalse(
                    unhandled,
                    msg=f"from_strings({cmdline!r}) shouldn't return unhandled tokens, but did: {unhandled}",
                )
                for name, (result, shouldbe, is_condition) in dict(
                    actions=(actions_, actions, False),
                    conditions=(conditions_, conditions, True),
                ).items():
                    match shouldbe:
                        case int():
                            self.assertEqual(
                                len(result),
                                shouldbe,
                                f"\n\nfrom_strings({cmdline!r}) should return {shouldbe} {name}, but instead returned {len(result)}",
                            )
                        case set():
                            shouldbe = {
                                t.evolve(is_condition=is_condition) for t in result
                            }
                            self.assertSetEqual(
                                result,
                                shouldbe,
                                f"\n\nfrom_strings({cmdline!r}) should return {name}\n{shouldbe}\nbut instead returned\n{result}",
                            )
                        case _:
                            self.fail(
                                f"wtf is {shouldbe!r} ({type(shouldbe)})? Should be int (how many {name}?) or set (the actual {name})"
                            )

    def test_from_strings_invalid_raises(self):
        for cmdline, kwargs in {
            "set bla": dict(is_condition=True),
            "if bla": dict(is_condition=False),
            "id=1 if @home": dict(is_condition=False),
            "id=1 set @home": dict(is_condition=True),
            "@home set bla": dict(is_condition=False),
            "@home set bla": dict(is_condition=True),
        }.items():
            with self.subTest(
                f"from_strings({cmdline!r}, **{kwargs}) should raise an exception"
            ):
                with self.assertRaises(
                    ValueError,
                    msg=f"from_strings({cmdline!r}) should raise an exception but didn't!",
                ):
                    Token.from_strings(shlex.split(cmdline), **kwargs)

    def test_split_by_trigger(self):
        tokens = Token.from_strings("orphan set work @home where a=b", reduce=False)
        self.assertEqual(
            Token.split_by_trigger(
                tokens, ConditionFollowingKeyword, ActionFollowingKeyword
            ),
            [
                [SetField("a", {"b"})],
                [AddToField("tag", {"work"}), SetField("location", {"home"})],
                [AddToField("tag", {"orphan"})],
            ],
        )

    def test_split_by_trigger_allow_repeat(self):
        for cmdline in f"""
            set work where a set bla
            set where set
            where set where
        """.strip().splitlines():
            tokens = Token.from_strings(cmdline, reduce=False)
            with self.assertRaises(ValueError):
                Token.split_by_trigger(
                    tokens, ConditionFollowingKeyword, ActionFollowingKeyword
                )

    def test_sort_into(self):
        self.maxDiff = None
        tokens = Token.from_strings(
            "10:00 until 2023-01-01T01:00 bla=blubb .open @home if", reduce=False
        )
        times, modifiers, properties, unknown = Token.sort_into(
            tokens, TimeToken, FieldModifier, Property
        )
        self.assertSequenceEqual(
            times,
            [
                Time(dt.now().replace(hour=10, minute=0, second=0, microsecond=0)),
                TimeKeywordUntil("until"),
                Time(dt(2023, 1, 1, 1)),
            ],
        )
        self.assertSequenceEqual(
            modifiers, [SetField("bla", {"blubb"}), SetField("location", {"home"})]
        )
        self.assertSequenceEqual(properties, [Property("open")])
        self.assertSequenceEqual(unknown, [ConditionFollowingKeyword()])


class EventTest(TestCase):
    def test_apply(self):
        for before, changes, after in [
            ("work at 10:00", "2h", "work 10 - 12"),
            ("bla", "tag-=bla @home", "@home"),
            ("work @home since 10", "end=12", "work @home 10 - 12"),
        ]:
            with self.subTest(
                f"An event made with {before!r} should be like {after!r} after applying {changes!r}"
            ):
                event1 = Event.from_cli(before)
                event1.apply(Token.from_strings(changes, is_condition=False))
                event2 = Event.from_cli(after)
                self.assertEqual(event1, event2)

    def test_to_dict(self):
        self.assertDictEqual(
            Event.from_cli(
                "2024-01-01T00:00+0100 2024-01-01T12:00+0100 work @home"
            ).to_dict(),
            {
                "id": None,
                "paths": set(),
                "key": None,
                "fields": {
                    "start": {"2023-12-31T23:00:00+0000"},
                    "end": {"2024-01-01T11:00:00+0000"},
                    "tag": {"work"},
                    "location": {"home"},
                },
            },
        )

    def test_parse_date(self):
        for string, shouldbe in {
            "y15:00": today(hour=15) - days(1),
            "t1:00": today(hour=1) + days(1),
            "yt1:00": today(hour=1),
            "yytt14:00": today(hour=14),
            "ytt00": today(hour=0) + days(1),
            (s := "2023-01-01T13:00"): dt.fromisoformat(s),
            "2023-01-01 1300": dt(2023, 1, 1, 13),
            "2023-01-01T13:00+0100": dt(
                2023, 1, 1, 13, tzinfo=timezone(timedelta(seconds=3600))
            ),
        }.items():
            with self.subTest(string=string, shouldbe=shouldbe):
                self.assertEqual(
                    (d := Event.parse_date(string)),
                    shouldbe,
                    msg=f"\nEvent.parse_date({string!r}) should be {shouldbe} but is instead {d}",
                )

    def test_from_cli(self):
        now = dt.now().replace(microsecond=0)
        today10 = now.replace(hour=10, minute=0, second=0)
        for cmdline, shouldhave in {
            "10min": dict(start=now - td(minutes=10), end=now),
            "bla=blubb": dict(fields={"bla": {"blubb"}}),
            "@home until now": dict(end=now, fields={"location": {"home"}}),
            "meeting since 10 @office": dict(
                start=today10,
                fields={"tag": {"office"}, "location": {"office"}},
            ),
            "explosion at 10:00": dict(
                start=today10, end=today10, fields={"tag": {"explosion"}}
            ),
            "explosion at 10": dict(
                start=today10, end=today10, fields={"tag": {"explosion"}}
            ),
        }.items():
            with self.subTest(f"Event.from_cli({cmdline!r}) should have {shouldhave}"):
                event = Event.from_cli(cmdline)
                for attr, shouldbe in shouldhave.items():
                    value = getattr(event, attr)
                    match attr, shouldbe:
                        case _, datetime():
                            self.assertLess(
                                abs(
                                    value.astimezone() - shouldbe.astimezone()
                                ).total_seconds(),
                                5,
                                msg=f"Event.from_cli({cmdline!r}) should have {attr} close to {shouldbe}, but is instead {value}",
                            )
                        case "fields", dict():
                            self.assertEqual(
                                (
                                    stripped := {
                                        k: v
                                        for k, v in shouldbe.items()
                                        if k not in "start end".split()
                                    }
                                ),
                                shouldbe,
                                msg=f"Event.from_cli({cmdline!r}) should have {attr} = {shouldbe}, but is instead {value} (stripped to {stripped})",
                            )
                        case _:
                            self.assertEqual(
                                value,
                                shouldbe,
                                msg=f"Event.from_cli({cmdline!r}) should have {attr} = {shouldbe}, but is instead {value}",
                            )

    def test_parse_date_now(self):
        self.assertLess(Event.parse_date("now") - dt.now(), timedelta(seconds=10))

    def test_to_from_cli_idempotent(self):
        for cmdline in (
            "person=me work",
            "[10:20]",
            "10:00 until 12:00 work @home",
            "10min",
            "10min ago",
            "10min ago until now",
            "10min since now",
            "10min since 30min ago work @home",
        ):
            with self.subTest(cmdline=cmdline):
                e1 = Event.from_cli(shlex.split(cmdline))
                e2 = Event.from_cli(e1.to_cli())
                self.assertEqual(e1, e2)

    def test_equality(self):
        def test(method, e1, e2):
            method(e1, e2)
            method(e2, e1)

        test(self.assertEqual, Event(), Event())
        test(self.assertNotEqual, Event(), Event(fields=dict(bla=set(["blubb"]))))
        test(
            self.assertEqual,
            Event(fields=dict(bla=set(["blubb"]))),
            Event.from_cli(["bla=blubb"]),
        )

    def test_matches(self):
        for evcli, query, match in [
            ("@home", "@home", True),
            ("today", "this hour", True),
            ("with=me", "with=you", False),
            ("with=me with=you", "with=you", True),
            ("2024-04-01T10:00 since 1h", "2024", True),
            ("2024-04-01T10:00 since 1h", "2024", True),
            ("todo todo=1", "todo", True),
            ("todo=1", "todo", True),
            ("todo=1", "bla", False),
            ("now", "1 week ago", True),
            ("tomorrow", "1 week ago", True),
            ("tomorrow", "1 week ago - now", False),
            ("7 days ago", "last week", True),
            ("tomorrow", "last week", False),
            ("now - now", ".open", False),
            ("now - ", ".open", True),
            ("- now", ".open", True),
            ("- now", ".openend", False),
            ("- now", ".openstart", True),
            ("since 10", ".openstart", False),
            ("since 10", ".openend", True),
            ("10:00", ".open", False),
            ("10:00", ".closed", False),
            ("10:00 - 12", ".closed", True),
            ("10:00", ".timepoint", True),
        ]:
            with self.subTest(
                f"{evcli!r} {'should' if match else 'should not'} match query {query!r}"
            ):
                event = Event.from_cli(shlex.split(evcli))
                querytokens = Token.from_strings(shlex.split(query), is_condition=True)
                self.assertEqual(event.matches(querytokens), match)


if __name__ == "__main__":
    unittest.main()
