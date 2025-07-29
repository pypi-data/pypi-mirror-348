# system modules
import time
from fnmatch import fnmatchcase
import warnings
from datetime import date
import unittest
import copy
import itertools
import glob
import collections
import uuid
import os
import json
import re
import textwrap
import sys
import shlex
import logging
import subprocess
import argparse
from collections import defaultdict
from typing import List, Dict, Set, Optional, Sequence, Tuple
from pathlib import Path
import importlib.metadata

# internal modules
from annextimelog.repo import Event, AnnextimelogRepo
from annextimelog.log import stdout, stderr, setup_logging, setup_locale
from annextimelog.run import run
from annextimelog.token import *
from annextimelog import utils
from annextimelog.utils import Range, RangeMerger
from annextimelog.datetime import datetime, datetime as dt, timedelta, timedelta as td

# external modules
import rich
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.table import Table
from rich.pretty import Pretty
from rich.text import Text
from rich import box

logger = logging.getLogger(__name__)


def test_cmd_handler(args, other_args):
    loader = unittest.TestLoader()
    logger.debug(f"🧪 Importing test suite")
    import annextimelog.test

    logger.info(f"🚀 Running test suite")
    testsuite = loader.loadTestsFromModule(annextimelog.test)
    result = unittest.TextTestRunner(
        verbosity=args.test_verbosity, buffer=args.test_verbosity <= 2
    ).run(testsuite)
    logger.debug(f"{result = }")
    if result.wasSuccessful():
        logger.info(f"✅ Test suite completed successfully")
    else:
        logger.error(f"💥 There were problems during testing.")
        sys.exit(1)


def git_cmd_handler(args, other_args):
    result = args.repo.run_git(subprocess.Popen, other_args)
    result.wait()
    sys.exit(result.returncode)


def config_cmd_handler(
    args: argparse.Namespace, other_args: Optional[List[str]] = None
):
    git_config_args = [
        (
            re.sub(r"^(annextimelog\.)?", "annextimelog.", a)
            if a in AnnextimelogRepo.ANNEXTIMELOG_CONFIG_KEYS
            else a
        )
        for a in (other_args or [])
    ]
    result = args.repo.run_git(subprocess.Popen, ["config"] + git_config_args)
    result.wait()
    sys.exit(result.returncode)


def sync_cmd_handler(args, other_args):
    sys.exit(0 if args.repo.sync(other_args) else 1)


def track_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    try:
        event = args.repo.Event.from_cli(args.metadata)
    except ValueError as e:
        logger.critical(f"Invalid metadata {shlex.join(args.metadata)!r}: {e}")
        sys.exit(1)
    if not (event.start or event.end):
        logger.debug(f"Event is fully open. Let's start it now.")
        event.start = dt.now()
    if logger.getEffectiveLevel() < logging.DEBUG:
        logger.debug(f"Event before saving:")
        stderr.print(event.to_rich())
    stderr.print(event.to_rich())
    if args.dry_run:
        logger.info(f"--dry-run was given, so this new event is not stored.")
        return
    event.store()


def summary_cmd_handler(
    args: argparse.Namespace, other_args: Optional[List[str]] = None
):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    query = getattr(
        args,
        "query",
        (
            default := (
                []
                if args.repo.config.get("annextimelog.listall", "false") == "true"
                else ["today"]
            )
        ),
    )
    kwargs = dict(is_condition=True)
    try:
        if not (tokens := Token.from_strings(query, config=args.repo.config, **kwargs)):
            logger.debug(f"No query tokens, using current day as constraint")
            tokens = Token.from_strings(default, config=args.repo.config, **kwargs)
    except ValueError as e:
        logger.critical(f"Invalid query {shlex.join(query)!r}: {e}")
        sys.exit(1)
    logger.debug(f"atl ls: {tokens = }")
    events = sorted(
        args.repo.find_events(tokens),
        key=lambda e: e.end or e.start or dt.now().astimezone(),
    )

    if getattr(args, "id_only", None):
        for event in events:
            stdout.out(event.id)
        return

    total_seconds: float = 0
    closed_events: List[Event] = []
    open_events: List[Event] = []
    touched_days: Set[date] = set()
    rangeMerger = utils.RangeMerger()
    for event in events:
        start = event.start or dt.now().astimezone()
        end = event.end or dt.now().astimezone()
        rangeMerger.add(Range(start, end))
        if start and end:
            total_seconds += abs((end - start).total_seconds())
            closed_events.append(event)
            startdate = day = start.astimezone().date()
            enddate = ((end or dt.now()) - td(microseconds=1)).date()
            while day <= enddate:
                touched_days.add(day)
                day += td(days=1)
        if not (start and end):
            open_events.append(event)
        event.output(args)
    if total := rangeMerger.total:
        nonoverlap_seconds = total.total_seconds()  # type: ignore[attr-defined]
    else:
        nonoverlap_seconds = 0
    logger.info(
        f"Found {len(events)} events spanning {len(rangeMerger.ranges)} disjunct time ranges with a total non-overlapping time of {td(seconds=nonoverlap_seconds).pretty_duration(units='h')} ({td(seconds=total_seconds).pretty_duration(units='h')} double-counting overlaps), touching {len(touched_days)} days."
    )


