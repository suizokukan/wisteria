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
import filecmp
import os
import os.path
import unittest

# Pylint is wrong: we can import wisteria.cwc.pgnreader.default.
# pylint: disable=import-error, no-name-in-module
from wisteria.cwc.pgnreader.default import ChessGames

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
            self.assertTrue(games.read_pgn(os.path.join("tests", pgnfilename)))
            self.assertEqual(games[0].board.human_repr(), finalposition)

    def test_read_game1pgn_tags(self):
        """
            CWCPgnreader.test_read_game1pgn_tags()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn(os.path.join("tests", "game1.pgn")))
        self.assertEqual(games[0].chessgame_tags["Black"], "Spassky, Boris V.")

    def test_read_game1xpgn(self):
        """
            CWCPgnreader.test_read_game1xpgn()
        """

        games = ChessGames()
        self.assertFalse(games.read_pgn("tests/game1x.pgn"))

    def test_read_game5xpgn(self):
        """
            CWCPgnreader.test_read_game5xpgn()
        """
        games = ChessGames()
        self.assertFalse(games.read_pgn("tests/game5x.pgn"))

    def test_read_pgngames2(self):
        """
            CWCPgnreader.test_read_pgngames2()
        """
        games = ChessGames()
        for pgnfilename in ('game6.pgn', 'game7.pgn', 'game8.pgn', 'game9.pgn'):
            self.assertTrue(games.read_pgn(os.path.join("tests", pgnfilename)))
            self.assertEqual(games[0].board.human_repr(),
                             FINAL_POSITIONS['game3.pgn'])
            self.assertEqual(games[1].board.human_repr(),
                             FINAL_POSITIONS['game4.pgn'])

    def test_readwrite_pgngames(self):
        """
            CWCPgnreader.test_readwrite_pgngames()
        """
        tmpfile1 = os.path.join("tests", "tests_tmp1.pgn")
        tmpfile2 = os.path.join("tests", "tests_tmp2.pgn")

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
            games = ChessGames()
            games.read_pgn(os.path.join("tests", pgnfilename))
            games.write_pgn(tmpfile1)
            games = ChessGames()
            games.read_pgn(tmpfile1)

            if pgnfilename in FINAL_POSITIONS:
                self.assertTrue(games[0].board.human_repr(),
                                FINAL_POSITIONS[pgnfilename])
                
            games.write_pgn(tmpfile2)

            self.assertTrue(filecmp.cmp(tmpfile1, tmpfile2, shallow=False))

        os.remove(tmpfile1)
        os.remove(tmpfile2)
