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
import unittest

from wisteria.cwc.pgnreader.default import ChessGames


class CWCPgnreader(unittest.TestCase):
    """
        CWCPgnreader class

        Test of wisteria/cwc/pgnreader/default.py

        _______________________________________________________________________

        o  test_game1pgn(self)
        o  test_game2pgn(self)
        o  test_game3pgn(self)
        o  test_game4pgn(self)
        o  test_game5pgn(self)
        o  test_game6pgn(self)
        o  test_game7pgn(self)
        o  test_game8pgn(self)
        o  test_game9pgn(self)
    """

    def test_game1pgn(self):
        """
            CWCPgnreader.test_game1pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game1.pgn"))
        self.assertEqual(games[0].chess_event["Black"], "Spassky, Boris V.")
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "________\n"
                         "____♖_♟_\n"
                         "__♚___♟_\n"
                         "_♟____♙_\n"
                         "_♙_♝_♙__\n"
                         "___♔_♞__\n"
                         "________")

        games = ChessGames()
        self.assertFalse(games.read_pgn("tests/game1x.pgn"))

    def test_game2pgn(self):
        """
            CWCPgnreader.test_game2pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game2.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "_______♕\n"
                         "_♝_♚♝___\n"
                         "♟__♟♟___\n"
                         "_____♙__\n"
                         "♟_♛♘____\n"
                         "♙____♙__\n"
                         "_♙♙_____\n"
                         "_♔_♖____")

    def test_game3pgn(self):
        """
            CWCPgnreader.test_game3pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game3.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "__♟__♟__\n"
                         "_♟_____♟\n"
                         "___♔_♙__\n"
                         "♙_____♞_\n"
                         "_♚___♗__\n"
                         "_______♟\n"
                         "________")

    def test_game4pgn(self):
        """
            CWCPgnreader.test_game4pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game4.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "♝_♜_♛♜♞_\n"
                         "______♚_\n"
                         "__♟_♟♞_♟\n"
                         "__♙__♟♟_\n"
                         "__♘♙____\n"
                         "_♕___♙♗_\n"
                         "♙♙♗___♙♙\n"
                         "___♖♖_♔_")

    def test_game5pgn(self):
        """
            CWCPgnreader.test_game5pgn()

            About game5.pgn and game5x.pgn, see:
                http://blog.mathieuacher.com/LongestChessGame/
        """
        games = ChessGames()
        self.assertFalse(games.read_pgn("tests/game5x.pgn"))

        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game5.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "___♚____\n"
                         "___♕____\n"
                         "____♔___\n"
                         "________\n"
                         "________\n"
                         "________\n"
                         "________\n"
                         "________")

    def test_game6pgn(self):
        """
            CWCPgnreader.test_game6pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game6.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "__♟__♟__\n"
                         "_♟_____♟\n"
                         "___♔_♙__\n"
                         "♙_____♞_\n"
                         "_♚___♗__\n"
                         "_______♟\n"
                         "________")

        self.assertEqual(games[1].gameboard.get_unicode(),
                         "♝_♜_♛♜♞_\n"
                         "______♚_\n"
                         "__♟_♟♞_♟\n"
                         "__♙__♟♟_\n"
                         "__♘♙____\n"
                         "_♕___♙♗_\n"
                         "♙♙♗___♙♙\n"
                         "___♖♖_♔_")

    def test_game7pgn(self):
        """
            CWCPgnreader.test_game7pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game7.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "__♟__♟__\n"
                         "_♟_____♟\n"
                         "___♔_♙__\n"
                         "♙_____♞_\n"
                         "_♚___♗__\n"
                         "_______♟\n"
                         "________")

        self.assertEqual(games[1].gameboard.get_unicode(),
                         "♝_♜_♛♜♞_\n"
                         "______♚_\n"
                         "__♟_♟♞_♟\n"
                         "__♙__♟♟_\n"
                         "__♘♙____\n"
                         "_♕___♙♗_\n"
                         "♙♙♗___♙♙\n"
                         "___♖♖_♔_")

    def test_game8pgn(self):
        """
            CWCPgnreader.test_game8pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game8.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "__♟__♟__\n"
                         "_♟_____♟\n"
                         "___♔_♙__\n"
                         "♙_____♞_\n"
                         "_♚___♗__\n"
                         "_______♟\n"
                         "________")

        self.assertEqual(games[1].gameboard.get_unicode(),
                         "♝_♜_♛♜♞_\n"
                         "______♚_\n"
                         "__♟_♟♞_♟\n"
                         "__♙__♟♟_\n"
                         "__♘♙____\n"
                         "_♕___♙♗_\n"
                         "♙♙♗___♙♙\n"
                         "___♖♖_♔_")

    def test_game9pgn(self):
        """
            CWCPgnreader.test_game9pgn()
        """
        games = ChessGames()
        self.assertTrue(games.read_pgn("tests/game9.pgn"))
        self.assertEqual(games[0].gameboard.get_unicode(),
                         "________\n"
                         "__♟__♟__\n"
                         "_♟_____♟\n"
                         "___♔_♙__\n"
                         "♙_____♞_\n"
                         "_♚___♗__\n"
                         "_______♟\n"
                         "________")

        self.assertEqual(games[1].gameboard.get_unicode(),
                         "♝_♜_♛♜♞_\n"
                         "______♚_\n"
                         "__♟_♟♞_♟\n"
                         "__♙__♟♟_\n"
                         "__♘♙____\n"
                         "_♕___♙♗_\n"
                         "♙♙♗___♙♙\n"
                         "___♖♖_♔_")
