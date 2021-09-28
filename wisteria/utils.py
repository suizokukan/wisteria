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

    o  normpath(path)
    o  shortenedstr(string, maximallength)
    o  trytoimport(module_name)
"""
import importlib
import os
import os.path

import wisteria.globs
from wisteria.globs import VERBOSITY_DETAILS
from wisteria.msg import msginfo


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


def trytoimport(module_name):
    """
        trytoimport()

        Try to import <module_name> module.
        _______________________________________________________________________

        ARGUMENT:
        o  (str)module_name: the module to be imported

        RETURNED VALUE: (bool)success
    """
    res = True
    try:
        wisteria.globs.MODULES[module_name] = importlib.import_module(module_name)
        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo(f"Module '{module_name}' successfully imported.")
    except ModuleNotFoundError:
        res = False
    return res