def edit_cmd_handler(
    args: argparse.Namespace,
    other_args: Optional[List[str]] = None,
    tokens: Optional[Sequence[Token]] = None,
):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    if tokens:
        logger.debug(
            f"Using tokens {Token.join(tokens)!r} instead of {shlex.join(args.query)!r} to modify events"
        )
    else:
        try:
            logger.debug(f"Interpreting query {shlex.join(args.query)!r}")
            tokens = [
                t for t in Token.from_strings(args.query, config=args.repo.config) if t
            ]
        except ValueError as e:
            if logger.getEffectiveLevel() <= logging.DEBUG:
                logger.critical(f"Invalid query {shlex.join(args.query)!r}: {e}")
            logger.critical(
                f"To edit events, the query must contain matching conditions and modification sequences, "
                f"Your query {shlex.join(args.query)!r} does not specify both (add some -vvvv for more info). "
                f"This usually means you need to add some 'if' before your conditions and/or 'set' before your modifications. "
                f"See the following examples:"
            )
            stderr.log(
                Syntax(
                    textwrap.dedent(
                        f"""
            atl edit note="My note" where id=asdf # set note for event 'asdf'
            atl edit @home if location= yesterday # set location to 'home' for all events yesterday that have none set
            atl edit this week set project=secret @work # set location to 'work' and project=secret for all events in this week
            """
                    ).strip(),
                    "bash",
                )
            )
            sys.exit(1)
    conditions: List[Token] = []
    actions: List[Token] = []
    for token in tokens:
        match token:
            case Token(is_condition=True):
                conditions.append(token)
            case Token(is_condition=False):
                actions.append(token)
            case _:
                logger.warning(f"Ignoring {token!r}")
    if not actions:
        logger.info(
            f"No actions to perform for events matching {Token.join(conditions)!r}. "
        )
        return
    if conditions:
        if args.allow_edit_all:
            logger.warning(
                f"Ignoring --all as you also gave {len(conditions)} conditions ({Token.join(conditions)!r})"
            )
    elif not args.allow_edit_all:
        logger.critical(
            f"No conditions given to update with {Token.join(actions)!r}. "
            f"If you really want to process all events, specify --all"
        )
        return
    logger.info(
        f"atl edit: Will modify events matching {Token.join(conditions)!r} with {Token.join(actions)!r}"
    )
    events = list(args.repo.find_events(conditions))
    changed_events: List[Event] = []
    for event in events:
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(
                f"Event matching {Token.join(conditions)!r} before applying {Token.join(actions)!r}"
            )
            stderr.log(event.to_rich())
        changed_event = copy.deepcopy(event)
        changed_event.apply(actions)
        if event == changed_event:
            if logger.getEffectiveLevel() < logging.INFO or args.dry_run:
                logger.info(
                    f"Event {event.id} {event.title or 'untitled'!r} didn't change when applying {Token.join(actions)!r}"
                )
            continue
        if (
            args.repo.config.get("annextimelog.confirm", "true") == "true"
            or args.dry_run
            or logger.getEffectiveLevel() < logging.INFO
        ):
            logger.info(
                f"{'Unsaved changes' if args.dry_run else 'Changes'} to {event.id} "
                f"(which matches {Token.join(conditions)!r}) after applying {Token.join(actions)!r}:"
            )
            stderr.print(event.compare_to(changed_event))
        else:
            stderr.print(changed_event.to_rich())
        if args.dry_run:
            continue
        if changed_event.store():
            changed_events.append(changed_event)
        else:
            stderr.print()
    logger.info(f"{len(changed_events)} events were touched")


