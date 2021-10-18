"""
PGN reader/writer; regular chess only; no sophisticated rules (castling, en passant: ok)

La validation d'un coup n'est jamais vérifiée; elle est supposée vraie.
Les données autres que la liste des coups, event, noms des joueurs et date sont
complètement laissés de côté

L'idée est de voir comment sérialiser un objet aussi complexe qu'une partie d'échecs, permettant
de sauver la partie sous un double format: PNG + dump du serializer. Il faut pouvoir rejouer
la partie coup après coup.

(A) pas de structure optimisée (array), pas de datetime.
(B) structure optimisée + datetime


TODO:
notation algébrique: e6-e4 // e6e4 // e4 / Rd3xd7 // Qh4e1
- revoir la regex.
- status: white_king already moved
- revoir ChessGame.regex pour events, ... : remplacer les attributs (.event, ...) par un dictionnaire

https://fr.chesstempo.com/pgn-viewer/
https://theweekinchess.com/a-year-of-pgn-game-files
"""
import re


COLOR_NOCOLOR = 0
COLOR_WHITE = 1
COLOR_BLACK = 2

PIECENATURE_NOPIECE = 0
PIECENATURE_PAWN = 1
PIECENATURE_ROOK = 2
PIECENATURE_KNIGHT = 3
PIECENATURE_BISHOP = 4
PIECENATURE_QUEEN = 5
PIECENATURE_KING = 6
PIECENATURE2ALGEBRICNOTATION =  {
    PIECENATURE_ROOK: 'R',
    PIECENATURE_KNIGHT: 'N',
    PIECENATURE_BISHOP: 'B',
    PIECENATURE_QUEEN: 'Q',
    PIECENATURE_KING: 'K'}
ALGEBRICNOTATION2PIECENATURE = {value: key for key, value in PIECENATURE2ALGEBRICNOTATION.items()}

CHESSRESULT_UNDEFINED = 0
CHESSRESULT_DRAW = 1
CHESSRESULT_WHITEWINS = 2
CHESSRESULT_BLACKWINS = 3

MOVETYPE_SINGLE = 0
MOVETYPE_CASTLING_OO = 1
MOVETYPE_CASTLING_OOO = 2
MOVETYPE_ENPASSANT = 3

class ChessResult:
    def __init__(self,
                 chessresult=CHESSRESULT_UNDEFINED):
        self.result = chessresult


class ChessPlayer:
    def __init__(self,
                 name="unknown"):
        self.name = name


class ChessEvent(dict):
    def __init__(self,
                 datadict=None):
        dict.__init__(self)
        if datadict:
            for key, value in datadict:
                self[key] = value


class ChessPiece:
    piece2unicode = {
        (PIECENATURE_NOPIECE, COLOR_NOCOLOR): '_',
        (PIECENATURE_PAWN, COLOR_WHITE): '♙',
        (PIECENATURE_PAWN, COLOR_BLACK): '♟',
        (PIECENATURE_ROOK, COLOR_WHITE): '♖',
        (PIECENATURE_ROOK, COLOR_BLACK): '♜',
        (PIECENATURE_KNIGHT, COLOR_WHITE): '♘',
        (PIECENATURE_KNIGHT, COLOR_BLACK): '♞',
        (PIECENATURE_BISHOP, COLOR_WHITE): '♗',
        (PIECENATURE_BISHOP, COLOR_BLACK): '♝',
        (PIECENATURE_QUEEN, COLOR_WHITE): '♕',
        (PIECENATURE_QUEEN, COLOR_BLACK): '♛',
        (PIECENATURE_KING, COLOR_WHITE): '♔',
        (PIECENATURE_KING, COLOR_BLACK): '♚',
        }
    unicode2piece = {value: key for key, value in piece2unicode.items()}

    def __eq__(self,
               other):
        return self.color == other.color and self.nature == other.nature

    def __init__(self,
                 color=COLOR_NOCOLOR,
                 nature=PIECENATURE_NOPIECE):
        self.color = color
        self.nature = nature

    def __repr__(self):
        return f"(ChessPiece: {self.color=}; {self.nature=})"

    def get_unicode(self):
        return ChessPiece.piece2unicode[self.nature, self.color]

    def init_from_unicode_string(self,
                              string):
        self.nature, self.color = ChessPiece.unicode2piece[string]
        return self

    def is_empty(self):
        return self.color==COLOR_NOCOLOR and self.nature==PIECENATURE_NOPIECE


