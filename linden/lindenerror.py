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
    lindenerror.py

    Definition of the LindenError class, the unique error class that should be
    raised by the project.

    ___________________________________________________________________________

    o  LindenError
"""


class LindenError(Exception):
    """
        LindenError class

        Unique exception raised by the program.
    """
