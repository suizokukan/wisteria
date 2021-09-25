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
    utils.py

    ___________________________________________________________________________

    o  shortenedstr(string, maximallength)
"""


def shortenedstr(string,
                 maximallength=40):
    """
        This function reduces a <string> so that the maximum length of the returned
        string is equal to <maximallength>.
    """
    # ---- nothing to do, <string> isn't too long. ----------------------------
    if len(string) <= maximallength:
        return string

    # ---- We have to reduce <string>. ----------------------------------------
    suffix = "[…]"

    # a special case: <maximallength> is really too short !
    if len(suffix) > maximallength:
        return string

    # e.g. if maximallength==10, if string="01234567890"(len=11)  > "0123456[…]" (len=10)
    # e.g. if maximallength==10, if string="012345678901"(len=12) > "0123456[…]" (len=10)
    return string[:maximallength-len(suffix)] + suffix
