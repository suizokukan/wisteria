#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Linden Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Linden.
#    Linden is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Linden is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Linden.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    linden.py

- données à ajouter:
        RegularClass
        IntheritedList
        IntheritedDict
        ("R01:class::meta class", MetaClass),

        ("R02:class::reg. class::RegularClass()", RegularClass()),
        ("R03:class::reg. class::async method", RegularClass.async_method),
        ("R04:class::reg. class::generator", RegularClass.generator),
        ("R05:class::reg. class::method", RegularClass.method),
        ("R06:class::reg. class::class method", RegularClass.class_method),
        ("R07:class::reg. class::static method", RegularClass.static_method),

        ("Y01:collections.deque(empty)", collections.deque()),
        ("Y02:collections.deque", collections.deque((1, 2))),
        ("Y03:collections.defaultdict(empty)", collections.defaultdict()),
        ("Y04:collections.defaultdict", collections.defaultdict(None, {1: 2})),
        ("Y05:collections.OrderedDict(empty)", collections.OrderedDict()),
        ("Y06:collections.OrderedDict", collections.OrderedDict({1: 2})),
        ("Y07:collections.Counter(empty)", collections.Counter()),
        ("Y08:collections.Counter", collections.Counter((1, 2))),
        ("Y09:collections.ChainMap", collections.ChainMap()),
        ("Y10:collections.ChainMap", collections.ChainMap({1: 2}, {2: 3})),
        ("Y11:collections.abc.Awaitable", collections.abc.Awaitable),
        ("Y12:collections.abc.Coroutine", collections.abc.Coroutine),
        ("Y13:collections.abc.AsyncIterable", collections.abc.AsyncIterable),
        ("Y14:collections.abc.AsyncIterator", collections.abc.AsyncIterator),
        ("Y15:collections.abc.AsyncGenerator", collections.abc.AsyncGenerator),
        ("Y16:collections.abc.Reversible", collections.abc.Reversible),
        ("Y17:collections.abc.Container", collections.abc.Container),
        ("Y18:collections.abc.Collection", collections.abc.Collection),
        ("Y19:collections.abc.Callable", collections.abc.Callable),
        ("Y20:collections.abc.Set", collections.abc.Set),
        ("Y21:collections.abc.MutableSet", collections.abc.MutableSet),
        ("Y22:collections.abc.Sequence", collections.abc.Sequence),
        ("Y23:collections.abc.MutableSequence", collections.abc.MutableSequence),
        ("Y24:collections.abc.ByteString", collections.abc.ByteString),
        ("Y25:collections.abc.MappingView", collections.abc.MappingView),
        ("Y26:collections.abc.KeysView", collections.abc.KeysView),
        ("Y27:collections.abc.ItemsView", collections.abc.ItemsView),
        ("Y28:collections.abc.ValuesView", collections.abc.ValuesView),
        ("Y29:contextlib.AbstractContextManager", contextlib.AbstractContextManager),
        ("Y30:contextlib.AbstractAsyncContextManager", contextlib.AbstractAsyncContextManager),

        ("Z01:decimal.localcontext", decimal.localcontext()),

