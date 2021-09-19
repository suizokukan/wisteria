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
    linden/globs.py

    Global variables.

    ___________________________________________________________________________

    o  VERBOSITY_MINIMAL
    o  VERBOSITY_NORMAL
    o  VERBOSITY_DETAILS
    o  VERBOSITY_DEBUG

    o  ARGS

    o  TIMEITNUMBER

    o  TMPFILENAME

    o  REGEX_CMP
    o  REGEX_CMP__HELP
"""
import re


VERBOSITY_MINIMAL = 0
VERBOSITY_NORMAL = 1
VERBOSITY_DETAILS = 2
VERBOSITY_DEBUG = 3

ARGS = None

TIMEITNUMBER = 10  # TODO !

TMPFILENAME = "linden.tmp"

REGEX_CMP = re.compile("^\s*(?P<serializer1>[^\s\(\)]+)((\svs\s|\sversus\s|\sagainst\s)(?P<serializer2>[^\s\(\)]+))?(\s*\((?P<data>all|cwc|ini)\))?\s*$")
REGEX_CMP__HELP = "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

REPORT_MINIMAL_STRING = "C;"
REPORT_FULL_STRING = "titles;A;B1a;B1b;B2a;B2b;C1b;C2b;"