def stop_cmd_handler(args: argparse.Namespace, other_args: Optional[List[str]] = None):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    tokens = [t for t in Token.from_strings(args.query, reduce=False) if t]
    timetokens, other = Token.sort_into(tokens, TimeToken)  # type: ignore[type-abstract]
    logger.debug(f"{timetokens = }")
    logger.debug(f"{other = }")
    try:
        actions = list(Token.reduce(timetokens, is_condition=False))
    except ValueError as e:
        logger.critical(
            f"While interpreting {Token.join(timetokens)!r} as stopping time for open events matching {Token.join(other)!r}: {e}"
        )
        sys.exit(1)
    actions_: List[Token] = []
    match actions:
        case [Duration()]:
            actions_.extend(actions)
        case []:
            actions_.append(TimeEnd(time=dt.now()))
        case [Time(time=t) as tt]:
            actions_.append(TimeEnd(string=tt.string, time=t))
        case [TimeFrame(start=start, end=end) as tt]:
            actions_.append(TimeEnd(time=end or start or dt.now()))
        case _:
            logger.critical(
                f"Don't know how to interpret {Token.joinpretty(actions)} as end for open events matching {Token.join(other)!r}"
            )
            sys.exit(1)
    actions = [t.evolve(is_condition=False) for t in actions_]
    conditions = [t.evolve(is_condition=True) for t in other]
    logger.debug(f"{conditions = }")
    logger.debug(f"{actions = }")
    return edit_cmd_handler(
        args=args,
        tokens=[t for t in Token.from_strings(".openend", is_condition=True) if t]
        + conditions
        + actions,
    )


def continue_cmd_handler(
    args: argparse.Namespace, other_args: Optional[List[str]] = None
):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    tokens = [t for t in Token.from_strings(args.query, reduce=False) if t]
    actiontokens, othertokens = Token.split_by_trigger(tokens, ActionFollowingKeyword)
    timeactiontokens, conditions = Token.sort_into(othertokens, TimeToken)  # type: ignore[type-abstract]
    logger.debug(f"{timeactiontokens = }")
    logger.debug(f"{conditions = }")
    try:
        timeactions_ = list(Token.reduce(timeactiontokens, is_condition=False))
    except ValueError as e:
        logger.critical(
            f"While interpreting {Token.join(timeactiontokens)!r} as starting time for continuing events matching {Token.join(conditions)!r}: {e}"
        )
        sys.exit(1)
    timeactions: List[Token] = []
    now = dt.now()
    match timeactions_:
        case []:
            timeactions.append(TimeFrame(start=now))
        case [Time(time=t) as tt]:
            timeactions.append(TimeFrame(start=t))
        case [TimeFrame(start=start, end=end) as tt] if not start:
            timeactions.append(tt.evolve(start=now))
        case [TimeFrame(start=start, end=end) as tt]:
            timeactions.append(tt)
        case [Duration(duration as d)]:
            timeactions.append(TimeFrame(start=now, end=now + d))
        case _:
            logger.critical(
                f"Don't know how to interpret {Token.joinpretty(timeactions_)} "
                f"(from {Token.join(timeactiontokens)!r}) as start for continuing events matching {Token.join(conditions)!r}"
            )
            sys.exit(1)
    actions = [t.evolve(is_condition=False) for t in timeactions] + actiontokens
    conditions = [t.evolve(is_condition=True) for t in conditions]
    logger.debug(f"{conditions = }")
    logger.debug(f"{actions = }")
    matching_closed_events = list(
        args.repo.find_events(
            [t for t in Token.from_strings(".closed", is_condition=True) if t]
            + conditions
        )
    )
    logger.debug(
        f"Found {len(matching_closed_events)} closed events matching {Token.join(conditions)!r}"
    )
    past_events = [
        e
        for e in matching_closed_events
        if all(t <= dt.now().astimezone() for t in (e.start, e.end) if t)
    ]
    logger.debug(
        f"Of the {len(matching_closed_events)} closed events matching {Token.join(conditions)!r}, {len(past_events)} are in the past"
    )
    latest_events = sorted(
        past_events, key=lambda e: e.start or e.end or dt.now(), reverse=True
    )
    if event := next(iter(latest_events), None):
        newevent = event.evolve(id=None, paths=set())
        newevent.start = dt.now()
        newevent.end = None
        newevent.apply(actions)
    else:
        metadata = actions + conditions
        logger.info(
            f"Didn't find an closed past event matching {Token.join(conditions)!r}. Making a new one with {Token.join(metadata)!r} instead."
        )
        newevent = args.repo.Event()
        newevent.apply(metadata)
    stderr.print(newevent.to_rich())
    if args.dry_run:
        logger.info(f"--dry-run was given, so this new event is not stored.")
        return
    newevent.store()