- transformer les print en logging.
"""
import argparse
import atexit
import configparser
import os
import re
import sys

from rich import print as rprint
import rich.table

import linden.globs
from linden.globs import REPORT_MINIMAL_STRING, REPORT_FULL_STRING
from linden.globs import TMPFILENAME, REGEX_CMP, REGEX_CMP__HELP
from linden.globs import VERBOSITY_MINIMAL, VERBOSITY_NORMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from linden.aboutproject import __projectname__, __version__


PARSER = \
    argparse.ArgumentParser(description="Comparisons of different Python serializers",
                            epilog=f"{__projectname__}: {__version__}",
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('--version', '-v',
                    action='version',
                    version=f"{__projectname__}: {__version__}",
                    help="Show the version and exit.")

PARSER.add_argument('--cmp',
                    action='store',
                    default="all vs all",
                    help=f"Comparisons details. Expected syntax: '{REGEX_CMP__HELP}'.")

PARSER.add_argument('--cfgfile',
                    action='store',
                    default="linden.ini",
                    help="config file to be used.")

PARSER.add_argument('--checkup',
                    action='store_true',
                    help="show installed serializers, current config file and exit")

PARSER.add_argument('--report',
                    action='store',
                    default="minimal",
                    help=f"Report format: 'minimal' (interpreted as '{REPORT_MINIMAL_STRING}'), "
                    f"'full' (interpreted as '{REPORT_FULL_STRING}'), "
                    "or a subset from this very last string, e.g. 'A;B1a;'. "
                    "Please notice that --verbosity has no effect upon --report.")

PARSER.add_argument('--verbosity',
                    type=int,
                    default=VERBOSITY_NORMAL,
                    choices=(VERBOSITY_MINIMAL,
                             VERBOSITY_NORMAL,
                             VERBOSITY_DETAILS,
                             VERBOSITY_DEBUG),
                    help="Verbosity level: 0(=minimal), 1(=normal), 2(=normal+details), 3(=debug). "
                    "Please notice that --verbosity has no effect upon --report.")

linden.globs.ARGS = PARSER.parse_args()

# ARGS.report interpretation:
if linden.globs.ARGS.report == "minimal":
    linden.globs.ARGS.report = REPORT_MINIMAL_STRING
    if linden.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        rprint(f"--report 'minimal' interpreted as '{linden.globs.ARGS.report}'.")
elif linden.globs.ARGS.report == "full":
    linden.globs.ARGS.report = REPORT_FULL_STRING
    if linden.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        rprint(f"--report 'full' interpreted as '{linden.globs.ARGS.report}'.")
elif not linden.globs.ARGS.report.endswith(";"):
    linden.globs.ARGS.report += ";"
    if linden.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        rprint(f"--report: semicolon added at the end; --report is now '{linden.globs.ARGS.report}'.")

# =============================================================================
# This point is only reached if there's no --version/--help argument
# on the command line.
# =============================================================================
ARGS = linden.globs.ARGS


# exit handler: let's remove the tmp file if it exists.
def exit_handler():
    """
        exit_handler()

        Remove the tmp file if it exists
    """
    if os.path.exists(TMPFILENAME):
        os.remove(TMPFILENAME)


atexit.register(exit_handler)


from linden.serializers import SERIALIZERS, SerializationResults


def read_cfgfile(filename):
    """
        read_cfgfile()

        Read the configuration file <filename>, return the corresponding dict.

        _______________________________________________________________________

        ARGUMENT: (str)filename, the file to be read.

        RETURNED VALUE: (None if a problem occured or a dict)
            (pimydoc)config file format
            ⋅
            ⋅----------------------------------------------------------------
            ⋅config file format                 read_cfgfile() returned value
            ⋅----------------------------------------------------------------
            ⋅(data selection)                   〖"data selection"〗 = {}
            ⋅    data selection=all             〖"data selection"〗〖"data selection"〗 = str
            ⋅                   only if yes
            ⋅                   data set/xxx
            ⋅data sets                          〖"data sets"〗= {}
            ⋅    data set/xxx=                  〖"data sets"〗〖"data set/xxx"〗 = set1;set2;...
            ⋅data objects
            ⋅    set1 = yes or false             〖"data objects"〗〖"set1"〗 = (bool)True/False
            ⋅    set2 = yes or false
            ⋅    ...
    """
    if ARGS.verbosity == VERBOSITY_DEBUG:
        rprint(f"@ Trying to read '{filename}' ({normpath(filename)}) as a config file.")

    if not os.path.exists(filename):
        if not ARGS.checkup:
            rprint(f"(ERR001) Missing config file '{filename}' ({normpath(filename)}).")
        return None

    res = {"data selection": {},
           "data sets": {},
           "data objects": {},
           }

    # ------------------------------------------------------------------
    # (1/3) let's read <filename> using configparser.ConfigParser.read()
    # ------------------------------------------------------------------
    try:
        config = configparser.ConfigParser()
        config.read(filename)
    except (configparser.DuplicateOptionError,) as error:
        rprint(f"(ERR002) While reading config file '{filename}': {error}.")
        return None

    # -------------------------------
    # (2/3) well formed config file ?
    # -------------------------------
    if "data selection" not in config:
        rprint(f"(ERR003) While reading config file '{filename}': "
               "missing '\[data selection]' section.")
        return None
    if "data sets" not in config:
        rprint(f"(ERR004) While reading config file '{filename}': "
               f"missing '\[data sets]' section.")
        return None
    if "data objects" not in config:
        rprint(f"(ERR005) While reading config file '{filename}': "
               f"missing '\[data objects]' section.")
        return None
    if "data selection" not in config["data selection"]:
        rprint(f"(ERR006) While reading config file '{filename}': "
               f"missing '\[data selection]data selection=' entry.")
        return None

    if config["data selection"]["data selection"] in ("all", "only if yes"):
        # ok, nothing to do.
        pass
    elif config["data selection"]["data selection"].startswith("data set/"):
        setname = config["data selection"]["data selection"]
        if setname not in config["data sets"]:
            rprint(f"(ERR007) While reading config file '{filename}': "
                   f"undefined data set '{setname}' "
                   "used in \[data selection] section but not defined in \[data sets] section")
            return None
    else:
        rprint(f"(ERR008) While reading config file '{filename}': "
               "can't interpret the value of config['data selection']['data selection']: "
               f"what is '{config['data selection']['data selection']}' ?")
        return None

    for data_set in config['data sets']:
        for data_set__subitem in config['data sets'][data_set].split(";"):
            if data_set__subitem.strip() != "" and \
               data_set__subitem not in config['data objects']:
                rprint("(ERROR014) Wrong definition in \[data sets]; unknown data object "
                       f"'{data_set__subitem}', not defined in \[data objects].")
                return None

    # --------------------------------------------------------
    # (3/3) if everything is in order, let's initialize <res>.
    # --------------------------------------------------------
    res['data selection']['data selection'] = config['data selection']['data selection']
    for dataobject_name in config['data objects']:
        res['data objects'][dataobject_name] = config['data objects'].getboolean(dataobject_name)
    for data_set in config['data sets']:
        res['data sets'][data_set] = \
            (data for data in config['data sets'][data_set].split(";") if data.strip() != "")

    # ----------------------
    # details/debug messages
    # ----------------------
    if ARGS.verbosity >= VERBOSITY_DETAILS:
        rprint(f"Init file '{filename}' ({normpath(filename)}) has been read.")

    if ARGS.verbosity == VERBOSITY_DEBUG:
        rprint(f"@ Successfully read '{filename}' ({normpath(filename)}) as a config file.")

    return res


def normpath(path):
    """
        normpath()

        Return a human-readable (e.g. "~" -> "/home/myhome/") normalized
        version of a file path.
        ________________________________________________________________________

        PARAMETER : (str)path

        RETURNED VALUE : the normalized <path>
    """
    res = os.path.normpath(os.path.abspath(os.path.expanduser(path)))
    if res == ".":
        res = os.getcwd()
    return res


def checkup():
    """
        checkup()

        Show some informations :
        - installed serializers;
        - configuration file that would be used; does this file exist ?
          can this file be read without errors ?
    """
    rprint("* Serializers:")
    for serializer in SERIALIZERS.values():
        rprint("  - ", serializer.checkup_repr())

    rprint()
    rprint("* Config file:")
    if not os.path.exists(ARGS.cfgfile):
        diagnostic = "Such a file doesn't exist."
    else:
        if read_cfgfile(ARGS.cfgfile) is None:
            diagnostic = "Such a file exists but can't be read correctly."
        else:
            diagnostic = "Such a file exists and can be read without errors."

    rprint(f"With current arguments, configuration file would be '{ARGS.cfgfile}' "
           f"({normpath(ARGS.cfgfile)}). "+diagnostic)


if linden.globs.ARGS.checkup:
    checkup()
    sys.exit(1)  # TODO RETURNED VALUE

# Such a file is required to create file descriptor objects.
# The temp. file will be removed at the end of the program.
if not os.path.exists(TMPFILENAME):
    with open(TMPFILENAME, "w", encoding="utf-8") as tmpfile:
        pass
from linden.data import DATA


class LindenError(Exception):
    """
        LindenError class

        Unique exception raised by the program.
    """


def get_data_selection(data, config):
    res = []

    if data == "all":
        res = tuple(DATA.keys())
    elif data == "ini":
        if config["data selection"]["data selection"] == "all":
            res = tuple(config["objects"].keys())
        elif config["data selection"]["data selection"] == "only if yes":
            res = (data_name for data_name in config["data objects"]
                   if config["data objects"][data_name])
        elif config["data selection"]["data selection"].startswith("data set/"):
            res = tuple(config["data sets"][config["data selection"]["data selection"]])
        else:
            # TODO: error
            raise LindenError("TODO")
    else:
        # TODO
        raise LindenError("TODO")

    return res


def get_serializers_selection(serializer1,
                              serializer2):
    """
        get_serializers_selection()

        Return a tuple of all serializers defined by (str)<serializer1>, (str)<serializer1>.

        _______________________________________________________________________

        ARGUMENTS:
        o    <serializer1> : value returned by read_cmpstring()
        o    <serializer2> : value returned by read_cmpstring()

        RETURNED VALUE: a tuple of str
    """
    res = set()

    if serializer1 == "all":
        for serializer in SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer1)

    if serializer2 == "all":
        for serializer in SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer2)

    return tuple(res)


def read_cmpstring(src_string):
    """
        read_cmpstring()

        Return a simpler representation of (str)<src_string>.

        Some valid examples, "..." being "(bool/success)True".
        --cmp="jsonpickle vs all (all)"
        --cmp="jsonpickle vs all"
        --cmp="jsonpickle"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (data/str)"all"

        --cmp="jsonpickle (ini)"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (data/str)"ini"

        --cmp="jsonpickle vs json"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"json", (data/str)"all"

        "vs" may be used as well as "versus" or "against".

        _______________________________________________________________________

        ARGUMENT: (str)src_string, the source string to be read.
                syntax: "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

        RETURNED VALUE: (bool)success, (str)serializer1, (str)serializer2, (str:"all|cwc|ini")data
    """
    if res := re.match(REGEX_CMP, src_string):
        serializer1 = res.group("serializer1")
        if serializer1 is None or serializer1 == "others":
            serializer1 = "all"
        serializer2 = res.group("serializer2")
        if serializer2 is None or serializer2 == "others":
            serializer2 = "all"
        data = res.group("data")
        if data is None:
            data = "all"

        if not (serializer1 == "all" or serializer1 in SERIALIZERS):
            rprint(f"(ERR009) Unknown serializer #1: what is '{serializer1}' ? "
                   f"Known serializers #1 are 'all' and {tuple(SERIALIZERS.keys())}.")
            return False, None, None, None
        if not (serializer2 == "all" or serializer2 == "others" or serializer2 in SERIALIZERS):
            rprint(f"(ERR010) Unknown serializer #2: what is '{serializer2}' ? "
                   f"Known serializers #2 are 'all', 'others' and {tuple(SERIALIZERS.keys())}.")
            return False, None, None, None
        if serializer1 == serializer2 and serializer1 != "all":
            rprint(f"(ERR011) Both serializer-s (here, both set to '{serializer1}') "
                   "can't have the same value, 'all' and 'all' excepted.")
            return False, None, None, None

        return True, serializer1, serializer2, data

    rprint(f"(ERR012) Ill-formed cmp string '{src_string}'. "
           f"Expected syntax is '{REGEX_CMP__HELP}'.")
    return False, None, None, None


def report(results,
           s1s2d):
    """
        report()

        Print an analyze of <results>.
        _______________________________________________________________________

        ARGUMENTS:
