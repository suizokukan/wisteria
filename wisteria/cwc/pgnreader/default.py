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
- x, y > xy
- NotImplementedError
- (pas fait) long alg. notation
- (pas fait) status: white_king already moved

https://fr.chesstempo.com/pgn-viewer/
https://theweekinchess.com/a-year-of-pgn-game-files
"""
import copy
import re


COLOR_NOCOLOR = 0
COLOR_WHITE = 1
COLOR_BLACK = 2
def invert_color(color):
    if color == COLOR_WHITE:
        return COLOR_BLACK
    return COLOR_WHITE

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
MOVETYPE_CAPTURE = 1
MOVETYPE_CASTLING = 2


class ChessError(Exception):
    pass


class ChessResult:
    def __init__(self,
                 chessresult=CHESSRESULT_UNDEFINED):
        self.result = chessresult

    def __repr__(self):
        return f"chessresult: {self.result=}"


class ChessPlayer:
    def __init__(self,
                 name="unknown"):
        self.name = name

    def __repr__(self):
        return f"player: {self.name=}"


class ChessGameTags(dict):
    def __init__(self,
                 datadict=None):
        dict.__init__(self)
        if datadict:
            for key, value in datadict:
                self[key] = value

    def __repr__(self):
        return "; ".join(f"{key}: {value}" for key, value in self.items())


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
        return f"ChessPiece: {self.color=}; {self.nature=}"

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
                 enpassant=False,
                 validmove=True):
        self.movetype = movetype
        self.beforeafter_coord_piece1 = beforeafter_coord_piece1
        self.beforeafter_coord_piece2 = beforeafter_coord_piece2
        self.beforeafter_advpiece = beforeafter_advpiece
        self.promotion = promotion
        self.enpassant = enpassant
        self.validmove = validmove

    def __repr__(self):
        return f"{self.movetype=}; " \
            f"{self.beforeafter_coord_piece1=}; {self.beforeafter_coord_piece2}; " \
            f"{self.beforeafter_advpiece=}; {self.promotion=}; {self.enpassant=}; " \
            f"{self.validmove=};"


class ChessListOfMoves(list):
    def __init__(self,
                 next_player=COLOR_WHITE,
                 doublemove_number=1):
        list.__init__(self)
        self.next_player = next_player
        self.doublemove_number = doublemove_number

    def __repr__(self):
        return f"list of moves: {self.nextplayer=}; {self.doublemove_number=}; " + \
            "; ".join(repr(move) for move in self)

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


class ChessGameStatus:
    def __init__(self,
                 pieces = {COLOR_BLACK: {PIECENATURE_KING: {"has already moved": False,},},
                           COLOR_WHITE: {PIECENATURE_KING: {"has already moved": False,},},
                           },
                 game_is_over = False,
                 who_won = None):

        self.pieces = pieces
        self.game_is_over = game_is_over  # (bool)
        self.who_won = who_won  # COLOR_NOCOLOR / COLOR_BLACK / COLOR_WHITE

    def __repr__(self):
        return f"{self.pieces=}; {self.game_is_over=}; {self.who_won=}"

    def copy(self):
        return ChessGameStatus(pieces=copy.deepcopy(self.pieces),
                               game_is_over=self.game_is_over,
                               who_won=self.who_won)

    def update_from_pgn_string(self,
                               status_string,
                               current_player):
        if status_string == "1/2-1/2":
            self.game_is_over = True
            self.who_won = COLOR_NOCOLOR
        elif status_string == "0-1":
            self.game_is_over = True
            self.who_won = COLOR_BLACK
        elif status_string == "1-0":
            self.game_is_over = True
            self.who_won = COLOR_WHITE
        elif status_string == "*":
            self.game_is_over = False
            self.who_won = None
        elif status_string == "++":
            self.game_is_over = True
            self.who_won = current_player
        else:
            raise ChessError(f"Unknown status string '{status_string}'.")

class ChessBoard:

    # moves description for all pieces but knight and pawn
    # moves[nature] = (deltamax, ((deltax, deltay), ...))
    moves_descr = {PIECENATURE_BISHOP: (8,
                                        ((+1, -1), (+1, +1), (-1, +1), (-1, -1)),),
                   PIECENATURE_ROOK: (8,
                                      ((0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   PIECENATURE_QUEEN: (8,
                                       ((+1, -1), (+1, +1), (-1, +1), (-1, -1),
                                        (0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   PIECENATURE_KING: (2,
                                      ((+1, -1), (+1, +1), (-1, +1), (-1, -1),
                                       (0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   }

    def __init__(self):
        self.board = {}  # cf .get_xy(), set_xy()
        self.pieces_status = ChessGameStatus()

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

    def __repr__(self):
        return self.get_unicode() + repr(self.pieces_status)

    def copy(self):
        res = ChessBoard()
        res.board = copy.deepcopy(self.board)
        res.pieces_status = self.pieces_status.copy()
        return res

    def get_king_coord(self,
                       color):
        """Return the (x, y) of the <color>(white/black) king"""
        for x in range(0, 8):
            for y in range(0, 8):
                obj = self.get_xy(x, y)
                if obj.nature == PIECENATURE_KING and \
                   obj.color == color:
                    return (x, y)
        raise ChessError(f"No king (color: {color}): {self.get_unicode()}")

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

    def is_kingpinned(self,
                      x0,
                      y0,
                      xy1):
        """return True if board[x0, y0] moving to bord[x1, y1] is impossible since board[x0, y0] is a pinned piece."""
        """pinned: au sens fort du terme, c'est le roi qui est attaqué"""
        x1, y1 = xy1

        # <piece> is the piece that may be pinned:
        piece = self.get_xy(x0, y0)
        # <king> is the king of <piece>:
        king = self.get_king_coord(piece.color)
        len0 = len(self.who_attacks(king[0], king[1]))

        # <board> is an alternative board with <piece> being moved to (x1, y1):
        _board = self.copy()
        _board.set_xy_empty(x0, y0)
        _board.set_xy(x1, y1, piece)
        king = _board.get_king_coord(piece.color)  # the king may have just moved !
        len1 = len(_board.who_attacks(king[0], king[1]))

        return len0 < len1

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
        if move.movetype in (MOVETYPE_SINGLE, MOVETYPE_CAPTURE):
            before, after = move.beforeafter_coord_piece1
            piece = self.get_xy(before[0], before[1])
            self.set_xy_empty(before[0], before[1])
            if not move.promotion:
                self.set_xy(after[0], after[1], piece)
            else:
                self.set_xy(after[0], after[1], ChessPiece(nature=move.promotion,
                                                           color=piece.color))

            if move.enpassant:
                if piece.color == COLOR_WHITE:
                    self.set_xy_empty(after[0], after[1]+1)
                else:
                    self.set_xy_empty(after[0], after[1]-1)

        elif move.movetype == MOVETYPE_CASTLING:
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
        x, y = coord_after
        res = []

        def add_to_res_if_rightpiece_notpinned(x, y, coord_after, piece):
            if 0 <= x <= 7 and \
               0 <= y <= 7 and \
               self.get_xy(x, y) == piece and \
               not self.is_kingpinned(x, y, coord_after):
                res.append((x, y))

        if piece.nature == PIECENATURE_PAWN:
            if movetype == MOVETYPE_SINGLE:
                if piece.color == COLOR_WHITE:
                    if y==4 and self.get_xy(x, y+1).is_empty():
                        add_to_res_if_rightpiece_notpinned(x, y+2, coord_after, piece)
                    else:
                        add_to_res_if_rightpiece_notpinned(x, y+1, coord_after, piece)
                else:  # piece.color == COLOR_BLACK
                    if y==3 and self.get_xy(x, y-1).is_empty():
                        add_to_res_if_rightpiece_notpinned(x, y-2, coord_after, piece)
                    else:
                        add_to_res_if_rightpiece_notpinned(x, y-1, coord_after, piece)
            elif movetype == MOVETYPE_CAPTURE:
                if piece.color == COLOR_WHITE:
                    add_to_res_if_rightpiece_notpinned(x+1, y+1, coord_after, piece)
                    add_to_res_if_rightpiece_notpinned(x-1, y+1, coord_after, piece)
                else:
                    add_to_res_if_rightpiece_notpinned(x+1, y-1, coord_after, piece)
                    add_to_res_if_rightpiece_notpinned(x-1, y-1, coord_after, piece)

        elif piece.nature == PIECENATURE_KNIGHT:
            add_to_res_if_rightpiece_notpinned(x-2, y-1, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x-2, y+1, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x+2, y-1, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x+2, y+1, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x-1, y-2, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x-1, y+2, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x+1, y-2, coord_after, piece)
            add_to_res_if_rightpiece_notpinned(x+1, y+2, coord_after, piece)
        elif piece.nature in (PIECENATURE_BISHOP,
                              PIECENATURE_ROOK,
                              PIECENATURE_QUEEN,
                              PIECENATURE_KING):
            deltamax = ChessBoard.moves_descr[piece.nature][0]
            for deltax, deltay in ChessBoard.moves_descr[piece.nature][1]:
                for delta in range(1, deltamax):
                    # ~~
                    if ChessBoard.xy_is_off_the_board(x+(deltax*delta), y+(deltay*delta)):
                        # we have to try another (deltax, deltay)
                        break
                    elif self.is_empty_or_is_this_piece(x+(deltax*delta), y+(deltay*delta), piece):
                        add_to_res_if_rightpiece_notpinned(x+(deltax*delta),
                                                           y+(deltay*delta),
                                                           coord_after,
                                                           piece)
                        if self.get_xy(x+(deltax*delta), y+(deltay*delta)) == piece:
                            break
                    else:
                        break
        else:
            raise NotImplementedError

        return res

    def who_attacks(self,
                    x,
                    y):
        def add_to_res_if_rightpiece(x, y, piece):
            if 0 <= x <= 7 and \
               0 <= y <= 7 and \
               self.get_xy(x, y)==piece:
                res.append((x, y))

        target = self.get_xy(x, y)
        _color = invert_color(target.color)
        res = []

        # ---- do a pawn attack (x, y) ? --------------------------------------
        piece = ChessPiece(color=_color,
                           nature=PIECENATURE_PAWN)
        if target.color == COLOR_WHITE:
            add_to_res_if_rightpiece(x+1, y-1, piece)
            add_to_res_if_rightpiece(x-1, y-1, piece)
        else:
            add_to_res_if_rightpiece(x+1, y+1, piece)
            add_to_res_if_rightpiece(x-1, y+1, piece)

        # ---- do a knight attack (x, y) ? ------------------------------------
        piece = ChessPiece(color=_color,
                           nature=PIECENATURE_KNIGHT)
        add_to_res_if_rightpiece(x-2, y-1, piece)
        add_to_res_if_rightpiece(x-2, y+1, piece)
        add_to_res_if_rightpiece(x+2, y-1, piece)
        add_to_res_if_rightpiece(x+2, y+1, piece)
        add_to_res_if_rightpiece(x-1, y-2, piece)
        add_to_res_if_rightpiece(x-1, y+2, piece)
        add_to_res_if_rightpiece(x+1, y-2, piece)
        add_to_res_if_rightpiece(x+1, y+2, piece)

        # ---- do a bishop/rook/queen/king attack (x, y) ? --------------------
        for nature in (PIECENATURE_BISHOP,
                       PIECENATURE_ROOK,
                       PIECENATURE_QUEEN,
                       PIECENATURE_KING):
            piece = ChessPiece(color=_color,
                               nature=nature)
            deltamax = ChessBoard.moves_descr[nature][0]
            for deltax, deltay in ChessBoard.moves_descr[nature][1]:
                for delta in range(1, deltamax):
                    # ~~
                    if ChessBoard.xy_is_off_the_board(x+(deltax*delta), y+(deltay*delta)):
                        # we have to try another (deltax, deltay)
                        break
                    elif self.is_empty_or_is_this_piece(x+(deltax*delta), y+(deltay*delta), piece):
                        add_to_res_if_rightpiece(x+(deltax*delta),
                                                 y+(deltay*delta),
                                                 piece)
                        if self.get_xy(x+(deltax*delta), y+(deltay*delta))==piece:
                            break
                    else:
                        break

        return res

    @staticmethod
    def xy_is_off_the_board(x,
                            y):
        return not ((0 <= x <= 7) and (0 <= y <= 7))


