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
    reportaspect.py

    Define some 'aspects' (=some text attributes) for some excepts in report.

    ___________________________________________________________________________

    o  aspect_data(data)
    o  aspect_serializer(serializer)
    o  aspect_title(title)
"""


def aspect_data(data):
    """
        aspect_data()

        Modify the aspect of (str)data.

        _______________________________________________________________________

        ARGUMENT: (str)data

        RETURNED VALUE: (str)data + some text attributes.
    """
    return f"[bold white]{data}[/bold white]"


def aspect_serializer(serializer):
    """
        aspect_serializer()

        Modify the aspect of (str)serializer.

        _______________________________________________________________________

        ARGUMENT: (str)serializer

        RETURNED VALUE: (str)serializer + some text attributes.
    """
    return f"[yellow]{serializer}[/yellow]"


def aspect_title(title):
    """
        aspect_title()

        Modify the aspect of (str)title.

        _______________________________________________________________________

        ARGUMENT: (str)title

        RETURNED VALUE: (str)title + some text attributes.
    """
    return f"[bold white on blue]{title}[/bold white on blue]"
