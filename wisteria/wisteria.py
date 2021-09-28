#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    wisteria.py

    (pimydoc)exit codes
    ⋅*  0: normal exit code
    ⋅*  1: normal exit code after --checkup
    ⋅*  2: normal exit code after --downloadconfigfile
    ⋅* -1: error, given config file can't be read (missing or ill-formed file)
    ⋅* -2: error, ill-formed --cmp string
    ⋅* -3: internal error, data can't be loaded

TODO : functions ?
"""
import argparse
import atexit
import configparser
import os
import os.path
import re
import shutil
import sys
import urllib.error
import urllib.request

from rich import print as rprint

import wisteria.globs
from wisteria.globs import REPORT_MINIMAL_STRING, REPORT_FULL_STRING
from wisteria.globs import TMPFILENAME, REGEX_CMP, REGEX_CMP__HELP
from wisteria.globs import VERBOSITY_MINIMAL, VERBOSITY_NORMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.globs import DEFAULT_CONFIG_FILENAME, DEFAULTCFGFILE_URL
from wisteria.aboutproject import __projectname__, __version__
from wisteria.report import report
from wisteria.results import compute_results
from wisteria.utils import normpath
import wisteria.serializers
import wisteria.data
from wisteria.wisteriaerror import WisteriaError

# =============================================================================
# (01) temp file opening
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report

# Such a file is required to create file descriptor objects.
# The temp. file will be removed at the end of the program.
if not os.path.exists(TMPFILENAME):
    with open(TMPFILENAME, "w", encoding="utf-8") as tmpfile:
        pass


# =============================================================================
# (02) command line parsing
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
PARSER = \
    argparse.ArgumentParser(description='Comparisons of different Python serializers. '
                            'Try $wisteria --checkup then $wisteria --cmp="pickle against marshal"',
                            epilog=f"{__projectname__}: {__version__}",
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('--version', '-v',
                    action='version',
                    version=f"{__projectname__} {__version__}",
                    help="Show the version and exit.")

PARSER.add_argument('--cmp',
                    action='store',
                    default="all vs all",
                    help=f"Comparisons details. Expected syntax: '{REGEX_CMP__HELP}'.")

PARSER.add_argument('--cfgfile',
                    action='store',
                    default=DEFAULT_CONFIG_FILENAME,
                    help="config file to be used.")

PARSER.add_argument('--checkup',
                    action='store_true',
                    help="show installed serializers, try to read current config file and exit")

PARSER.add_argument('--downloadconfigfile',
                    action='store_true',
                    help="download default config file and exit")

PARSER.add_argument('--report',
                    action='store',
                    default="minimal",
                    help=f"Report format: 'minimal' (interpreted as '{REPORT_MINIMAL_STRING}'), "
                    f"'full' (interpreted as '{REPORT_FULL_STRING}'), "
                    "or a subset from this last string, e.g. 'A1;B1a;'. "
                    "You may use shorter strings like 'B' (=B1+B2, i.e. B1a+B1b...+B2a+B2b...) "
                    "or like 'B1' (=B1a+B1b+B1c). "
                    f"Accepted keywords are {tuple(wisteria.report.STR2REPORTSECTION.keys())}. "
                    "More informations in the documentation. "
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

wisteria.globs.ARGS = PARSER.parse_args()


# =============================================================================
# (03) project name & version
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint(f"> {__projectname__}, {__version__}")


# =============================================================================
# (04) ARGS.report interpretation
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
if wisteria.globs.ARGS.report == "minimal":
    wisteria.globs.ARGS.report = REPORT_MINIMAL_STRING
    if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"> --report 'minimal' interpreted as '{wisteria.globs.ARGS.report}'.")
elif wisteria.globs.ARGS.report == "full":
    wisteria.globs.ARGS.report = REPORT_FULL_STRING
    if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"> --report 'full' interpreted as '{wisteria.globs.ARGS.report}'.")
elif not wisteria.globs.ARGS.report.endswith(";"):
    wisteria.globs.ARGS.report += ";"
    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint("> --report: semicolon added at the end; "
               f"--report is now '{wisteria.globs.ARGS.report}'.")
if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint("@ From now --report (wisteria.globs.ARGS.report) is set "
           f"to '{wisteria.globs.ARGS.report}'.")

# =============================================================================
# This point is only reached if there's no --version/--help argument
# on the command line.
# =============================================================================
ARGS = wisteria.globs.ARGS


# =============================================================================
# (05) exit handler
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report

# exit handler: let's remove the tmp file if it exists.
def exit_handler():
    """
        exit_handler()

        Remove the tmp file if it exists
    """
    if os.path.exists(TMPFILENAME):
        os.remove(TMPFILENAME)


atexit.register(exit_handler)


# =============================================================================
# (06) serializers import
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
wisteria.serializers.init_serializers()


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
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"@ Trying to read '{filename}' ({normpath(filename)}) as a config file.")

    if not os.path.exists(filename):
        if not ARGS.checkup:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID001) Missing config file '{filename}' ({normpath(filename)}).")
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
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID002) While reading config file '{filename}': {error}.")
        return None

    # -------------------------------
    # (2/3) well formed config file ?
    # -------------------------------
    if "data selection" not in config:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID003) While reading config file '{filename}': "
               "missing '\\[data selection]' section.")
        return None
    if "data sets" not in config:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID004) While reading config file '{filename}': "
               "missing '\\[data sets]' section.")
        return None
    if "data objects" not in config:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID005) While reading config file '{filename}': "
               "missing '\\[data objects]' section.")
        return None
    if "data selection" not in config["data selection"]:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID006) While reading config file '{filename}': "
               "missing '\\[data selection]data selection=' entry.")
        return None

    if config["data selection"]["data selection"] in ("all", "only if yes"):
        # ok, nothing to do.
        pass
    elif config["data selection"]["data selection"].startswith("data set/"):
        setname = config["data selection"]["data selection"]
        if setname not in config["data sets"]:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID007) While reading config file '{filename}': "
                   f"undefined data set '{setname}' "
                   "used in \\[data selection] section but not defined in \\[data sets] section")
            return None
    else:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID008) While reading config file '{filename}': "
               "can't interpret the value of config['data selection']['data selection']: "
               f"what is '{config['data selection']['data selection']}' ?")
        return None

    for data_set in config['data sets']:
        for data_set__subitem in config['data sets'][data_set].split(";"):
            if data_set__subitem.strip() != "" and \
               data_set__subitem not in config['data objects']:
                # (pimydoc)console messages
                # ⋅- debug messages start with   @
                # ⋅- info messages start with    >
                # ⋅- error messages start with   ERRORIDXXX
                # ⋅- checkup messages start with *
                rprint("(ERROR014) Wrong definition in \\[data sets]; unknown data object "
                       f"'{data_set__subitem}', not defined in \\[data objects].")
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
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"> Init file '{filename}' ({normpath(filename)}) has been read.")

    if ARGS.verbosity == VERBOSITY_DEBUG:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"@ Successfully read '{filename}' ({normpath(filename)}) as a config file.")

    return res


def checkup():
    """
        checkup()

        Show some informations :
        - installed serializers;
        - configuration file that would be used; does this file exist ?
          can this file be read without errors ?
    """
    serializers = wisteria.globs.SERIALIZERS

    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint("* Serializers:")
    for serializer in serializers.values():
        rprint("  - ", serializer.checkup_repr())

    rprint()

    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint("* Config file:")
    if not os.path.exists(ARGS.cfgfile):
        diagnostic = "Such a file doesn't exist."
    else:
        if read_cfgfile(ARGS.cfgfile) is None:
            diagnostic = "Such a file exists but can't be read correctly."
        else:
            diagnostic = "Such a file exists and can be read without errors."

    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint(f"  With current arguments, configuration file would be '{ARGS.cfgfile}' "
           f"({normpath(ARGS.cfgfile)}). " + diagnostic)


# =============================================================================
# (07) checkup
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
if wisteria.globs.ARGS.checkup:
    checkup()
    # (pimydoc)exit codes
    # ⋅*  0: normal exit code
    # ⋅*  1: normal exit code after --checkup
    # ⋅*  2: normal exit code after --downloadconfigfile
    # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
    # ⋅* -2: error, ill-formed --cmp string
    # ⋅* -3: internal error, data can't be loaded
    sys.exit(1)


def downloadconfigfile():
    """
        downloadconfigfile()

        Download default config file.
        _______________________________________________________________________

        RETURNED VALUE: (bool)success
    """
    targetname = DEFAULT_CONFIG_FILENAME

    if wisteria.globs.ARGS.verbosity >= VERBOSITY_NORMAL:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"> Trying to download '{DEFAULTCFGFILE_URL}' "
               f"which will be written as '{targetname}' ('{normpath(targetname)}').")

    try:
        with urllib.request.urlopen(DEFAULTCFGFILE_URL) as response, \
             open(targetname, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_NORMAL:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"> Successfully downloaded '{DEFAULTCFGFILE_URL}', "
                   f"written as '{targetname}' ('{normpath(targetname)}')")
        return True

    except urllib.error.URLError as exception:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"(ERRORID000) An error occured: {exception}")
        return False


# =============================================================================
# (08) download default config file
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
if wisteria.globs.ARGS.downloadconfigfile:
    downloadconfigfile()
    # (pimydoc)exit codes
    # ⋅*  0: normal exit code
    # ⋅*  1: normal exit code after --checkup
    # ⋅*  2: normal exit code after --downloadconfigfile
    # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
    # ⋅* -2: error, ill-formed --cmp string
    # ⋅* -3: internal error, data can't be loaded
    sys.exit(2)


# =============================================================================
# (09) known data init
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
wisteria.data.init_data()


def read_cmpstring(cmpstring):
    """
        read_cmpstring()

        Return a simpler representation of (str)<cmpstring>.

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

        ARGUMENT: (str)cmpstring, the source string to be read.
                syntax: "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

        RETURNED VALUE: (bool)success,
                        (str)serializer1,
                        (str)serializer2,
                        (str:"all|cwc|ini")cmpdata
    """
    serializers = wisteria.globs.SERIALIZERS

    if res := re.match(REGEX_CMP, cmpstring):
        serializer1 = res.group("serializer1")
        if serializer1 is None or serializer1 == "others":
            serializer1 = "all"
        serializer2 = res.group("serializer2")
        if serializer2 is None or serializer2 == "others":
            serializer2 = "all"
        cmpdata = res.group("data")
        if cmpdata is None:
            cmpdata = "all"

        if not (serializer1 == "all" or serializer1 in serializers):
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID009) Unknown serializer #1 from cmp string '{cmpstring}': "
                   f"what is '{serializer1}' ? "
                   f"Known serializers #1 are 'all' and {tuple(serializers.keys())}.")
            return False, None, None, None
        if not (serializer2 == "all" or serializer2 == "others" or serializer2 in serializers):
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID010) Unknown serializer #2 from cmp string '{cmpstring}': "
                   f"what is '{serializer2}' ? "
                   f"Known serializers #2 are 'all', 'others' and {tuple(serializers.keys())}.")
            return False, None, None, None
        if serializer1 == serializer2 and serializer1 != "all":
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID011) Both serializer-s from cmp string '{cmpstring}' "
                   f"(here, both set to '{serializer1}') "
                   "can't have the same value, 'all' and 'all' excepted.")
            return False, None, None, None

        return True, serializer1, serializer2, cmpdata

    # (pimydoc)console messages
    # ⋅- debug messages start with   @
    # ⋅- info messages start with    >
    # ⋅- error messages start with   ERRORIDXXX
    # ⋅- checkup messages start with *
    rprint(f"(ERRORID012) Ill-formed cmp string '{cmpstring}'. "
           f"Expected syntax is '{REGEX_CMP__HELP}'.")
    return False, None, None, None


def main():
    """
        main()

        Main entrypoint in the project. This method is called when Wisteria is called from outside,
        e.g. by the command line.

        _______________________________________________________________________

        RETURNED VALUE:
                (pimydoc)exit codes
                ⋅*  0: normal exit code
                ⋅*  1: normal exit code after --checkup
                ⋅*  2: normal exit code after --downloadconfigfile
                ⋅* -1: error, given config file can't be read (missing or ill-formed file)
                ⋅* -2: error, ill-formed --cmp string
                ⋅* -3: internal error, data can't be loaded
    """
    data = wisteria.globs.DATA
    serializers = wisteria.globs.SERIALIZERS

    # =========================================================================
    # (10.1) main(): debug messages
    # =========================================================================
    # (pimydoc)code structure
    # ⋅- (01) temp file opening
    # ⋅- (02) command line parsing
    # ⋅- (03) project name & version
    # ⋅- (04) ARGS.report interpretation
    # ⋅- (05) exit handler
    # ⋅- (06) serializers import
    # ⋅- (07) checkup
    # ⋅- (08) download default config file
    # ⋅- (09) known data init
    # ⋅- (10) call to main()
    # ⋅       - (10.1) main(): debug messages
    # ⋅       - (10.2) main(): cmp string interpretation
    # ⋅       - (10.3) main(): config file reading
    # ⋅       - (10.4) main(): results computing
    # ⋅       - (10.5) main(): report
    if ARGS.verbosity == VERBOSITY_DEBUG:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint("@ known data:", list(data.keys()))
    if ARGS.verbosity == VERBOSITY_DEBUG:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint("@ known serializers:", serializers)

    try:
        # =========================================================================
        # (10.2) main(): cmp string interpretation
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) temp file opening
        # ⋅- (02) command line parsing
        # ⋅- (03) project name & version
        # ⋅- (04) ARGS.report interpretation
        # ⋅- (05) exit handler
        # ⋅- (06) serializers import
        # ⋅- (07) checkup
        # ⋅- (08) download default config file
        # ⋅- (09) known data init
        # ⋅- (10) call to main()
        # ⋅       - (10.1) main(): debug messages
        # ⋅       - (10.2) main(): cmp string interpretation
        # ⋅       - (10.3) main(): config file reading
        # ⋅       - (10.4) main(): results computing
        # ⋅       - (10.5) main(): report
        success, serializer1, serializer2, cmpdata = read_cmpstring(ARGS.cmp)
        if ARGS.verbosity == VERBOSITY_DEBUG:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"@ Result of the call to read_cmpstring('{ARGS.cmp}'):",
                   success, serializer1, serializer2, cmpdata)

        if not success:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint(f"(ERRORID013) an error occured while reading cmp string '{ARGS.cmp}'.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            return -2

        # =========================================================================
        # (10.3) main(): config file reading
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) temp file opening
        # ⋅- (02) command line parsing
        # ⋅- (03) project name & version
        # ⋅- (04) ARGS.report interpretation
        # ⋅- (05) exit handler
        # ⋅- (06) serializers import
        # ⋅- (07) checkup
        # ⋅- (08) download default config file
        # ⋅- (09) known data init
        # ⋅- (10) call to main()
        # ⋅       - (10.1) main(): debug messages
        # ⋅       - (10.2) main(): cmp string interpretation
        # ⋅       - (10.3) main(): config file reading
        # ⋅       - (10.4) main(): results computing
        # ⋅       - (10.5) main(): report
        config = None
        if cmpdata == "ini":
            config = read_cfgfile(ARGS.cfgfile)

            if config is None:
                # (pimydoc)exit codes
                # ⋅*  0: normal exit code
                # ⋅*  1: normal exit code after --checkup
                # ⋅*  2: normal exit code after --downloadconfigfile
                # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
                # ⋅* -2: error, ill-formed --cmp string
                # ⋅* -3: internal error, data can't be loaded
                return -1

        # =========================================================================
        # (10.4) main(): results computing
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) temp file opening
        # ⋅- (02) command line parsing
        # ⋅- (03) project name & version
        # ⋅- (04) ARGS.report interpretation
        # ⋅- (05) exit handler
        # ⋅- (06) serializers import
        # ⋅- (07) checkup
        # ⋅- (08) download default config file
        # ⋅- (09) known data init
        # ⋅- (10) call to main()
        # ⋅       - (10.1) main(): debug messages
        # ⋅       - (10.2) main(): cmp string interpretation
        # ⋅       - (10.3) main(): config file reading
        # ⋅       - (10.4) main(): results computing
        # ⋅       - (10.5) main(): report
        compute_results__res = compute_results(config,
                                               serializer1,
                                               serializer2,
                                               cmpdata)
        if compute_results__res[0] is None:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            return compute_results__res[1]
        results = compute_results__res[0]

        # =========================================================================
        # (10.5) main(): report
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) temp file opening
        # ⋅- (02) command line parsing
        # ⋅- (03) project name & version
        # ⋅- (04) ARGS.report interpretation
        # ⋅- (05) exit handler
        # ⋅- (06) serializers import
        # ⋅- (07) checkup
        # ⋅- (08) download default config file
        # ⋅- (09) known data init
        # ⋅- (10) call to main()
        # ⋅       - (10.1) main(): debug messages
        # ⋅       - (10.2) main(): cmp string interpretation
        # ⋅       - (10.3) main(): config file reading
        # ⋅       - (10.4) main(): results computing
        # ⋅       - (10.5) main(): report
        report(results,
               (serializer1, serializer2, cmpdata))

        # (pimydoc)exit codes
        # ⋅*  0: normal exit code
        # ⋅*  1: normal exit code after --checkup
        # ⋅*  2: normal exit code after --downloadconfigfile
        # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
        # ⋅* -2: error, ill-formed --cmp string
        # ⋅* -3: internal error, data can't be loaded
        return 0

    except WisteriaError as exception:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(exception)

        # (pimydoc)exit codes
        # ⋅*  0: normal exit code
        # ⋅*  1: normal exit code after --checkup
        # ⋅*  2: normal exit code after --downloadconfigfile
        # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
        # ⋅* -2: error, ill-formed --cmp string
        # ⋅* -3: internal error, data can't be loaded
        # TODO
        return -5


# =============================================================================
# (10) call to main()
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) temp file opening
# ⋅- (02) command line parsing
# ⋅- (03) project name & version
# ⋅- (04) ARGS.report interpretation
# ⋅- (05) exit handler
# ⋅- (06) serializers import
# ⋅- (07) checkup
# ⋅- (08) download default config file
# ⋅- (09) known data init
# ⋅- (10) call to main()
# ⋅       - (10.1) main(): debug messages
# ⋅       - (10.2) main(): cmp string interpretation
# ⋅       - (10.3) main(): config file reading
# ⋅       - (10.4) main(): results computing
# ⋅       - (10.5) main(): report
if __name__ == '__main__':
    main()