class ChessMove:
    def __init__(self,
                 beforeafter_coord_piece1,
                 beforeafter_coord_piece2=None,
                 beforeafter_advpiece=None,
                 movetype=MOVETYPE_SINGLE,
                 promotion=None,
                 validmove=True):
        self.movetype = movetype
        self.beforeafter_coord_piece1 = beforeafter_coord_piece1
        self.beforeafter_coord_piece2 = beforeafter_coord_piece2
        self.beforeafter_advpiece = beforeafter_advpiece
        self.validmove = validmove

    def __repr__(self):
        return f"{self.movetype=}; {self.beforeafter_coord_piece1=}; {self.beforeafter_coord_piece2}; " \
            f"{self.beforeafter_advpiece=}; {self.validmove=}"


class ChessListOfMoves(list):
    def __init__(self):
        list.__init__(self)
        self.next_player = COLOR_WHITE
        self.doublemove_number = 1

    def add_move(self, move):
        """This move is played by self.next_player"""
        self.append((self.doublemove_number, self.next_player, move))

        if self.next_player == COLOR_WHITE:
            self.next_player = COLOR_BLACK
        else:
            self.next_player = COLOR_WHITE
            self.doublemove_number += 1

    def who_plays(self):
        return self.next_player


class ChessPiecesStatus:
    # TODO: est-ce que les rois ont bougé ?
    pass