def delete_cmd_handler(
    args: argparse.Namespace, other_args: Optional[List[str]] = None
):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    kwargs = dict(is_condition=True)
    try:
        tokens = Token.from_strings(args.query, config=args.repo.config, **kwargs)
    except ValueError as e:
        logger.critical(f"Invalid query {shlex.join(args.query)!r}: {e}")
        sys.exit(1)
    logger.debug(f"atl del: {tokens = }")
    events = list(args.repo.find_events(tokens))
    if not events:
        return
    logger.info(f"Will delete these {len(events)} events:")
    for event in events:
        stderr.print(event.to_rich())
    if args.dry_run:
        logger.info(f"--dry-run: not deleting the above events")
        return
    logger.info(f"Deleting the above {len(events)} events")
    args.repo.delete(events)


def key2value(x: str) -> Tuple[str, str]:
    if m := AnnextimelogRepo.GIT_CONFIG_REGEX.fullmatch(x):
        key, value = m.groups()
        if key not in AnnextimelogRepo.ANNEXTIMELOG_CONFIG_KEYS:
            logger.warning(f"{key!r} (from {x!r}) is not an annextimelog config key")
        if not value:
            value = "true"
        return key, value
    else:
        raise argparse.ArgumentTypeError(f"{x!r} is not a key=value pair")


def add_common_arguments(parser):
    # TODO return/yield new groups?
    datagroup = parser.add_argument_group(title="Data")
    datagroup.add_argument(
        "--repo",
        type=Path,
        default=(default := AnnextimelogRepo.DEFAULT_PATH),
        help=f"Backend repository to use. "
        f"Defaults to $ANNEXTIMELOGREPO, $ANNEXTIMELOG_REPO or $XDG_DATA_HOME/annextimelog (currently: {str(default)})",
    )
    datagroup.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="don't actually store, modify or delete events in the repo. "
        "Useful for testing what exactly commands would do."
        "Note that the automatic repo creation is still performed.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Just do it. Ignore potential data loss.",
    )
    outputgroup = parser.add_argument_group(
        title="Output", description="Options changing output behaviour"
    )
    outputgroup.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbose output. More -v ⮕ more output",
    )
    outputgroup.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="less output. More -q ⮕ less output",
    )
    outputgroup.add_argument(
        "-O",
        "--output-format",
        choices=("rich", "console", "json", "timeclock", "cli"),
        default=(default := "console"),  # type: ignore
        help=f"Select output format. Defaults to {default!r}.",
    )


configdoc = "\n".join(
    f"> atl config {key} ... # {desc}"
    for key, desc in sorted(AnnextimelogRepo.ANNEXTIMELOG_CONFIG_KEYS.items())
)

