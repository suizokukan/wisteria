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
    Wisteria project : tests/cwc_pgnreader_default.py

    Test of wisteria/cwc/pgnreader/default.py

    ___________________________________________________________________________

    o  CWCPgnreader class
"""
import os
import os.path
import unittest

# Pylint is wrong: we can import wisteria.cwc.pgnreader.cwc_default.
#   pylint: disable=import-error, no-name-in-module
from wisteria.cwc.pgnreader.cwc_default import ChessGames
from wisteria.dmfile import DMFile


FINAL_POSITIONS = {
    "game1.pgn":
    "________\n"
    "________\n"
    "____♖_♟_\n"
    "__♚___♟_\n"
    "_♟____♙_\n"
    "_♙_♝_♙__\n"
    "___♔_♞__\n"
    "________",

    "game2.pgn":
    "_______♕\n"
    "_♝_♚♝___\n"
    "♟__♟♟___\n"
    "_____♙__\n"
    "♟_♛♘____\n"
    "♙____♙__\n"
    "_♙♙_____\n"
    "_♔_♖____",

    "game3.pgn":
    "________\n"
    "__♟__♟__\n"
    "_♟_____♟\n"
    "___♔_♙__\n"
    "♙_____♞_\n"
    "_♚___♗__\n"
    "_______♟\n"
    "________",

    "game4.pgn":
    "♝_♜_♛♜♞_\n"
    "______♚_\n"
    "__♟_♟♞_♟\n"
    "__♙__♟♟_\n"
    "__♘♙____\n"
    "_♕___♙♗_\n"
    "♙♙♗___♙♙\n"
    "___♖♖_♔_",

    "game5.pgn":
    "___♚____\n"
    "___♕____\n"
    "____♔___\n"
    "________\n"
    "________\n"
    "________\n"
    "________\n"
    "________",

    "game10.pgn":
    "♜_♝♛_♜♚_\n"
    "___♞♝♟♟♟\n"
    "__♟♟_♞__\n"
    "_♟__♟___\n"
    "___♙♙___\n"
    "_♗___♘_♙\n"
    "♙♙___♙♙_\n"
    "♖♘♗♕♖_♔_",

    "game11.pgn":
    "♜_♝♛_♜♚_\n"
    "___♞♝♟♟♟\n"
    "__♟♟_♞__\n"
    "_♟__♟___\n"
    "___♙♙___\n"
    "_♗___♘_♙\n"
    "♙♙___♙♙_\n"
    "♖♘♗♕♖_♔_",
    }


class CWCPgnreader(unittest.TestCase):
    """
        CWCPgnreader class

        Test of wisteria/cwc/pgnreader/default.py

        _______________________________________________________________________

        o  test_read_pgngames(self)
        o  test_read_game1pgn_tags(self)
        o  test_read_game1xpgn(self)
        o  test_read_game5xpgn(self)
        o  test_read_pgngames2(self)
        o  test_readwrite_pgngames(self)
    """

    def test_read_pgngames(self):
        """
            CWCPgnreader.test_read_pgngames()
        """
        for pgnfilename, finalposition in FINAL_POSITIONS.items():
            games = ChessGames()
            with open(os.path.join("tests", pgnfilename), encoding="utf-8") as src:
                self.assertTrue(games.read_pgn(src))
                self.assertEqual(games[0].board.human_repr(), finalposition)

    def test_read_game1pgn_tags(self):
        """
            CWCPgnreader.test_read_game1pgn_tags()
        """
        games = ChessGames()
        with open(os.path.join("tests", "game1.pgn"), encoding="utf-8") as src:
            self.assertTrue(games.read_pgn(src))
            self.assertEqual(games[0].chessgame_tags["Black"], "Spassky, Boris V.")

    def test_read_game1xpgn(self):
        """
            CWCPgnreader.test_read_game1xpgn()
        """
        games = ChessGames()
        with open(os.path.join("tests", "game1x.pgn"), encoding="utf-8") as src:
            self.assertFalse(games.read_pgn(src))

    def test_read_game5xpgn(self):
        """
            CWCPgnreader.test_read_game5xpgn()
        """
        games = ChessGames()
        with open(os.path.join("tests", "game5x.pgn"), encoding="utf-8") as src:
            self.assertFalse(games.read_pgn(src))

    def test_read_pgngames2(self):
        """
            CWCPgnreader.test_read_pgngames2()
        """
        games = ChessGames()
        for pgnfilename in ('game6.pgn', 'game7.pgn', 'game8.pgn', 'game9.pgn'):
            with open(os.path.join("tests", pgnfilename), encoding="utf-8") as src:
                self.assertTrue(games.read_pgn(src))
                self.assertEqual(games[0].board.human_repr(),
                                 FINAL_POSITIONS['game3.pgn'])
                self.assertEqual(games[1].board.human_repr(),
                                 FINAL_POSITIONS['game4.pgn'])

    def test_readwrite_pgngames(self):
        """
            CWCPgnreader.test_readwrite_pgngames()
        """
        for pgnfilename in ('game1.pgn',
                            'game2.pgn',
                            'game3.pgn',
                            'game4.pgn',
                            'game5.pgn',
                            'game6.pgn',
                            'game7.pgn',
                            'game8.pgn',
                            'game9.pgn',
                            'game10.pgn',
                            'game11.pgn'):

            # wisteria being a Python3.8+ project, no parenthesized context managers is available.
            # NB: both DMFile-s are in-memory files
            with \
                open(os.path.join("tests", pgnfilename), encoding="utf-8") as src, \
                DMFile(":tests_tmp1.pgn:") as tmpfile1, \
                DMFile(":tests_tmp2.pgn:") as tmpfile2:

                games = ChessGames()
                self.assertTrue(games.read_pgn(src))
                games.write_pgn(tmpfile1)
                games = ChessGames()
                self.assertTrue(games.read_pgn(tmpfile1))

                if pgnfilename in FINAL_POSITIONS:
                    self.assertTrue(games[0].board.human_repr(),
                                    FINAL_POSITIONS[pgnfilename])

                games.write_pgn(tmpfile2)

                self.assertEqual(tmpfile1.read(), tmpfile2.read())