class ChessBoard:
    def __init__(self):
        self.moves = []
        self.board = {}
        self.pieces_status = ChessPiecesStatus()

        for x in range(8):
            for y in range(8):
                self.set_xy(x, y, ChessPiece())

        self.init_from_unicode_string("♜♞♝♛♚♝♞♜" \
                                   "♟♟♟♟♟♟♟♟" \
                                   "________" \
                                   "________" \
                                   "________" \
                                   "________" \
                                   "♙♙♙♙♙♙♙♙" \
                                   "♖♘♗♕♔♗♘♖")

    def get_king_coord(self, color):
        """Return the (x, y) of the <color>(white/black) king"""
        for x in range(0, 8):
            for y in range(0, 8):
                obj = self.get_xy(x, y)
                if obj.nature == PIECENATURE_KING and \
                   obj.color == color:
                    return (x, y)
        return None  # error: no king !

    def get_unicode(self):
        res = []
        for y in range(8):
            res.append("".join(self.get_xy(x, y).get_unicode() for x in range(8)))
        return "\n".join(res)

    def get_xy(self,
               x,
               y):
        return self.board[(x, y)]

    def init_from_unicode_string(self,
                              string):
        index = 0
        for y in range(8):
            for x in range(8):
                self.set_xy(x, y, ChessPiece().init_from_unicode_string(string[index]))
                index += 1

    def is_empty_or_is_this_piece(self,
                                  x,
                                  y,
                                  piece):
        """return True if [x, y] is an empty square OR if [x, y] is <piece>"""
        obj = self.get_xy(x, y)
        return obj.is_empty() or obj == piece

    def set_xy(self,
               x,
               y,
               value):
        self.board[(x, y)] = value

    def set_xy_empty(self,
                     x,
                     y):
        self.set_xy(x, y, ChessPiece())

    def update_by_playing_a_move(self,
                                 move):
        """Modify <self> by playing a <move>."""
        if move.movetype == MOVETYPE_SINGLE:
            before, after = move.beforeafter_coord_piece1
            piece = self.get_xy(before[0], before[1])
            self.set_xy_empty(before[0], before[1])
            self.set_xy(after[0], after[1], piece)
        elif move.movetype in (MOVETYPE_CASTLING_OO, MOVETYPE_CASTLING_OOO):
            # king:
            before, after = move.beforeafter_coord_piece1
            piece = self.get_xy(before[0], before[1])
            self.set_xy_empty(before[0], before[1])
            self.set_xy(after[0], after[1], piece)
            # rook:
            before, after = move.beforeafter_coord_piece2
            piece = self.get_xy(before[0], before[1])
            self.set_xy_empty(before[0], before[1])
            self.set_xy(after[0], after[1], piece)
        else:
            raise NotImplementedError

    def which_piece_could_go_to(self,
                                piece,
                                coord_after,
                                movetype):
        """
        d'où vient le pion qui va arriver en <coord_after> ? coord_after: (2, 3)

        More than one result may be returned !
        """
        print("@@@", piece, coord_after, movetype)
        x, y = coord_after
        res = []  # there should be only one result; see the end of this function.

        def add_to_res_if_rightpiece(x, y, piece):
            if 0 <= x <= 7 and \
               0 <= y <= 7 and \
               self.get_xy(x, y)==piece:
                res.append((x, y))

        if piece.nature == PIECENATURE_PAWN:
            if movetype == MOVETYPE_SINGLE:
                if piece.color == COLOR_WHITE:
                    if y==4 and self.get_xy(x, y+1).is_empty():
                        add_to_res_if_rightpiece(x, y+2, piece)
                    else:
                        add_to_res_if_rightpiece(x, y+1, piece)
                else:  # piece.color == COLOR_BLACK
                    if y==3 and self.get_xy(x, y-1).is_empty():
                        add_to_res_if_rightpiece(x, y-2, piece)
                    else:
                        add_to_res_if_rightpiece(x, y-1, piece)
            else:
                raise NotImplementedError
        elif piece.nature == PIECENATURE_KNIGHT:
            if movetype == MOVETYPE_SINGLE:
                add_to_res_if_rightpiece(x-2, y-1, piece)
                add_to_res_if_rightpiece(x-2, y+1, piece)
                add_to_res_if_rightpiece(x+2, y-1, piece)
                add_to_res_if_rightpiece(x+2, y+1, piece)
                add_to_res_if_rightpiece(x-1, y-2, piece)
                add_to_res_if_rightpiece(x-1, y+2, piece)
                add_to_res_if_rightpiece(x+1, y-2, piece)
                add_to_res_if_rightpiece(x+1, y+2, piece)
            else:
                raise NotImplementedError
        elif piece.nature == PIECENATURE_BISHOP:
            for deltax, deltay in ((+1, -1), (+1, +1), (-1, +1), (-1, -1)):  # 4 diagonals to check
                for delta in range(1, 8):
                    if ChessBoard.xy_is_off_the_board(x+(deltax*delta), y+(deltay*delta)) or \
                       self.is_empty_or_is_this_piece(x+(deltax*delta), y+(deltay*delta), piece) is False:
                        # A piece (different from <piece>) was encountered on the diagonal or
                        # we were about to go off the board:
                        break
                    if self.get_xy(x+(deltax*delta), y+(deltay*delta))==piece:
                        res.append((x+(deltax*delta), y+(deltay*delta)))
        elif piece.nature == PIECENATURE_ROOK:
            for deltax, deltay in ((0, -1), (0, +1), (-1, 0), (+1, 0)):  # 4 columns/rows to check
                for delta in range(1, 8):
                    if ChessBoard.xy_is_off_the_board(x+(deltax*delta), y+(deltay*delta)) or \
                       self.is_empty_or_is_this_piece(x+(deltax*delta), y+(deltay*delta), piece) is False:
                        # A piece (different from <piece>) was encountered on the diagonal or
                        # we were about to go off the board:
                        break
                    if self.get_xy(x+(deltax*delta), y+(deltay*delta))==piece:
                        res.append((x+(deltax*delta), y+(deltay*delta)))

        else:
            raise NotImplementedError

        return res

    @staticmethod
    def xy_is_off_the_board(x,
                            y):
        return not ((0 <= x <= 7) and (0 <= y <= 7))


