from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import dataclasses
import math
import re
import json
import functools
import logging
from typing import Dict, Union, Literal, Sequence, Optional, Any, Iterator, Tuple


# external modules
from rich.text import Text


logger = logging.getLogger(__name__)


def make_it_n(items: Sequence, n: int, filler: Optional[Any] = None) -> Iterator:
    it = iter(items)
    for i in range(n):
        yield next(it, filler)


def make_it_two(items: Sequence, filler: Optional[Any] = None) -> Tuple[Any, Any]:
    it = iter(items)
    return next(it, filler), next(it, filler)


def sign(x: Union[float, int]) -> Union[Literal[-1, 1]]:
    return 1 if x >= 0 else -1


def from_jsonlines(string):
    if hasattr(string, "decode"):
        string = string.decode(errors="ignore")
    string = str(string or "")
    for i, line in enumerate(string.splitlines(), start=1):
        try:
            yield json.loads(line)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"line #{i} ({line!r}) is invalid JSON: {e!r}")
            continue


def as_regex(string: str, **kwargs):
    try:
        return re.compile(string, **kwargs)
    except Exception as e:
        logger.warning(f"Invalid regular rexpression {string!r}. Matching literally.")
        return re.compile(re.escape(string), **kwargs)


# TODO: How to type this correctly?
# Apparently there is no annotation for something 'Orderable' 🤔


@dataclasses.dataclass
class Range:
    start: object
    end: object

    def overlaps(self, other: Range) -> bool:
        return self.start <= other.end and other.start <= self.end  # type: ignore[operator]

    def extend(self, other: Range) -> Range:
        self.start = min(self.start, other.start)  # type: ignore[call-overload]
        self.end = max(self.end, other.end)  # type: ignore[call-overload]
        return self


@dataclasses.dataclass
class RangeMerger:
    ranges: list[Range] = dataclasses.field(default_factory=list)

    def add(self, newrg: Range):
        for rg in self.ranges:
            if rg.overlaps(newrg):
                rg.extend(newrg)
                return
        self.ranges.append(newrg)  # no overlap, start new range

    def collapse(self) -> RangeMerger:
        lastranges: list[Range] = []
        while (ranges := self.ranges.copy()) != lastranges:
            self.ranges.clear()
            for rg in ranges:
                self.add(rg)
            lastranges = ranges
        return self

    @property
    def total(self) -> object:
        self.collapse()
        if not self.ranges:
            return None
        return functools.reduce(
            lambda x, y: x + y, (rg.end - rg.start for rg in self.ranges)  # type: ignore[operator]
        )
