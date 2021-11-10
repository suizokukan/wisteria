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
    Wisteria project : tests/cwc_utils__tests.py

    Test of wisteria/cwc/cwc_utils.py

    ___________________________________________________________________________

    o  CWCUtils class
"""
import unittest

# Pylint is wrong: we can import wisteria.cwc.cwc_utils.
#   pylint: disable=import-error, no-name-in-module
from wisteria.cwc.cwc_utils import count_dataobjs_number_without_cwc_variant


class CWCUtils(unittest.TestCase):
    """
        CWCUtils class

        Test of wisteria/cwc/cwc_utils.py

        _______________________________________________________________________

        o  test_count_dataobjs_number_without_cwc_variant(self)
    """
    def test_count_dataobjs_number_without_cwc_variant(self):
        """
            CWCUtils.test_count_dataobjs_number_without_cwc_variant()

            test of count_dataobjs_number_without_cwc_variant()
        """
        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {}),
                         0)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"str": None, "int": None, }),
                         2)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "int": None, }),
                         2)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "int": None, }),
                         2)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None, }),
                         1)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "wisteria.cwc.pgnreader.xyz.ChessGames": None,
             "int": None, }),
                         2)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.chessplayer.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "int": None, }),
                         3)

        self.assertEqual(count_dataobjs_number_without_cwc_variant(
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.chessplayer.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "wisteria.cwc.chessplayer.iaswn.ChessGames": None,
             "int": None, }),
                         3)
