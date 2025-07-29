[![coverage report](https://gitlab.com/nobodyinperson/annextimelog/badges/main/coverage.svg)](https://gitlab.com/nobodyinperson/annextimelog/-/commits/main)
[![PyPI version](https://badge.fury.io/py/annextimelog.svg)](https://badge.fury.io/py/annextimelog)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/nobodyinperson/annextimelog)](https://api.reuse.software/info/gitlab.com/nobodyinperson/annextimelog)

> ⚠️  This tool is in alpha stage. The most basic time tracking features recording, deletion, editing, search as well as syncing are implemented, but a lot of features (especially nice visual summaries) are missing.

![[annextimelog workflow terminal screenshot](https://fosstodon.org/@nobodyinperson/111772833299502409)](https://cdn.fosstodon.org/media_attachments/files/111/772/809/056/293/179/original/8d46177b3fbc9a0f.png)

# `annextimelog` - ⏱️ [Git Annex](https://git-annex.branchable.com)-backed Time Tracking

This is a brainstorm for a [Git Annex](https://git-annex.branchable.com)-backed time tracker.
The idea originated across some of my Mastodon threads:

- https://fosstodon.org/@nobodyinperson/109596495108921683
- https://fosstodon.org/@nobodyinperson/109159397807119512
- https://fosstodon.org/@nobodyinperson/111591979214726456

The gist is that I was (and still am) unhappy with the existing time tracking solutions. I worked with [hledger's timeclock](https://hledger.org/1.32/hledger.html#timeclock-format) and [timewarrior](https://timewarrior.net/) each for quite some time and built my own workflow and scripts around them.

## ✅ Requirements

Over the years, the below features turned out to be **my** personal requirements for a time-tracking system (**TL;DR**: easy and intuitive recording, hassle-free syncing, data export for further analysis).
Here is a table comparing annextimelog with [timewarrior](https://timewarrior.net/) and [hledger timeclock](https://hledger.org/1.32/hledger.html#timeclock-format):

✅ = feature available, 🟡 = partly available, ❌ = not available

| feature                                            | `timewarrior` | `hledger` timeclock    | `annextimelog`                       |
|----------------------------------------------------|---------------|------------------------|--------------------------------------|
| precise **start and end times**                    | ✅            | ✅                     | ✅ as git-annex metadata             |
| tracking of overlapping/simultaneous periods       | ❌            | 🟡 (separate files)    | ✅ backend can do it                 |
| nice, colourful, **graphical summary**             | ✅            | 🟡                     | ✅ with Python `rich`, more planned  |
| **plain text** data storage                        | ✅            | ✅                     | 🟡 buried in `git-annex` branch      |
| git-friendly, **merge conflict free data format**  | 🟡¹           | 🟡¹                    | ✅ git-annex’ own merge strategy     |
| arbitrary **tags** attachable to tracked periods   | ✅            | 🟡 hledger tags²       | ✅ just git-annex metadata           |
| arbitrary **notes** attachable to tracked periods  | 🟡³           | 🟡 hledger tags²       | ✅ just git-annex metadata           |
| tags can have **values**                           | ❌            | ✅ hledger tags²       | ✅ just git-annex metadata           |
| **files** attach-/linkable to tracked periods      | ❌            | 🟡 path as `file:` tag | 🟡 annexed files, linking is planned |
| **cli** to start, stop, edit, etc. tracked periods | ✅⁴           | ❌ own scripts needed  | 🟡 recording and editing             |
| **plugin system**                                  | 🟡⁵           | 🟡⁶ (hledger’s own)    | ❌ git-style plugin system planned   |
| **data export** to common format                   | ✅ (JSON)     | ✅ (CSV, JSON)         | ✅ as timeclock, JSON, cli commands  |
| **syncing** functionality built-in                 | ❌            | ❌                     | ✅ git-annex’s purpose is syncing    |
| **multi-user** support                             | ❌            | ❌                     | ✅ nothing in the way, just use tags |

¹last line is always modified, merge conflicts can arise when working from different machines

²[hledger tags](https://hledger.org/1.32/hledger.html#tags) have limitations, e.g. no spaces, colons, commas, etc.

³timewarrior annotations can't contain newlines for example. I wrote an extension to edit your annotation in your `$EDITOR` and optionally GPG-encrypt it, which lets you add newlines. Quite an inconvenience.

⁴timewarrior’s cli has some nasty inconveniences (e.g. no shortcut for ‘yesterday’, must painfully type out the full date, no intelligence to operate only on yesterday, gets confused and errors out in certain combinations of start/end times, etc…)

⁵timewarrior extensions ([here mine](https://gitlab.com/-/snippets/2498711)) are just fed the data via STDIN, not other command-line arguments. Not as useful as the git-style plugin system.

⁶for the analysis part, `hledger` plugins can be used. But as there is no actual cli to manage the data, there’s no plugin system for that.

## 🛠️ Implementation

To learn more about how `annextimelog` works under the hood with git-annex as backend, have a look at [doc/implementation](doc/implementation.md).

## 📦 Installation

You can run this tool if you have [nix](https://nixos.org) installed:

```bash
# drop into a temporary shell with the command available
nix shell gitlab:nobodyinperson/annextimelog

# install it
nix profile install gitlab:nobodyinperson/annextimelog
```

On Arch Linux you can install from the [AUR](https://aur.archlinux.org/packages/annextimelog) with your favorite helper, or directly with pacman from [this user repository](https://wiki.archlinux.org/title/Unofficial_user_repositories#alerque).

```bash
# use an AUR helper to install
paru -S annextimelog
```

Otherwise, you can install it like any other Python package, e.g. with `pip` or better `pipx`:

```bash
pipx install annextimelog

# latest development version
pipx install git+https://gitlab.com/nobodyinperson/annextimelog
```

Note that in this case you will need to install [git-annex](https://git-annex.branchable.com) manually.

Any of the above makes the `annextimelog` (or `atl`) command available.

## ❓ Usage

```bash
usage: annextimelog [-h] [--no-config] [-c key=value] [--repo REPO] [-n]
                    [--force] [-v] [-q] [-O {rich,console,json,timeclock,cli}]
                    [--version | --version-only]
                    {test,git,config,sync,sy,track,tr,delete,del,rm,remove,edit,ed,mod,change,upd,update,stop,cont,summary,su,ls,list,find,search}
                    ...

⏱️ Time tracker based on Git Annex

options:
  -h, --help            show this help message and exit
  --no-config           Ignore config from git
  -c key=value          Set a temporary config 'key=value' or just 'key' (implicit '=true'). If not present, 'annextimelog.' will be prepended to the key. The following keys are available: emojis, color, commit, confirm, fast, weekstartssunday, longlist, listall, matchconditions, outputformat, dryrun, slowdown.
  --force               Just do it. Ignore potential data loss.
  --version             show version information and exit
  --version-only        show only version and exit

Data:
  --repo REPO           Backend repository to use. Defaults to $ANNEXTIMELOGREPO, $ANNEXTIMELOG_REPO or $XDG_DATA_HOME/annextimelog (currently: /home/yann/.local/share/annextimelog)
  -n, --dry-run         don't actually store, modify or delete events in the repo. Useful for testing what exactly commands would do.Note that the automatic repo creation is still performed.

Output:
  Options changing output behaviour

  -v, --verbose         verbose output. More -v ⮕ more output
  -q, --quiet           less output. More -q ⮕ less output
  -O {rich,console,json,timeclock,cli}, --output-format {rich,console,json,timeclock,cli}
                        Select output format. Defaults to 'console'.

Subcommands:
  {test,git,config,sync,sy,track,tr,delete,del,rm,remove,edit,ed,mod,change,upd,update,stop,cont,summary,su,ls,list,find,search}
    test                run test suite
    git                 Access the underlying git repository
    config              Convenience wrapper around 'atl git config [annextimelog.]key [value], e.g. 'atl config emojis false' will set the annextimelog.emojis config to false.
    sync (sy)           sync data
    track (tr)          record a time period
    delete (del, rm, remove)
                        delete an event
    edit (ed, mod, change, upd, update)
                        modify an event
    stop                set end of seleted currently open-end events to now
    cont                continue a closed event now or at a given time
    summary (su, ls, list, find, search)
                        show a summary of tracked periods

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
> atl config color ... # whether colored output should be used. The default 'true' decides based on the typical $TERM and $NO_COLOR envvars.
> atl config commit ... # whether events should be committed upon modification. Setting this to false can improve performance but will reduce granularity to undo changes. 
> atl config confirm ... # whether to ask before actually touching anything
> atl config dryrun ... # equivalent of -n / --dry-run
> atl config emojis ... # whether emojis should be shown in pretty-formated event output
> atl config fast ... # setting this to false will cause annextimelog be be more sloppy (and possible faster) by leaving out some non-critical cleanup steps. 
> atl config listall ... # equivalent of specifying --all (e.g. atl ls -a)
> atl config longlist ... # equivalent of specifying --long (e.g. atl ls -l)
> atl config matchconditions ... # equivalent of atl ls --match (set to 'all' or 'any')
> atl config outputformat ... # equivalent of -O / --output-format
> atl config slowdown ... # a float value like 0.1 (ms) to make finding events *even* slower 😅 (for debugging purposes)
> atl config weekstartssunday ... # whether the week should start on Sunday instead of Monday (the default)
```

## 🛠️ Development

This project uses [poetry](https://python-poetry.org/), so you can run the following in this repository to get into a development environment:

```bash
poetry install
poetry shell
# now you're in a shell with everything set up
```

Other:

```bash
# Auto-run mypy when file changes:
just watch-mypy

# Auto-run tests when file changes:
just watch-test

# Test how a sequence of command-line args is interpreted as event metadata
just test-tokens work @home note=bla myfield+=one,two,three 2h ago until now

# Run tests against a different Python version
just test-with-python-version 3.10
```

