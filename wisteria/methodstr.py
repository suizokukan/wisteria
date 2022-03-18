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
    Wisteria project : wisteria/methodstr.py

    parse_methodstr() function, required to parse --method argument.

    ___________________________________________________________________________

    o  parse_methodstr()
"""


def parse_methodstr(methodstr):
    """
        parse_methodstr()

        Parse the --method string <methodstr>.

        (pimydoc)methodstr
TODO
        _______________________________________________________________________

        ARGUMENT: (str)methodstr

        RETURNED VALUE: (bool)                  success,
                        (int)                   totaliterations
                        (None|int)              shuffle seed,
                        (None|list of int/str)  elems
    """
    shuffleseed = None
    elems = []

    # ---- shuffle seed ----
    if methodstr.startswith("(shuffle="):
        if ")" not in methodstr:
            return False, None, None, None
        try:
            shuffleseed = int(methodstr[len("(shuffle="):methodstr.index(")")])
            methodstr = methodstr[methodstr.index(")")+1:]
        except ValueError:
            # shuffle seed is not an integer !
            return False, None, None, None

    # ---- totaliterations ----
    if "x" not in methodstr:
        return False, None, None, None
    try:
        totaliterations = int(methodstr[1:methodstr.index(":")])
        methodstr = methodstr[methodstr.index(":")+1:]
    except ValueError:
        # totaliterations is not an integer !
        return False, None, None, None

    # ---- elements ----
    for elem in methodstr.split(";"):
        if elem == "rp":
            elems.append("rp")
        elif elem == "RP":
            elems.append("RP")
        elif elem == "p1":
            elems.append("p1")
        elif elem == "p10":
            elems.append("p10")
        elif elem == "p100":
            elems.append("p100")
        else:
            try:
                elems.append(int(elem))

                if int(elem) == 0:
                    # forbidden value
                    return False, None, None
            except ValueError:
                # given value isn't an integer !
                return False, None, None, None

    return True, totaliterations, shuffleseed, elems
