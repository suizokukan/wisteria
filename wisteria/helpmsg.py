#!/usr/bin/env python3
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
    Wisteria project : wisteria/helpmsg.py

    Some help messages
    ___________________________________________________________________________

    o  help_cmdline_exportreport(details=False)
    o  help_cmdline_filter(details=False)
    o  help_cmdline_output(details=False)
    o  help_helpcommandlineargument()
    o  help_graphsfilenames()
"""
import os.path

from wisteria.globs import GRAPHS_GENERIC_FILENAME, DEFAULT_REPORTFILE_NAME
from wisteria.globs import DEFAULT_EXPORTREPORT_FILENAME
from wisteria.globs import REPORTFILE_PATH
from wisteria.utils import normpath, get_missing_required_internal_modules, get_python_version
from wisteria.utils import pimydocstr2str


def help_cmdline_exportreport(details=False):
    """
        help_cmdline_exportreport()

        Return help messages for the command line option "--filter".
        _______________________________________________________________________

        ARGUMENT: (bool)details, True if a full help string has to be returned

        RETURNED VALUE: (str)help message
    """
    if not details:
        return pimydocstr2str("""
        (pimydoc)command line help for --exportreport(short version)
        ⋅Export report by creating a new file in which
        ⋅both report text and graphics are put together.
        ⋅- default value: "no export", i.e. no exported report file
        ⋅- otherwise 'md' is the only value or the only acceptable start string
        ⋅  since md format;
        ⋅  e.g. 'md=myfile.md';
        ⋅  otherwise the default filename is '$DEFAULT_EXPORTREPORT_FILENAME' . "
        """.replace("$DEFAULT_EXPORTREPORT_FILENAME", DEFAULT_EXPORTREPORT_FILENAME))
    return pimydocstr2str("""
    (pimydoc)command line help for --exportreport(full version)
    ⋅Export report by creating a new file in which
    ⋅both report text and graphics are put together.
    ⋅- default value: "no export", i.e. no exported report file
    ⋅- otherwise 'md' is the only value or the only acceptable start string
    ⋅  since md format is the only known format for exported report;
    ⋅  you may add the exported report filename after '=',
    ⋅  e.g. 'md=myfile.md';
    ⋅  the default filename is '$DEFAULT_EXPORTREPORT_FILENAME' . "
    ⋅  Please note that graphs will not be added to the exported file if
    ⋅  --checkup/--downloadconfigfile/--mymachine is set.
    """.replace("$DEFAULT_EXPORTREPORT_FILENAME", DEFAULT_EXPORTREPORT_FILENAME))


def help_cmdline_filter(details=False):
    """
        help_cmdline_filter()

        Return help messages for the command line option "--filter".
        _______________________________________________________________________

        ARGUMENT: (bool)details, True if a full help string has to be returned

        RETURNED VALUE: (str)help message
    """
    if not details:
        return pimydocstr2str("""
        (pimydoc)command line help for --filter(short version)
        ⋅Filter out the data or the serializers to be used.
        ⋅format: either empty string if no filter,
        ⋅either 'data:oktrans_only' to only keep the objects that can be successfully
        ⋅transcoded
        """)
    return pimydocstr2str("""
           (pimydoc)command line help for --filter(full version)
           ⋅The --filter argument allows to select only some serializers or
           ⋅data objects. Currently only two values are accepted:
           ⋅* either a null string (--filter=""): all serializers/data objects are
           ⋅  used;
           ⋅* either 'data:oktrans_only' (--filter='data:oktrans_only'): in this case,
           ⋅  only the objects that can be successfully transcoded are kept;
           """)


def help_cmdline_output(details=False):
    """
        help_cmdline_output()

        Return help messages for the command line option "--output".
        _______________________________________________________________________

        ARGUMENT: (bool)details, True if a full help string has to be returned

        RETURNED VALUE: (str)help message
    """
    if not details:
        return pimydocstr2str("""
        (pimydoc)command line help for --output(short version)
        ⋅Values are 'console' or 'reportfile' or 'console;reportfile'.
        ⋅Instead of 'reportfile'
        ⋅you may specify 'reportfile/a' (append mode) or 'reportfile/w' (write mode).
        ⋅You may add special strings 'TIMESTAMP' or 'DATETIME' to report file name
        ⋅in order to add a timestamp in the filename.
        ⋅Instead of 'reportfile'
        ⋅you may specify 'reportfile=myreportfile'.
        ⋅Combinations like 'reportfile/w=$DEFAULT_REPORTFILE_NAME' are accepted.
        ⋅See by example the default value.
        """.replace("$DEFAULT_REPORTFILE_NAME", DEFAULT_REPORTFILE_NAME))
    return pimydocstr2str("""
           (pimydoc)command line help for --output(full version)
           ⋅A string like '[console;][reportfile/w/a]=subdirectory/myreportfilename'
           ⋅
           ⋅* 'console':
           ⋅  - 'console' : if you want to write output messages to the console
           ⋅
           ⋅* 'reportfile='
           ⋅  - either a simple string like 'report.txt'
           ⋅  - either a string containing 'DATETIME'; in this case, 'DATETIME' will
           ⋅    be replaced by datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S");
           ⋅    e.g. "report_DATETIME.txt" would become something like
           ⋅         "report_2021-12-31.23.59.59.txt"
           ⋅  - either a string containing 'TIMESTAMP'; in this case, 'TIMESTAMP' will
           ⋅    be replaced by str(int(time.time()))
           ⋅      e.g. "report_DATETIME.txt" would become something like
           ⋅           "report_1635672267.txt"
           ⋅
           ⋅BEWARE: The path to the report file must exist; e.g. if ./path/ doesn't
           ⋅exist you can't write:
           ⋅     --output="console;reportfile/w=path/myreportfile"
           """.replace("$DEFAULT_REPORTFILE_NAME", DEFAULT_REPORTFILE_NAME))


def help_helpcommandlineargument():
    """
        help_helpcommandlineargument()

        Complete the --help message. If all required packages are installed,
        give some advice; if all required packages ARE NOT installed,
        give the list of the missing packages.
    """
    missing_modules = get_missing_required_internal_modules()

    if not missing_modules:
        return 'Try $ wisteria --checkup then $ wisteria --cmp="pickle against marshal". ' \
            'The results appear in the console and ' \
            'are also written in a file, ' \
            f'\'{DEFAULT_REPORTFILE_NAME}\' ({normpath(DEFAULT_REPORTFILE_NAME)}), ' \
            'and - if matplotlib is installed - graphs are written in files named ' \
            f'{help_graphsfilenames()}.'

    return "\n\nERROR !\nBEWARE, MISSING REQUIRED PACKAGAGES ! " \
        "THE PROGRAM CAN'T BE EXECUTED WITHOUT THE FOLLOWING PACKAGE(S): " \
        f"{tuple(missing_modules)}; " \
        f"current Python version: {get_python_version()}"


def help_graphsfilenames():
    """
        help_graphsfilenames()

        Return a message describing where graphs files would be written
        on disk.
        _______________________________________________________________________

        RETURNED VALUE: (str)an help message
    """
    file1 = os.path.join(REPORTFILE_PATH,
                         GRAPHS_GENERIC_FILENAME.replace('__SUFFIX__', '1'))
    file2 = os.path.join(REPORTFILE_PATH,
                         GRAPHS_GENERIC_FILENAME.replace('__SUFFIX__', '2'))
    return f"'{file1}' " \
        f"({normpath(file1)}), " \
        f"'{file2}' " \
        f"({file2}), " \
        "and so on"