TODO
        o  results: (SerializationResults)a dict of [(str)serializer][(str)data_name] = SerializationResult
    """
    serializer1, serializer2, data = s1s2d

    # report (A)
    if "A;" in ARGS.report:
        rprint(f"[bold white on blue]REPORT for --cmp set to '[italic]{ARGS.cmp}[/italic]'[/bold white on blue]")
        rprint()

    # report (B1a)
    if "B1a;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](B1a) full details: serializer * data object[/bold white on blue]")
        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("serializer/data object", width=25)
        table.add_column("enc. ok ?", width=12)
        table.add_column("enc. time", width=10)
        table.add_column("jsonstr. len.", width=13)
        table.add_column("dec. ok ?", width=12)
        table.add_column("dec. time", width=10)
        table.add_column("enc ⇆ dec ?", width=12)

        for serializer in results.serializers:
            table.add_row("[yellow]"+serializer+":"+"[/yellow]")
            for dataobj in results.dataobjs:
                table.add_row("> "+ "[white]" + dataobj + "[/white]",
                              results.repr_attr(serializer, dataobj, "encoding_success"),
                              results.repr_attr(serializer, dataobj, "encoding_time"),
                              results.repr_attr(serializer, dataobj, "encoding_stringlength"),
                              results.repr_attr(serializer, dataobj, "decoding_success"),
                              results.repr_attr(serializer, dataobj, "decoding_time"),
                              results.repr_attr(serializer, dataobj, "similarity"))
        rprint(table)
        rprint()

    # report (B1b)
    if "B1b;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](B1b) full details: serializers[/bold white on blue]")
        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("serializer", width=25)
        table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
        table.add_column("Σ enc. time", width=10)
        table.add_column("Σ jsonstr. len.", width=13)
        table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)
        table.add_column("Σ dec. time", width=10)
        table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

        for serializer in results.serializers:
            table.add_row(f"[yellow]{serializer}[/yellow]",
                          f"{results.ratio_encoding_success(serializer=serializer)}",
                          f"{results.total_encoding_time(serializer=serializer)}",
                          f"{results.total_encoding_stringlength(serializer=serializer)}",
                          f"{results.ratio_decoding_success(serializer=serializer)}",
                          f"{results.total_decoding_time(serializer=serializer)}",
                          f"{results.ratio_similarity(serializer=serializer)}",
                          )

        rprint(table)
        rprint()

    # report (B1c)
    if "B1c;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](B1c) full details: serializer <S> can't handle <dataobj>[/bold white on blue]")
        for serializer in results.serializers:
            _list = tuple(dataobj for dataobj in results[serializer] \
                          if not results[serializer][dataobj].similarity)
            if not _list:
                rprint(f"* There's no data object that serializer '[yellow]{serializer}[/yellow]' can't handle.")
            else:
                rprint(f"* Serializer '[yellow]{serializer}[/yellow]' can't handle the following data objects:")
                for dataobj in _list:
                    rprint("  - ", "[white]" + dataobj + "[/white]")
        rprint()

    # report (B2a)
    if "B2a;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](B2a) full details: data object * serializer[/bold white on blue]")
        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("data object/serializer", width=25)
        table.add_column("enc. ok ?", width=12)
        table.add_column("enc. time", width=10)
        table.add_column("jsonstr. len.", width=13)
        table.add_column("dec. ok ?", width=12)
        table.add_column("dec. time", width=10)
        table.add_column("enc ⇆ dec ?", width=12)

        for dataobj in results.dataobjs:
            table.add_row("[white]"+dataobj+":"+"[/white]")
            for serializer in results.serializers:
                table.add_row("> "+ "[yellow]" + serializer + "[/yellow]",
                              results.repr_attr(serializer, dataobj, "encoding_success"),
                              results.repr_attr(serializer, dataobj, "encoding_time"),
                              results.repr_attr(serializer, dataobj, "encoding_stringlength"),
                              results.repr_attr(serializer, dataobj, "decoding_success"),
                              results.repr_attr(serializer, dataobj, "decoding_time"),
                              results.repr_attr(serializer, dataobj, "similarity"))
        rprint(table)
        rprint()

    # report (B2b)
    if "B2b;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](B2b) full details: data objects[/bold white on blue]")
        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("data object", width=25)
        table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)
        table.add_column("Σ enc. time", width=10)
        table.add_column("Σ jsonstr. len.", width=13)
        table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)
        table.add_column("Σ dec. time", width=10)
        table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

        for dataobj in results.dataobjs:
            table.add_row(f"[white]{dataobj}[/white]",
                          f"{results.ratio_encoding_success(dataobj=dataobj)}",
                          f"{results.total_encoding_time(dataobj=dataobj)}",
                          f"{results.total_encoding_stringlength(dataobj=dataobj)}",
                          f"{results.ratio_decoding_success(dataobj=dataobj)}",
                          f"{results.total_decoding_time(dataobj=dataobj)}",
                          f"{results.ratio_similarity(dataobj=dataobj)}",
                          )

        rprint(table)
        rprint()

    # report (C1b)
    if "C1b;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](C1b) full details / base 100: serializers[/bold white on blue]")

        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("serializer", width=25)
        table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
        if base100 := results._get_serializers_base('encoding_time'):
            table.add_column(f"Σ enc. time " \
                             f"(base 100 = {results.total_encoding_time(serializer=base100)})",
                             width=10)
        else:
            table.add_column(f"Σ enc. time [red](NO BASE 100)[/red]",
                             width=10)

        if base100 := results._get_serializers_base('encoding_stringlength'):
            table.add_column("Σ jsonstr. len. " \
                             f"(base 100 = {results.total_encoding_stringlength(serializer=base100)})",
                             width=13)
        else:
            table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)
            
        table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)

        if base100 := results._get_serializers_base('decoding_time'):
            table.add_column(f"Σ dec. time " \
                             f"(base 100 = {results.total_decoding_time(serializer=base100)})",
                             width=10)
        else:
            table.add_column(f"Σ dec. time [red](NO BASE 100)[/red]",
                             width=10)
        
        table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

        for serializer in results.serializers:
            table.add_row(f"[yellow]{serializer}[/yellow]",
                          f"{results.ratio_encoding_success(serializer=serializer)}",
                          f"{results.total_encoding_time(serializer=serializer, output='base100')}",
                          f"{results.total_encoding_stringlength(serializer=serializer, output='base100')}",
                          f"{results.ratio_decoding_success(serializer=serializer)}",
                          f"{results.total_decoding_time(serializer=serializer, output='base100')}",
                          f"{results.ratio_similarity(serializer=serializer)}",
                          )

        rprint(table)
        rprint()

    # report (C2b)
    if "C2b;" in ARGS.report:
        if "titles;" in ARGS.report:
            rprint("[bold white on blue](C2b) full details: data objects / base 100[/bold white on blue]")

        table = rich.table.Table(show_header=True, header_style="bold blue")
        table.add_column("data object", width=25)
        table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)

        if base100 := results._get_dataobjs_base('encoding_time'):
            table.add_column(f"Σ enc. time " \
                             f"(base 100 = {results.total_encoding_time(dataobj=base100)})",
                             width=10)
        else:
            table.add_column(f"Σ enc. time [red](NO BASE 100)[/red]",
                             width=10)

        if base100 := results._get_dataobjs_base('encoding_stringlength'):
            table.add_column("Σ jsonstr. len. " \
                             f"(base 100 = {results.total_encoding_stringlength(dataobj=base100)})",
                             width=13)
        else:
            table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)

        table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)

        if base100 := results._get_dataobjs_base('decoding_time'):
            table.add_column(f"Σ dec. time " \
                             f"(base 100 = {results.total_decoding_time(dataobj=base100)})",
                             width=10)
        else:
            table.add_column(f"Σ dec. time [red](NO BASE 100)[/red]",
                             width=10)
        
        table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

        for dataobj in results.dataobjs:
            table.add_row(f"[white]{dataobj}[/white]",
                          f"{results.ratio_encoding_success(dataobj=dataobj)}",
                          f"{results.total_encoding_time(dataobj=dataobj, output='base100')}",
                          f"{results.total_encoding_stringlength(dataobj=dataobj, output='base100')}",
                          f"{results.ratio_decoding_success(dataobj=dataobj)}",
                          f"{results.total_decoding_time(dataobj=dataobj, output='base100')}",
                          f"{results.ratio_similarity(dataobj=dataobj)}",
                          )

        rprint(table)
        rprint()


def main():
    """
        main()

        Main entrypoint in the project. This method is called when Linden is called from outside,
        e.g. by the command line.

        _______________________________________________________________________

        RETURNED VALUE: TODO
    """
    if ARGS.verbosity >= VERBOSITY_DETAILS:
        rprint(__projectname__, __version__)
    if ARGS.verbosity == VERBOSITY_DEBUG:
        rprint("@ known data:", list(DATA.keys()))
    if ARGS.verbosity == VERBOSITY_DEBUG:
        rprint("@ known serializers:", SERIALIZERS)

    success, serializer1, serializer2, data = read_cmpstring(ARGS.cmp)
    if ARGS.verbosity == VERBOSITY_DEBUG:
        rprint(f"@ Result of the call to read_cmpstring('{ARGS.cmp}'):",
               success, serializer1, serializer2, data)

    if not success:
        rprint(f"(ERR013) an error occured while reading cmp string '{ARGS.cmp}'.")
        return -2  # TODO

    config = None
    if data == "ini":
        config = read_cfgfile(ARGS.cfgfile)

        if config is None:
            return -1  # TODO returned value

    try:
        # serializers and data to be used through the tests:
        _serializers = get_serializers_selection(serializer1, serializer2)
        if ARGS.verbosity == VERBOSITY_DEBUG:
            rprint("@ serializers to be used are: ", _serializers)
        _dataobjs = get_data_selection(data, config)
        if ARGS.verbosity == VERBOSITY_DEBUG:
            rprint("@ data objs to be used are: ", _dataobjs)

        results = SerializationResults()
        for serializer in _serializers:
            results[serializer] = {}
            for data_name in _dataobjs:
                if ARGS.verbosity == VERBOSITY_DEBUG:
                    rprint(f"@ about to call function for serializer='{serializer}' "
                           f"and data name='{data_name}'")
                results[serializer][data_name] = SERIALIZERS[serializer].func(action="serialize",
                                                                              obj=DATA[data_name])
                if ARGS.verbosity == VERBOSITY_DEBUG:
                    rprint("@ result:", results[serializer][data_name])
        if not results._finish_initialization():
            rprint("ERR015: incorrect data, the program has to stop.")
            return -3  # TODO
        if results.dataobjs_number == 0:
            rprint("No data to handle, the program can stop.")
            return 2  # TODO

        report(results,
               (serializer1, serializer2, data))

    except LindenError as exception:
        rprint(exception)

    return 0  # TODO


# =============================================================================
if __name__ == '__main__':
    main()
