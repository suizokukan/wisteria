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
    codesearch.py

        Search a string in the project's files.

        See codesearch.py --help for more informations.
"""
import argparse
import subprocess
import sys

VERSION = "codesearch.py v.4/2021-08-26"


def read_command_line_arguments():
    """
        read_command_line_arguments()

        Read the command line arguments.
        ________________________________________________________________________


        RETURNED VALUE
                return the argparse object.
    """
    parser = argparse.ArgumentParser(
        description="Search a string in all directories",
        epilog=VERSION,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('--version', '-v',
                        action='version',
                        version=f"{VERSION}",
                        help="Show the version and exit")

    parser.add_argument(
        "string",
        action="store",
        help="string to be found",
    )

    parser.add_argument(
        "--codesubdirectoryonly",
        action="store_true",
        default=False,
        help="Search only in the code subdirectory",
    )

    parser.add_argument(
        "--exclude",
        action="store",
        required=False,
        default="",
        help='The syntax is tricky ! Different paths may be added : they are separated '
             'by a semicolon. Add a whole directory by adding /* to its path. '
             'Files in the root directory must preceded by the two characters ./ .'
             'Use quotation mark around the whole string.'
             'E.g. --exclude='
             '"wisteria/pyside2/*;./check_code_quality.sh"'
    )
    return parser.parse_args()


ARGS = read_command_line_arguments()

# By example:
#
# subprocess.run(('find', 'wisteria', '-type', 'f',
#                 '-name', '*.py',
#                '!', '-path', 'wisteria/pyside2/*',
#                '!', '-path', 'wisteria/error_messages.py',
#                 '-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'))
EXCLUDE_ARG = []
for exclude_path in ARGS.exclude.split(";"):
    EXCLUDE_ARG.append("!")
    EXCLUDE_ARG.append("-path")
    EXCLUDE_ARG.append(exclude_path)

try:
    # wisteria/ : .py files
    subprocess.run(['find', 'wisteria', '-type', 'f', '-name', '*.py', ] +
                   EXCLUDE_ARG +
                   ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
                   check=True)

    if not ARGS.codesubdirectoryonly:
        # # tests/ : .py files
        # subprocess.run(['find', 'tests', '-type', 'f', '-name', '*.py', ] +
        #                EXCLUDE_ARG +
        #                ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
        #                check=True)

        # root directory : .py files
        subprocess.run(['find', '.', '-maxdepth', '1', '-type', 'f', '-name', '*.py', ] +
                       EXCLUDE_ARG +
                       ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
                       check=True)

        # root directory : .sh files
        subprocess.run(['find', '.', '-maxdepth', '1', '-type', 'f', '-name', '*.sh', ] +
                       EXCLUDE_ARG +
                       ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
                       check=True)

        # root directory : .ini files
        subprocess.run(['find', '.', '-maxdepth', '1', '-type', 'f', '-name', '*.ini', ] +
                       EXCLUDE_ARG +
                       ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
                       check=True)

        # root directory : .md files
        subprocess.run(['find', '.', '-maxdepth', '1', '-type', 'f', '-name', '*.md', ] +
                       EXCLUDE_ARG +
                       ['-exec', 'grep', '-rHn', '--color', ARGS.string, '{}', ';'],
                       check=True)

        # root directory : pimydoc file
        subprocess.run(['grep', '-rHn', '--color', ARGS.string, 'pimydoc'],
                       check=True)

except subprocess.CalledProcessError:
    sys.exit(255)

sys.exit(0)