parser = argparse.ArgumentParser(
    description="⏱️ Time tracker based on Git Annex",
    epilog=textwrap.dedent(
        f"""
🛠️ Usage

Logging events:

> atl tr work @office                # an open event starting now
> atl tr work @office since 10:10    # an open event starting at a specific time
> atl tr work @office 10:10 -        # same (note the dash)
> atl stop work           # some time later, sets end of the latest 'work' event
> atl cont work           # next day, copy the latest work event and start it now
> atl tr work for 4h @home with client=smallcorp on project=topsecret    # a past event of 4h duration
> atl tr 10 - 11 @doctor  # at the doctor's for 1h
> atl tr 10:00 title="Note for 10 o'clock"  # record a time point
> atl tr y22:00 - 30min ago sleep @home quality=meh
> atl -vvv tr ... # debug problems

    Note: Common prepositions like 'with', 'about', etc. are ignored. See the full list with
    > python -c 'from annextimelog.token import Noop;print(Noop.FILLERWORDS)'

Listing events:

> atl
> atl ls
> atl ls .open      # list events that don't have both start and end set
> atl ls .openend   # list events that don't have an end set („currently running”)
> atl ls week
> atl ls yesterday
> atl ls until 2days ago
> atl -O json ls -a  # dump all data as JSON
> atl -O timeclock ls -a | hledger -f timeclock:- bal --daily   # analyse with hledger

Editing events:

> atl stop                               # stop all open-end events
> atl mod .openend set end=now           # same but manually
> atl mod id=jajekwka project=secret     # add custom tag to specific event
> atl mod id=LXKGrBGA end=now            # change end of specific event
> atl mod id=LXKGrBGA until 18           # change end of specific event
> atl mod @home where note=text          # add 'home' to location where note contains 'text'

Continuing events:

> atl cont work @office           # continues the last matching closed event as a new event
> atl cont work @office until 15  # same, but sets the end time to 15:00 today
> atl cont work set project=A     # continue and add/override metadata

Removing events:

> atl rm id=O3YzvZ4m   # delete by ID
> atl rm @work sleep   # delete all events where you slept at work 😉

Syncing:

# add a git remote of your choice
> atl git remote add git@gitlab.com:you/yourrepo
# sync up
> atl sync

Configuration

> atl -c key=value ... # temporarily set config
> atl config key value # permanently set config
{configdoc}

    """.strip()
    ),
    prog="annextimelog",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "--no-config",
    action="store_true",
    help="Ignore config from git",
)
parser.add_argument(
    "-c",
    dest="extra_config",
    action="append",
    metavar="key=value",
    type=key2value,
    help="Set a temporary config 'key=value' or just 'key' (implicit '=true'). "
    "If not present, 'annextimelog.' will be prepended to the key. "
    f"The following keys are available: {', '.join(AnnextimelogRepo.ANNEXTIMELOG_CONFIG_KEYS)}.",
    default=[],
)
add_common_arguments(parser)
versiongroup = parser.add_mutually_exclusive_group()
versiongroup.add_argument(
    "--version",
    action="store_true",
    help="show version information and exit",
)
versiongroup.add_argument(
    "--version-only",
    action="store_true",
    help="show only version and exit",
)


subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")
testparser = subparsers.add_parser(
    "test",
    help="run test suite",
    description="Run the test suite",
    formatter_class=argparse.RawTextHelpFormatter,
)
testparser.add_argument(
    "-v",
    "--verbose",
    dest="test_verbosity",
    help="Increase verbosity of test runner. "
    "-v: show test names, "
    "-vv: show raw debug output in all tests, not just failed tests. "
    "(Note that to set the debug level of annextimelog itself, you need to specify 'atl -vvvvv text -vv') ",
    action="count",
    default=1,
)
testparser.set_defaults(func=test_cmd_handler)
gitparser = subparsers.add_parser(
    "git",
    help="Access the underlying git repository",
    add_help=False,
    formatter_class=argparse.RawTextHelpFormatter,
)
gitparser.set_defaults(func=git_cmd_handler)
configparser = subparsers.add_parser(
    "config",
    help="Convenience wrapper around 'atl git config [annextimelog.]key [value], "
    "e.g. 'atl config emojis false' will set the annextimelog.emojis config to false.",
    add_help=False,
    formatter_class=argparse.RawTextHelpFormatter,
)
configparser.set_defaults(func=config_cmd_handler)
syncparser = subparsers.add_parser(
    "sync",
    help="sync data",
    description=textwrap.dedent(
        """
    Sync data with configured remotes by running 'git annex assist'.
    """
    ).strip(),
    aliases=["sy"],
)
add_common_arguments(syncparser)
syncparser.set_defaults(func=sync_cmd_handler)
trackparser = subparsers.add_parser(
    "track",
    help="record a time period",
    description=textwrap.dedent(
        """
    Record a time with metadata.

    Example:

    > atl tr y22  800 work python @home ="annextimelog dev" :"working on cli etc." project=annextimelog project+=timetracker

    """
    ).strip(),
    aliases=["tr"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(trackparser)
trackparser.add_argument(
    "metadata",
    nargs="+",
    help=textwrap.dedent(
        """
    Examples:

        10:00                   10:00 today
        y15:00                  15:00 yesterday
        yy15:00                 15:00 the day before yesterday
        t20:00                  20:00 tomorrow
        tt20:00                 20:00 the day after tomorrow
        2023-12-04
        2023-12-04T13:15
        justaword               adds tag 'justaword'
        "with space"            (shell-quoted) adds tag "with space"
        field=value             sets metadata field 'field' to (only) 'value'
        field+=value            adds 'value' to metadata field
"""
    ).strip(),
)
trackparser.set_defaults(func=track_cmd_handler)
deleteparser = subparsers.add_parser(
    "delete",
    help="delete an event",
    description=textwrap.dedent(
        """
    Delete events matching a query similar to `atl ls`

    Example:

    # the following commands would delete event rejacisumuqedowe
    > atl del id=rejaci    # delete event with id containing string
    > atl del todo         # delete all events with a todo (tag or field)
    > atl delete yesterday # delete all events yesterday
    ...

    """
    ).strip(),
    aliases=["del", "rm", "remove"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(deleteparser)
deleteparser.add_argument("query", nargs="+")
deleteparser.set_defaults(func=delete_cmd_handler)
editparser = subparsers.add_parser(
    "edit",
    help="modify an event",
    description=textwrap.dedent(
        """
    Modify an event.
    """
    ).strip(),
    aliases=["ed", "mod", "change", "upd", "update"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(editparser)
editparser.add_argument("query", nargs="+")
editparser.add_argument(
    "-a",
    "--all",
    dest="allow_edit_all",
    help="Allow processing all events",
    action="store_true",
)
editparser.set_defaults(func=edit_cmd_handler)
stopparser = subparsers.add_parser(
    "stop",
    help="set end of seleted currently open-end events to now",
    description=textwrap.dedent(
        """
    Have selected currently open-end events stop now
    """
    ).strip(),
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(stopparser)
stopparser.add_argument("query", nargs="*")
stopparser.add_argument(
    "-a",
    "--all",
    dest="allow_edit_all",
    help="Allow processing all events",
    action="store_true",
)
stopparser.set_defaults(func=stop_cmd_handler)
contparser = subparsers.add_parser(
    "cont",
    help=(doc := "continue a closed event now or at a given time"),
    description=textwrap.dedent(
        f"""
    {doc}
    """
    ).strip(),
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(contparser)
contparser.add_argument("query", nargs="*")
contparser.set_defaults(func=continue_cmd_handler)
summaryparser = subparsers.add_parser(
    "summary",
    help="show a summary of tracked periods",
    description=textwrap.dedent(
        """
    List a summary of tracked periods

    The format matches the 'atl tr' syntax, e.g.:

    atl ls today # (the default)
    atl ls week
    atl ls month
    atl ls since 10min ago
    atl ls field=REGEX   # field has value matching a regular expression
    atl ls field=REGEX,REGEX,REGEX   # field has value matching any of the given regex
    atl ls @home last week
    atl ls .openend
    ...
    """
    ).strip(),
    aliases=["su", "ls", "list", "find", "search"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(summaryparser)
summaryparser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="list all events (unless another time period is given)",
)
summaryparser.add_argument("--match", choices="all any".split())
listgroup = summaryparser.add_mutually_exclusive_group()
listgroup.add_argument(
    "--id",
    "--id-only",
    dest="id_only",
    action="store_true",
    help="only print IDs of matched events",
)
listgroup.add_argument("-l", "--long", action="store_true", help="more details")
summaryparser.add_argument("query", nargs="*")
summaryparser.set_defaults(func=summary_cmd_handler)


def cli(cmdline: Sequence[str] = sys.argv[1:]):
    args, other_args = parser.parse_known_args(args=cmdline)

    setup_logging(level=logging.INFO - (args.verbose - args.quiet) * 5)
    setup_locale()

    if not sys.stdin.isatty():
        logger.warning(
            f"annextimelog's cli is not yet stable, be careful relying on it in scripts."
        )

    logger.debug(f"{args = }")
    logger.debug(f"{other_args = }")

    if args.version or args.version_only:
        version = importlib.metadata.version(package := "annextimelog")
        urls: Dict[str, str] = dict(
            utils.make_it_two(re.split(r"\s*,\s*", s, maxsplit=1))
            for s in (
                importlib.metadata.metadata("annextimelog").get_all("project-url") or []
            )
        )
        author = importlib.metadata.metadata("annextimelog")["Author"]
        logger.warning(
            f"The displayed version {version!r} does not (yet) reflect development commits made after the release, "
            f"if you installed {package} from {urls['Repository']}."
        )
        if args.version_only:
            stdout.out(version)
            sys.exit(0)
        stdout.print(
            textwrap.dedent(
                f"""
                {package} v[b]{version}[/b] - A cli time tracker based on Git Annex
                by [b]{author}[/b] ({urls['Author on Mastodon']})
                Source code: {urls['Repository']}
                Changelog: {urls['Changelog']}
            """
            ).strip("\r\n")
        )
        sys.exit(0)

    args.repo = AnnextimelogRepo(args.repo)

    if not args.repo.ensure_git():
        sys.exit(1)

    if not args.no_config:
        args.repo.read_config()

    # apply extra configs
    args.repo.config.update(
        {
            re.sub(r"^(annextimelog\.)?", "annextimelog.", k): v
            for k, v in args.extra_config
        }
    )
    if args.dry_run:
        args.repo.config["annextimelog.dryrun"] = "true"
    if getattr(args, "long", None):
        args.repo.config["annextimelog.longlist"] = "true"
    if getattr(args, "all", None):
        args.repo.config["annextimelog.listall"] = "true"
    if m := getattr(args, "match", None):
        args.repo.config["annextimelog.matchcondition"] = m

    if args.repo.config.get("annextimelog.color", "true") == "false":
        stdout.no_color = True
        stderr.no_color = True

    if not args.repo.ensure_git_annex():
        sys.exit(1)

    # ✅ at this point, args.repo is a git annex repository

    if args.repo.config.get("annextimelog.commit", "true") == "true":
        if args.subcommand not in ["git"]:
            if args.repo.dirty:
                logger.warning(
                    f"🐛 The repo {args.repo.path} is not clean. "
                    f"This should not happen. Committing away the following changes:"
                )
                result = args.repo.run_git(subprocess.Popen, ["status"])
                with stderr.status("Committing..."):
                    result = args.repo.run_git(subprocess.run, ["annex", "add"])
                    result = args.repo.run_git(subprocess.run, ["add", "-A"])
                    result = args.repo.run_git(
                        subprocess.run,
                        ["commit", "-m", "🧹 Leftover changes"],
                    )
                result = args.repo.run_git(subprocess.run, ["status", "--porcelain"])
                if not (result.returncode or result.stderr):
                    logger.info(f"✅ Repo is now clean")
                else:
                    logger.warning(f"Commiting leftover changes didn't work.")

    # handle the subcommand
    # (when a subcommand is specified, the 'func' default is set to a callback function)
    if not getattr(args, "func", None):
        # default to 'atl summary'
        args.func = summary_cmd_handler
    try:
        args.func(args, other_args)
    finally:
        if (
            args.subcommand not in ["git"]
            and args.repo.config.get("annextimelog.commit", "true") == "true"
        ):
            result = args.repo.run_git(subprocess.run, ["status", "--porcelain"])
            if result.returncode or result.stdout or result.stderr:
                logger.warning(
                    f"🐛 This command left the repo {args.repo.path} in an unclean state. "
                    f"This should not happen. Consider investigating. "
                    f"The next time you run any 'annextimelog' command, these changes will be committed."
                )
                result = args.repo.run_git(subprocess.Popen, ["status"])


if __name__ == "__main__":
    cli()
