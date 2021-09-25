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
   Wisteria project : propagate_versionumber.py

   Inject wisteria.aboutproject.__version__ in various files.

   ____________________________________________________________________________

   * pyproject_toml() : Update the version number in the `pyproject.toml` file.
"""
import argparse
import os
import os.path
import re

from wisteria.aboutproject import __version__


VERSION = "propagate_versionumber.py v.3/2021-08-26"
PARSER = \
    argparse.ArgumentParser(description="Inject wisteria.aboutproject.__version__ in various files.",
                            epilog=VERSION,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('--version', '-v',
                    action='version',
                    version=f"{VERSION}",
                    help="Show the version and exit")
ARGS = PARSER.parse_args()


def pyproject_toml():
    """
        pyproject_toml()

        Update the version number in the `pyproject.toml file.

        Inject wisteria.aboutproject::__version__ into the
        `pyproject.toml` file at line :
            version = "..."
    """
    target_filename = "pyproject.toml"

    print(f"* about to update '{target_filename}'...")

    # regex describing the line to be modified:
    regex = '(?P<versionline>^version = "(?P<versionname>.*)")'

    def repl(matchobject):
        """
            repl() sub-function

            Modify the version number in a line defined by regex
        """
        line = matchobject.group("versionline")
        return line[:matchobject.start("versionname")] + \
            __version__ + \
            line[matchobject.end("versionname"):]

    if not os.path.exists(target_filename):
        print("Error : missing pyproject.toml file.")
        return

    # ---- read current file --------------------------------------------------
    new_lines = []  # new lines of the future pyproject.toml file
    with open(target_filename, "r", encoding="utf-8") as current_pyproject_toml:
        for _line in current_pyproject_toml:
            line = _line.strip()

            res = re.search(regex, line)
            if res:
                new_line = re.sub(regex, repl, line)
                new_lines.append(new_line)
                print(f"  > in '{target_filename}', version number is now defined by '{new_line}'.")
            else:
                new_lines.append(line)

    # ---- remove current file ------------------------------------------------
    os.remove(target_filename)

    # ---- write new file -----------------------------------------------------
    with open(target_filename, "w", encoding="utf-8") as new_pyproject_toml:
        for line in new_lines:
            new_pyproject_toml.write(line+"\n")


if __name__ == "__main__":
    pyproject_toml()