class ChessGame:
    # e.g. [Event "F/S Return Match"]
    regex_pgn_tags = re.compile('^\s*\[(?P<key>.+)\s+\"(?P<value>.+)\"\]$')

    regex_pgn_listofmoves = {
        'doublemovenumber': re.compile('[\d]+\.\s'),
        'game_result': re.compile('(?P<pre>.+)(?P<game_result>1\/2-1\/2|1\-0|0\-1|#|\*|\+\+)'),
        'en passant': re.compile('\s*e\.p\.'),
    }
    regex_simplemove_algebraicnotation = re.compile(
        "^"
        "(?P<str_piecenature>[KQNRB])?"
        "(?P<str_intersymb>[x|\-])?"
        "(?P<str_coord_x1>[a-h]|[1-8]|[a-h][1-8])"
        "(=(?P<str_promotion>[KQNRB]))?"
        "(?P<str_chess>\+)?"
        "(?P<str_enpassant>e\.p\.)?"
        "$")
    regex_simplemove_algebraicnotation2 = re.compile(
        "^"
        "(?P<str_piecenature>[KQNRB])?"
        "(?P<str_coord_x0>[a-h][1-8]|[a-h]|[1-8])?"
        "(?P<str_intersymb>[x|\-])?"
        "(?P<str_coord_x1>[a-h][1-8]|[a-h]|[1-8])"
        "(=(?P<str_promotion>[KQNRB]))?"
        "(?P<str_chess>\+)?"
        "(?P<str_enpassant>e\.p\.)?"
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

        '1': (None, 7), '2': (None, 6), '3': (None, 5), '4': (None, 4),
        '5': (None, 3), '6': (None, 2), '7': (None, 1), '8': (None, 0),
        }
    coord2strcoord = {value: key for key, value in strcoord2coord.items()}

    def __init__(self):
        self.white_player = ChessPlayer()
        self.black_player = ChessPlayer()
        self.chessgame_tags = ChessGameTags()
        self.board = ChessBoard()
        self.result = ChessResult()
        self.listofmoves = ChessListOfMoves()
        self.status = ChessGameStatus()

        self.errors = []

    def __repr__(self):
        res = f"{self.white_player=}; {self.black_player=}; {self.chessgame_tags=}; " \
            "{self.board=}; {self.result=}; {self.listofmoves=}; {self.status=}"

        if self.errors:
            res += "errors: "+str(self.errors)

    def read_pgn(self,
                 lines):
        success = True

        self.listofmoves = ChessListOfMoves()
        try:
            str_listofmoves = []
            for _line in lines:
                line = _line.strip()

                if line:
                    regex_pgn__found = False
                    if res_regex_pgn_tags := re.search(ChessGame.regex_pgn_tags, line):
                        regex_pgn__found = True
                        self.chessgame_tags[res_regex_pgn_tags.group('key')] = res_regex_pgn_tags.group('value')

                    if regex_pgn__found is False:
                        str_listofmoves.append(line)

            str_listofmoves = " ".join(str_listofmoves)

            self.read_pgn__listofmoves(str_listofmoves)

        except (ChessError, TypeError) as error:
            self.errors.append(error)
            success = False

        return success

    def read_pgn__doublemove(self,
                             str_doublemove):
        """str_doublemove: e4 e5"""
        # " e.p." with space(s) must be rewritten "e.p." (without space)
        if re.search(ChessGame.regex_pgn_listofmoves['en passant'], str_doublemove):
            str_doublemove = re.sub(ChessGame.regex_pgn_listofmoves['en passant'],
                                    "e.p.",
                                    str_doublemove)
        # if <str_doublemove> is something like:
        #   "Kd5 Kxb3 0-1"
        # we have to attach the last part using the '_' character:
        #   "Kd5 Kxb3_0-1"
        if res__game_result := re.search(ChessGame.regex_pgn_listofmoves['game_result'],
                                        str_doublemove):
            self.status.update_from_pgn_string(status_string=res__game_result.group('game_result'),
                                               current_player=self.listofmoves.next_player)
            str_doublemove = re.sub(
                ChessGame.regex_pgn_listofmoves['game_result'],
                lambda match: match.group('pre').strip()+'_'+match.group('game_result').strip(),
                str_doublemove)

        if " " not in str_doublemove:
            # only one move in <str_doublemove> (as in 'Nc4')
            self.read_pgn__simplemove(str_doublemove)
        else:
            # normal case, two moves in <str_doublemove> (as in 'e4 e5')
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
        if res__game_result := re.search(ChessGame.regex_pgn_listofmoves['game_result'], str_simplemove):
            # let's remove the '_' character added by read_pgn__doublemove() before the game result:
            str_simplemove = str_simplemove.replace('_', '')
            # we can now remove the game result suffix (e.g. '1-0')
            self.status.update_from_pgn_string(status_string=res__game_result.group('game_result'),
                                               current_player=self.listofmoves.next_player)
            str_simplemove = re.sub(
                ChessGame.regex_pgn_listofmoves['game_result'],
                lambda match: match.group('pre').strip(),
                str_simplemove)

        str_simplemove = str_simplemove.strip()

        if not str_simplemove:
            return

        # ---------------------------------------------------------------------
        # ---- normal case: str_simplemove describes a move -------------------
        # ---------------------------------------------------------------------

        # default values:
        who_plays = self.listofmoves.who_plays()
        movetype = MOVETYPE_SINGLE  # default value, may be changed.
        piece1_coord_before = None  # if movetype is MOVETYPE_SINGLE, will be automatically computed with the help of .which_piece_could_go_to()
        piece1_coord_after = None
        piece2_coord_before = None
        piece2_coord_after = None
        promotion = None  # if promotion, <promotion> will be the PIECENATURE_xxx constant
        enpassant=False

        if str_simplemove == "O-O":
            movetype = MOVETYPE_CASTLING
            # king
            piece1_coord_before = self.board.get_king_coord(color=who_plays)
            piece1_coord_after = piece1_coord_before[0]+2, piece1_coord_before[1]
            # rook:
            piece2_coord_before = piece1_coord_before[0]+3, piece1_coord_before[1]
            piece2_coord_after = piece1_coord_before[0]+1, piece1_coord_before[1]
        elif str_simplemove == "O-O-O":
            movetype = MOVETYPE_CASTLING
            # king
            piece1_coord_before = self.board.get_king_coord(color=who_plays)
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
                                    "str_chess": None,
                                    "str_enpassant": None,
                                    }

            if _res := re.search(ChessGame.regex_simplemove_algebraicnotation,
                                 str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
                res_algebricnotation["str_chess"] = _res.group("str_chess")
                res_algebricnotation["str_enpassant"] = _res.group("str_enpassant")
            elif _res := re.search(ChessGame.regex_simplemove_algebraicnotation2,
                                   str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_coord_x0"] = _res.group("str_coord_x0")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
                res_algebricnotation["str_chess"] = _res.group("str_chess")
                res_algebricnotation["str_enpassant"] = _res.group("str_enpassant")
            else:
                raise ChessError(
                    f"Ill-formed or unknown string format for str_simplemove='{str_simplemove}'.")

            if res_algebricnotation["str_intersymb"] == "x":
                movetype = MOVETYPE_CAPTURE

            if res_algebricnotation["str_piecenature"] is not None:
                # str_piecenature: 'Q' / 'K' / 'R' / 'B' / 'N'
                piece1_piecenature = ALGEBRICNOTATION2PIECENATURE[res_algebricnotation["str_piecenature"]]
            else:
                # no piecenature: it's a pawn
                piece1_piecenature = PIECENATURE_PAWN

            if res_algebricnotation["str_coord_x0"] is None:  # coord_x0 wasn't given (e.g. 'Rxb4')
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]
            else:  # coord_x0 was given, at least partially (e.g. 'cxb5', 'Rbxb4')
                piece1_coord_before = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x0"]]  # maybe partial (e.g. 'Rbb4')
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]

                if piece1_coord_before[1] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the column, as in 'Qab2', 'cxb5'
                    for _x, _y in  self.board.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _x == piece1_coord_before[0]:
                            piece1_coord_before = list(piece1_coord_before)  # a tuple would not be writable
                            piece1_coord_before[1] = _y  # we found the row
                            #
                            # To optimize, you may want to consider the first solution is the right
                            # one and therefore add 'break'; without this 'break' statement you may
                            # find errors in the list of moves.
                            #
                            # break

                elif piece1_coord_before[0] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the row, as in 'Q2b2'
                    for _x, _y in  self.board.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _y == piece1_coord_before[1]:
                            piece1_coord_before = list(piece1_coord_before)  # a tuple would not be writable
                            piece1_coord_before[0] = _x  # we found the column
                            #
                            # To optimize, you may want to consider the first solution is the right
                            # one and therefore add 'break'; without this 'break' statement you may
                            # find errors in the list of moves.
                            #
                            # break

            if res_algebricnotation["str_promotion"]:
                promotion = ALGEBRICNOTATION2PIECENATURE[res_algebricnotation["str_promotion"]]

        # ---- piece1_coord_before has not yet been initialized ---------------
        if piece1_coord_before is None:
            _possibilities = self.board.which_piece_could_go_to(
                piece=ChessPiece(nature=piece1_piecenature,
                                 color=self.listofmoves.next_player),
                coord_after=piece1_coord_after,
                movetype=movetype)
            if not _possibilities:
                raise ChessError(
                    f"Can't interpret (simple) move '{str_simplemove}' for the current board. "
                    f"No legal move matches this string. "
                    f"self={repr(self)}")
            if len(_possibilities) > 1:
                raise ChessError(
                    f"Anomaly: too many possibilities, the move '{str_simplemove}' is ambiguous. "
                    f"Current situation is: {repr(self)}")
            # [0] since there is only ONE POSSIBILITY here: len(_possibilities) is 1.
            piece1_coord_before = _possibilities[0]

        # ---- en passant ? ---------------------------------------------------
        enpassant = movetype == MOVETYPE_CAPTURE and \
            self.board.get_xy(piece1_coord_after[0], piece1_coord_after[1]).is_empty()

        # ---- new_move, update of .listofmoves and .board ----------------
        new_move = ChessMove(movetype=movetype,
                             beforeafter_coord_piece1=(piece1_coord_before, piece1_coord_after),
                             beforeafter_coord_piece2=(piece2_coord_before, piece2_coord_after),
                             promotion=promotion,
                             enpassant=enpassant)
        self.listofmoves.add_move(new_move)
        self.board.update_by_playing_a_move(new_move)


class ChessGames(list):
    def read_pgn(self,
                 pgnfilename):
        success = True

        inside_header = False
        buff = []

        with open(pgnfilename) as src:

            for _line in src:
                line = _line.strip()

                if line:
                    if inside_header:
                        if re.search(ChessGame.regex_pgn_tags, line) and not line.startswith("1. "):
                            # we're still in the header.
                            pass
                        else:
                            # we're not in the header anymore.
                            inside_header = False
                    else:
                        if re.search(ChessGame.regex_pgn_tags, line) and not line.startswith("1. "):
                            # we weren't in the header but <line> is a header line.
                            if buff:
                                game = ChessGame()
                                success = success and game.read_pgn(buff)
                                self.append(game)
                            buff = []
                            inside_header = True
                        else:
                            # we're still reading data lines that are not in a header.
                            if line.startswith("1. "):
                                if buff:
                                    game = ChessGame()
                                    success = success and game.read_pgn(buff)
                                    self.append(game)
                                buff = []

                    buff.append(line)

        if buff:
            game = ChessGame()
            success = success and game.read_pgn(buff)
            self.append(game)

        return success