class ChessGame:
    regex_pgn_tags = re.compile('^\s*\[(?P<key>.+)\s+\"(?P<value>.+)\"\]$')

    regex_pgn_listofmoves = {'doublemovenumber': re.compile('[\d]+\.\s'),
                             }

    regex_simplemove_algebraicnotation = re.compile(
        "^"
        "(?P<str_piecenature>[KQNRB])?"
        "(?P<str_intersymb>[x|\-])?"
        "(?P<str_coord_x1>[a-h]|[1-8]|[a-h][1-8])"
        "(=(?P<str_promotion>[KQNRB]))?"
        "$")
    regex_simplemove_algebraicnotation2 = re.compile(
        "^"
        "(?P<str_piecenature>[KQNRB])?"
        "(?P<str_coord_x0>[a-h][1-8]|[a-h]|[1-8])?"
        "(?P<str_intersymb>[x|\-])?"
        "(?P<str_coord_x1>[a-h][1-8]|[a-h]|[1-8])"
        "(=(?P<str_promotion>[KQNRB]))?"
        "$")

    strcoord2coord = {
        'a8': (0, 0), 'b8': (1, 0), 'c8': (2, 0), 'd8': (3, 0),
        'e8': (4, 0), 'f8': (5, 0), 'g8': (6, 0), 'h8': (7, 0),
        'a7': (0, 1), 'b7': (1, 1), 'c7': (2, 1), 'd7': (3, 1),
        'e7': (4, 1), 'f7': (5, 1), 'g7': (6, 1), 'h7': (7, 1),
        'a6': (0, 2), 'b6': (1, 2), 'c6': (2, 2), 'd6': (3, 2),
        'e6': (4, 2), 'f6': (5, 2), 'g6': (6, 2), 'h6': (7, 2),
        'a5': (0, 3), 'b5': (1, 3), 'c5': (2, 3), 'd5': (3, 3),
        'e5': (4, 3), 'f5': (5, 3), 'g5': (6, 3), 'h5': (7, 3),
        'a4': (0, 4), 'b4': (1, 4), 'c4': (2, 4), 'd4': (3, 4),
        'e4': (4, 4), 'f4': (5, 4), 'g4': (6, 4), 'h4': (7, 4),
        'a3': (0, 5), 'b3': (1, 5), 'c3': (2, 5), 'd3': (3, 5),
        'e3': (4, 5), 'f3': (5, 5), 'g3': (6, 5), 'h3': (7, 5),
        'a2': (0, 6), 'b2': (1, 6), 'c2': (2, 6), 'd2': (3, 6),
        'e2': (4, 6), 'f2': (5, 6), 'g2': (6, 6), 'h2': (7, 6),
        'a1': (0, 7), 'b1': (1, 7), 'c1': (2, 7), 'd1': (3, 7),
        'e1': (4, 7), 'f1': (5, 7), 'g1': (6, 7), 'h1': (7, 7),

        'a': (0, None), 'b': (1, None), 'c': (2, None), 'd': (3, None),
        'e': (4, None), 'f': (5, None), 'g': (6, None), 'h': (7, None),

        '0': (None, 0), '1': (None, 1), '2': (None, 2), '3': (None, 3),
        '4': (None, 4), '5': (None, 5), '6': (None, 6), '7': (None, 7),
        }
    coord2strcoord = {value: key for key, value in strcoord2coord.items()}

    def __init__(self,
                 white_player=ChessPlayer(),
                 black_player=ChessPlayer(),
                 chess_event=ChessEvent(),
                 gameboard=ChessBoard(),
                 result=ChessResult()):
        self.white_player = white_player
        self.black_player = black_player
        self.chess_event = chess_event
        self.gameboard = gameboard
        self.result = result
        self.listofmoves = ChessListOfMoves()

    def read_pgn(self,
                 pgnfilename):
        self.listofmoves = ChessListOfMoves()

        str_listofmoves = []
        with open(pgnfilename) as src:
            for _line in src:
                line = _line.strip()

                if line:
                    regex_pgn__found = False
                    if res_regex_pgn_tags := re.match(ChessGame.regex_pgn_tags, line):
                        regex_pgn__found = True
                        self.chess_event[res_regex_pgn_tags.group('key')] = res_regex_pgn_tags.group('value')

                    if regex_pgn__found is False:
                        str_listofmoves.append(line)

        str_listofmoves = " ".join(str_listofmoves)

        self.read_pgn__listofmoves(str_listofmoves)

    def read_pgn__doublemove(self,
                             str_doublemove):
        """str_doublemove: e4 e5"""
        move1, move2 = str_doublemove.split(" ")
        self.read_pgn__simplemove(move1)
        self.read_pgn__simplemove(move2)

    def read_pgn__listofmoves(self,
                              src):
        """src: str_listofmoves"""
        doublemove_number = 0
        for _str_doublemove in re.split(ChessGame.regex_pgn_listofmoves['doublemovenumber'], src):
            str_doublemove = _str_doublemove.strip()
            if str_doublemove:
                doublemove_number += 1
                self.read_pgn__doublemove(str_doublemove)

    def read_pgn__simplemove(self,
                             str_simplemove):
        """simplemove: e6e4 // e6-e4 // e4"""
        print("===", str_simplemove)
        who_plays = self.listofmoves.who_plays()

        movetype = MOVETYPE_SINGLE  # default value, may be changed.
        piece1_coord_before = None  # if movetype is MOVETYPE_SINGLE, will be automatically computed with the help of .which_piece_could_go_to()
        piece1_coord_after = None
        piece2_coord_before = None
        piece2_coord_after = None

        if str_simplemove == "O-O":
            movetype = MOVETYPE_CASTLING_OO
            # king
            piece1_coord_before = self.gameboard.get_king_coord(color=who_plays)
            piece1_coord_after = piece1_coord_before[0]+2, piece1_coord_before[1]
            # rook:
            piece2_coord_before = piece1_coord_before[0]+3, piece1_coord_before[1]
            piece2_coord_after = piece1_coord_before[0]+1, piece1_coord_before[1]
        elif str_simplemove == "O-O-O":
            movetype = MOVETYPE_CASTLING_OOO
            # king
            piece1_coord_before = self.gameboard.get_king_coord(color=who_plays)
            piece1_coord_after = piece1_coord_before[0]-2, piece1_coord_before[1]
            # rook:
            piece2_coord_before = piece1_coord_before[0]-4, piece1_coord_before[1]
            piece2_coord_after = piece1_coord_before[0]-1, piece1_coord_before[1]
        else:
            res_algebricnotation = {"str_piecenature": None,
                                    "str_coord_x0": None,
                                    "str_intersymb": None,
                                    "str_coord_x1": None,
                                    "str_promotion": None,
                                    }

            if _res := re.match(ChessGame.regex_simplemove_algebraicnotation,
                               str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
            elif _res := re.match(ChessGame.regex_simplemove_algebraicnotation2,
                                  str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_coord_x0"] = _res.group("str_coord_x0")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
            else:
                raise NotImplementedError

            if res_algebricnotation["str_piecenature"] is not None:
                # str_piecenature: 'Q' / 'K' / 'R' / 'B' / 'N'
                piece1_piecenature = ALGEBRICNOTATION2PIECENATURE[res_algebricnotation["str_piecenature"]]
            else:
                # no piecenature: it's a pawn
                piece1_piecenature = PIECENATURE_PAWN

            if res_algebricnotation["str_coord_x0"] is None:  # coord_x0 wasn't given (e.g. 'Rxb4')
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]
                if res_algebricnotation["str_intersymb"] == "x":
                    raise NotImplementedError

            else:  # coord_x0 was given, at least partially (e.g. 'cxb5', 'Rbxb4')
                piece1_coord_before = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x0"]]  # maybe partial (e.g. 'Rbb4')
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]

                if piece1_coord_before[1] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the column, as in 'Qab2'
                    for _x, _y in  self.gameboard.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _x == piece1_coord_before[0]:
                            piece1_coord_before = list(piece1_coord_before)  # a tuple would not be writable
                            piece1_coord_before[1] = _y  # we found the row
                            break  # let's pray there was no other solutions !

                elif piece1_coord_before[0] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the row, as in 'Q2b2'
                    for _x, _y in  self.gameboard.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _y == piece1_coord_before[1]:
                            piece1_coord_before = list(piece1_coord_before)  # a tuple would not be writable
                            piece1_coord_before[0] = _x  # we found the column
                            break  # let's pray there was no other solutions !

                if res_algebricnotation["str_intersymb"] == "x":
                    raise NotImplementedError

        # ---- piece1_coord_before has not yet been initialized ---------------
        if movetype == MOVETYPE_SINGLE:
            piece1_coord_before = self.gameboard.which_piece_could_go_to(
                piece=ChessPiece(nature=piece1_piecenature,
                                 color=self.listofmoves.next_player),
                coord_after=piece1_coord_after,
                movetype=movetype)[0]  # [0] since there is only ONE POSSIBILITY: here, no ambiguous algebric string like 'Q2b2'

        # ---- new_move, .listofmoves and .gameboard updates ------------------
        new_move = ChessMove(movetype=movetype,
                             beforeafter_coord_piece1=(piece1_coord_before, piece1_coord_after),
                             beforeafter_coord_piece2=(piece2_coord_before, piece2_coord_after))
        print(movetype)
        self.listofmoves.add_move(new_move)
        self.gameboard.update_by_playing_a_move(new_move)
        print(new_move)
        print(self.listofmoves)
        print(self.gameboard.get_unicode())


game = ChessGame()
game.read_pgn("game1.pgn")
