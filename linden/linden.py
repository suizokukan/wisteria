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
import numbers
import io
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
    if not os.path.exists(filename):
        if not ARGS.checkup:
            rprint(f"ERROR: missing config file '{filename}' ({normpath(filename)}).")
        return None

    res = {"serializers": {},
           "data sets": {},
           "data": {},
           }
    try:
        config = configparser.ConfigParser()
        config.read(filename)
    except (configparser.DuplicateOptionError,) as error:
        rprint(f"ERROR while reading config file '{filename}': {error}.")
        return None

    for serializer in config['serializers']:
        res['serializers'][serializer] = config['serializers'].getboolean(serializer)
    for data in config['data']:
        res['data'][data] = config['data'].getboolean(data)
    for data_set in config['data sets']:
        res['data sets'][data_set] = \
            (data for data in config['data sets'][data_set].split(";") if data.strip() != "")

    if ARGS.verbosity>=VERBOSITY_DETAILS:
        if not ARGS.checkup:
            rprint(f"Init file '{filename}' ({normpath(filename)}) has been read.")

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
    rprint("Serializers:")
    for serializer in SERIALIZERS.values():
        rprint("* ", serializer.checkup_repr())

    rprint()
    rprint("Config file:")
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
    with open(TMPFILENAME, "w") as tmpfile:
        pass
from linden.data import DATA


class LindenError(Exception):
    """
    """

def get_data_selection(config):
    # TODO
    # pourquoi ne pas remplacer <config> par la globale CONFIG ?

    res = []

    if config["tasks"]["data selection"] == "all":
        res = config["data"]
    elif config["tasks"]["data selection"] == "only if yes":
        res = (data for data in config["data"] if config["data"][data])
    elif config["tasks"]["data selection"].startswith("data set/"):
        res = config["data sets"][config["tasks"]["data selection"]]
    else:
        # TODO
        # erreur: unknown order
        pass

    # TODO
    # vérification: est-ce que le contenu de <res> est connu de DATA ?
    _res = []
    for data in res:
        if data not in DATA:
            raise LindenError(f"! ERROR: unknown data '{data}'.")
        else:
            _res.append(data)
    return _res


def get_serializers_selection(config):
    """
    None if error
    """
    # TODO
    # pourquoi ne pas remplacer <config> par la globale CONFIG ?

    res = []

    if config["tasks"]["serializers selection"] == "all":
        res = config["serializers"]
    elif config["tasks"]["serializers selection"] == "only if yes":
        res = (serializer for serializer in config["serializers"] if config["serializers"][serializer])
    else:
        raise LindenError(f"ERROR: unknown serializer selection keyword '{config['tasks']['serializers selection']}'")
        return None

    # TODO
    # vérification: est-ce que le contenu de <res> est connu de SERIALIZERS ?
    _res = []
    for serializer in res:
        if serializer not in SERIALIZERS:
            raise LindenError(f"! ERROR: unknown serializer '{serializer}'.")
        else:
            _res.append(serializer)

    return _res


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
            rprint(f"Unknown serializer #1: what is '{serializer1}' ? " \
                   f"Known serializers #1 are 'all' and {tuple(SERIALIZERS.keys())}.")
            return False, None, None, None
        if not (serializer2 == "all" or serializer2 == "others" or serializer2 in SERIALIZERS):
            rprint(f"Unknown serializer #2: what is '{serializer2}' ? " \
                   f"Known serializers #2 are 'all', 'others' and {tuple(SERIALIZERS.keys())}.")
            return False, None, None, None
        if serializer1==serializer2 and serializer1 != "all":
            rprint(f"Both serializer-s (here, both set to '{serializer1}') can't have the same value, 'all' and 'all' excepted.")
            return False, None, None, None

        return True, serializer1, serializer2, data

    rprint(f"ERROR: ill-formed cmp string '{src_string}'. Expected syntax is '{REGEX_CMP__HELP}'.")
    return False, None, None, None


def main():
    success, serializer1, serializer2, data = read_cmpstring(ARGS.cmp)

    if not success:
        rprint(f"ERROR: an error occured while reading cmp string '{ARGS.cmp}'.")
        return -2 # TODO

    rprint(success, serializer1, serializer2, data)

    if data=="ini":
        CONFIG = read_cfgfile(ARGS.cfgfile)

        if CONFIG is None:
            return -1  # TODO returned value

    # try:
    #     if ARGS.verbosity>=VERBOSITY_DETAILS:
    #         rprint(__projectname__, __version__)

    #     if ARGS.verbosity==VERBOSITY_DEBUG:
    #         rprint("* known data:", list(DATA.keys()))
    #     if ARGS.verbosity==VERBOSITY_DEBUG:
    #         rprint("* known serializers:", SERIALIZERS)

    #     for task in CONFIG["tasks"]["tasks"]:
    #         if task == "data selection * serializers selection":
    #             for data in get_data_selection(CONFIG):
    #                 for serializer in get_serializers_selection(CONFIG):
    #                     result = SERIALIZERS[serializer].func(action="serialize",
    #                                                       obj=DATA[data])

    # except LindenError as exception:
    #     rprint(exception)

if __name__ == '__main__':
    main()
