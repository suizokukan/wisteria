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

import linden.globs
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

PARSER.add_argument('--verbosity',
                    type=int,
                    default=VERBOSITY_NORMAL,
                    choices=(VERBOSITY_MINIMAL,
                             VERBOSITY_NORMAL,
                             VERBOSITY_DETAILS,
                             VERBOSITY_DEBUG),
                    help="Verbosity level: 0(=mute), 1(=normal), 2(=normal+details), 3(=debug)")

linden.globs.ARGS = PARSER.parse_args()

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


from linden.serializers import SERIALIZERS


def read_cfgfile(filename):
    """
        None if problem
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
    try:
        config = configparser.ConfigParser()
        config.read(filename)
    except (configparser.DuplicateOptionError,) as error:
        rprint(f"(ERR002) While reading config file '{filename}': {error}.")
        return None

    # -------------------------
    # well formed config file ?
    # -------------------------
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

    # --------------------------------------------------
    # if everything is in order, let's initialize <res>.
    # --------------------------------------------------
    res['data selection']['data selection'] = config['data selection']['data selection']
    for data_object_name in config['data objects']:
        res['data objects'][data_object_name] = config['data objects'].getboolean(data_object_name)
    for data_set in config['data sets']:
        res['data sets'][data_set] = \
            (data for data in config['data sets'][data_set].split(";") if data.strip() != "")

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
        _data_objs = get_data_selection(data, config)
        if ARGS.verbosity == VERBOSITY_DEBUG:
            rprint("@ data objs to be used are: ", _data_objs)

        for serializer in _serializers:
            for data_name in _data_objs:
                if ARGS.verbosity == VERBOSITY_DEBUG:
                    rprint(f"@ about to call function for serializer='{serializer}' "
                           f"and data name='{data_name}'")
                result = SERIALIZERS[serializer].func(action="serialize",
                                                      obj=DATA[data_name])
                if ARGS.verbosity == VERBOSITY_DEBUG:
                    rprint("@ result:", result)

    except LindenError as exception:
        rprint(exception)

    return 0  # TODO


# =============================================================================
if __name__ == '__main__':
    main()
