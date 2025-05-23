"""Contains a class that represents a checkers board.

It works as a game state representation for the checkers game.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

import copy
import random
import checkers.constants as constant
from checkers.player import Player
from checkers.piece import Piece
from checkers.display import Display

from checkers.types import *

class Board:
    """Represents a checkers board, with its pieces and moves.

    It is also used a game state for AI purposes. When a new board is created
    this is set to an initial position.

    Attributes
    -----------
    num_white_pieces : int
        Number of white pieces in play.
    num_white_kings : int
        Number of white kings in play. A king is also counted on the pieces count.
    num_black_pieces : int
        Number of black pieces in play.
    num_black_kings : int
        Number of black kings in play. A king is also counted on the pieces count.
    board : Piece[][]
        Matrix that represents a board with pieces. None represents an empty space.
    moves : [(int, int), (int, int), Piece[]]
        Vector that holds all the past moves performed on the board.
    """

    def __init__(self, board = None):
        """Creates a new board and sets it to a starting position."""
        # The starting counts are set to 0 and modified when the board is initiated.
        self.num_black_pieces = 0
        self.num_black_kings = 0
        self.num_white_pieces = 0
        self.num_white_kings = 0
        # Creates a new board and fills it with the appropriate pieces.
        if board:
            self.board = board
            self.num_black_pieces = len(self.get_all_pieces(Player.black))
            self.num_white_pieces = len(self.get_all_pieces(Player.white))
        else:
            self.board = self._initiate_board()
        self.moves = []

    def evaluate(self, player: Player):
        """Heuristic function that evaluates the current position.

        The evaluation method assign points for the following parameters:
            - The number of pieces in play against the opponent ones.
            - Position of the current pieces, including the distance
                of the king to the other pieces.
            - Random point used to break ties to give different game variants.

        Parameters
        -----------
        player : Player
            Player who evaluates the board. It is needed to know which color to favor in the evaluation.

        Returns
        --------
        int
            Value that represents the advantage of the player in the current board.
            Positive is winning. Negative is losing.

        """
        evaluation = 0

        # Takes into account the number of pieces for each side in play.
        self._evaluate_num_pieces(player)

        # Evaluates the position of each piece
        evaluation += self._evaluate_pieces_position(player)
        evaluation -= self._evaluate_pieces_position(player.other)

        # Random extra point used to randomize plays that are equal
        evaluation += random.randint(0, 1)

        return evaluation

    def has_winner(self):
        """Get the winner of the game, or None if it's not over.

        A game is won by one side if there is no left pieces of the opponent.
        If there has been a repetition of three moves, the game ends in a tie.

        Returns
        --------
        boolean
            Returns None if there is not a winner. Returns the
            winner if there is one. Returns "Tie" if there is
            a tie.
        """

        if self.num_black_pieces == 0 or len(self.get_all_valid_moves(Player.black)) == 0:
            return Player.white
        elif self.num_white_pieces == 0 or len(self.get_all_valid_moves(Player.white)) == 0:
            return Player.black
        elif self.repetition_happened() or self.passive_game():
            return "Tie"
        else:
            return None

    def get_all_valid_moves(self, player: Player) -> list[Move]:
        """Gets all the valid moves that a player can do.

        Moves are shown with the format [
            current position of the piece (row, col)
            next position for the piece (row, col)
            pieces that get eaten [in a list]
        ]

        Parameters
        -----------
        player : Player
            Player who has to move.

        Returns
        --------
        List [position, next_position, pieces_to_delete]
            Returns a move explained by the starting and ending position and
            the pieces that get captured.

        """
        moves: list[Move] = []  # Stores the possible moves
        capture_move_exists = False  # Indicates if a capturing move is possible

        for piece in self.get_all_pieces(player):
            valid_moves = self._get_valid_moves(piece)

            for move, skip in valid_moves.items():
                moves.append([(piece.position[0], piece.position[1]), move, skip])

                if len(skip) > 0:
                    # Checks if there is a move that can capture a piece
                    capture_move_exists = True

        if capture_move_exists:
            # Only gets the capturing moves if there is one
            eating_moves = []
            for move in moves:
                if len(move[2]) != 0:
                    eating_moves.append(move)

            moves = eating_moves

        return moves

    def make_move(self, move: Move):
        """Executes a move in the board.

        Parameters
        -----------
        move : [(int, int), (int, int), Piece[]]
            Move to apply to the board. It holds the current position,
            the next position and the pieces captured.

        """
        # Unpack the information from the move
        piece = self.get_piece(move[0])
        row = move[1][0]
        col = move[1][1]
        eliminated_pieces = move[2]

        # Move the piece and eliminate the captured pieces
        self.board[piece.position[0]][piece.position[1]] = None
        self.board[row][col] = piece
        piece.position = (row, col)
        self.remove(eliminated_pieces)

        # Checks if the piece has been promoted
        if piece.get_player() == Player.black and \
                piece.position[0] == constant.BOARD_DIMENSION - 1 \
                and not piece.is_king():
            piece.make_king()
            self.num_black_kings += 1

        elif piece.get_player() == Player.white and \
                piece.position[0] == 0 \
                and not piece.is_king():
            piece.make_king()
            self.num_white_kings += 1

        # Add the move performed to the history of the game
        self.moves.append(move)

    def last_move(self):
        """Get the last move executed on the board.

        Returns
        --------
        [(int, int), (int, int), Piece[]]
            Last move performed. Returns None if the game hasn't started.
        """
        if len(self.moves) > 0:
            return self.moves[-1]
        else:
            return None

    def get_all_pieces(self, player: Player) -> list[Piece]:
        """Gets all the pieces from a player in the board.

        Parameters
        ----------
        player : Player
            Player that owns the pieces requested.

        Returns
        -------
        Pieces[]
            List with all the pieces existing in the board that
            a player owns.

        """
        pieces: list[Piece] = []
        for row in range(constant.BOARD_DIMENSION):
            for col in range(constant.BOARD_DIMENSION):
                piece = self.get_piece((row, col))
                if piece is not None and piece.get_player() is player:
                    pieces.append(piece)
        return pieces

    def get_piece(self, position: Position):
        """Gets the piece located in a given position.

        Parameters
        ----------
        position : (int, int)
            Position represented by a row and a column.
            The piece located in that position will be returned.

        Returns
        -------
        Piece
            Returns the piece located in that position.
            If the position is empty returns None.
        """
        return self.board[position[0]][position[1]]

    def remove(self, pieces):
        """Removes all the indicated pieces from the board.

        Parameters
        ----------
        pieces : Pieces[]
            Pieces that will get removed from the board.

        """
        for piece in pieces:
            self.board[piece.position[0]][piece.position[1]] = None
            if piece.get_player() is Player.white:
                self.num_white_pieces -= 1
                if piece.is_king():
                    self.num_white_kings -= 1

            elif piece.get_player() is Player.black:
                self.num_black_pieces -= 1
                if piece.is_king():
                    self.num_black_kings -= 1

    def num_pieces_left(self):
        """Gets the total number of pieces left in the game.

        Returns
        -------
        int
            Number of pieces left on the game including both sides.

        """
        return self.num_white_pieces + self.num_black_pieces

    def get_num_white_pieces(self):
        """Gets the total number of white pieces left in the game.

        Returns
        -------
        int
            Number of white pieces left on the game.

        """
        return self.num_white_pieces

    def get_num_black_pieces(self):
        """Gets the total number of black pieces left in the game.

        Returns
        -------
        int
            Number of black pieces left on the game.

        """
        return self.num_black_pieces
    
    def get_num_pieces(self, player: Player):
        """Gets the number of pieces for the player
        
        Parameters
        ----------
        player: Player - the player to get the num pieces for
        
        Returns
        -------
        int
            Number of that player's pieces
        """

        if player == Player.white:
            return self.num_white_pieces
        else:
            return self.num_black_pieces

    def repetition_happened(self):
        """Checks for a three-move repetition.

        Returns
        -------
        boolean
            True if the players have performed the same board state
            three times in a row. False if that is not the case.

        """
        repetition = False
        if len(self.moves) >= 12:
            if self.moves[-1][0] == self.moves[-5][0] == self.moves[-9][0] and \
                    self.moves[-1][1] == self.moves[-5][1] == self.moves[-9][1] and \
                    self.moves[-2][0] == self.moves[-6][0] == self.moves[-10][0] and \
                    self.moves[-2][1] == self.moves[-6][1] == self.moves[-10][1] and \
                    self.moves[-3][0] == self.moves[-7][0] == self.moves[-11][0] and \
                    self.moves[-3][1] == self.moves[-7][1] == self.moves[-11][1] and \
                    self.moves[-4][0] == self.moves[-8][0] == self.moves[-12][0] and \
                    self.moves[-4][1] == self.moves[-8][1] == self.moves[-12][1]:
                repetition = True

        return repetition

    def passive_game(self):
        """Checks if X number of moves have passed without any capture.

        Returns
        -------
        boolean
            True if for the past X moves a piece have not been captured.
            False if otherwise.

        """
        passive_game = False
        if len(self.moves) >= constant.MAX_MOVES_WITHOUT_CAPTURE:
            passive_game = True
            for move in range(constant.MAX_MOVES_WITHOUT_CAPTURE):
                if len(self.moves[-move][2]) != 0:
                    passive_game = False
                    break

        return passive_game

    def _get_valid_moves(self, piece: Piece):
        """Gets all the valid moves for a piece.

        Parameters
        ----------
        piece : Piece
            Piece that wants to retrieve all it's moves.

        Returns
        --------
        Dictionary {(int, int), Pieces[]}
            Where key corresponds to the next position
            and value is a list of the pieces captured in the movement.

        """
        moves = {}
        left = piece.position[1] - 1  # Left position
        right = piece.position[1] + 1  # Right position
        row = piece.position[0]  # Current row

        if piece.get_player() == Player.white or piece.is_king():
            # Checks the movements from the bottom to the top
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.get_player(), left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.get_player(), right))

        if piece.get_player() == Player.black or piece.is_king():
            # Checks the movements from the top to the bottom
            moves.update(self._traverse_left(row + 1, min(row + 3, constant.BOARD_DIMENSION),
                                             1, piece.get_player(), left))
            moves.update(self._traverse_right(row + 1, min(row + 3, constant.BOARD_DIMENSION),
                                              1, piece.get_player(), right))

        return moves

    def _traverse_left(self, start, stop, step, player, left, skipped=[]):
        """Algorithm that traverses the board to the left to find possible movements for a piece.

        Parameters
        ----------
        start : int
            Where to start looking from.
        stop : int
            Where to stop looking for.
        step : int
            Steps to take between positions.
        player : Player
            Current player performing the moves (or analysis)
        left : int
            Left position to look from.
        skipped : List (Empty by default)
            Stores the pieces skipped on the movement.

        Returns
        -------
        Dictionary {(int, int), Pieces[]}
            Where key corresponds to the next position
            and value is a list of the pieces captured in the movement.

        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, constant.BOARD_DIMENSION)
                    moves.update(self._traverse_left(r + step, row, step, player, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, player, left + 1, skipped=last))
                break
            elif current.get_player() == player:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, player, right, skipped=[]):
        """Algorithm that traverses the board to the left to find possible movements for a piece.

                Parameters
                ----------
                start : int
                    Where to start looking from.
                stop : int
                    Where to stop looking for.
                step : int
                    Steps to take between positions.
                player : Player
                    Current player performing the moves (or analysis)
                right : int
                    Right position to look from.
                skipped : List (Empty by default)
                    Stores the pieces skipped on the movement.

                Returns
                -------
                Dictionary {next_position, [pieces_captured]}
                    Where key corresponds to the next position
                    and value is a list of the pieces captured in the movement.

                """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= constant.BOARD_DIMENSION:
                break

            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, constant.BOARD_DIMENSION)
                    moves.update(self._traverse_left(r + step, row, step, player, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, player, right + 1, skipped=last))
                break
            elif current.get_player() == player:
                break
            else:
                last = [current]

            right += 1

        return moves

    def _initiate_board(self) -> list[list[Piece]]:
        """ Initiates a board based on the dimension and the rows of pieces set.

        To change the values of the board, look for a constants file.

        Returns
        --------
        Piece[][]
            Matrix that represents the board. A gris is created
            and populated by pieces. If a position is occupied
            by a piece, it has the piece in it. If it is empty,
            it has None.

        """
        grid = []
        for i in range(constant.BOARD_DIMENSION):
            # Starts each row
            current_row = []
            for j in range(constant.BOARD_DIMENSION):
                # Adds the pieces depending on the position
                if i < constant.ROWS_OF_PIECES:
                    # Black pieces
                    if (j + i) % 2 != 0:
                        current_row.append(Piece((i, j), Player.black))
                        self.num_black_pieces = self.num_black_pieces + 1
                    else:
                        current_row.append(None)

                elif i >= constant.BOARD_DIMENSION - constant.ROWS_OF_PIECES:
                    # White pieces
                    if (j + i) % 2 != 0:
                        current_row.append(Piece((i, j), Player.white))
                        self.num_white_pieces = self.num_white_pieces + 1
                    else:
                        current_row.append(None)

                else:
                    current_row.append(None)

            grid.append(current_row)

        return grid

    def _evaluate_num_pieces(self, player):
        """Gets a score taking into account the number of pieces in play.

        The score will be:
            - 10 points for piece in play.
            - 10 points extra for a king in play.
            - -10 points for an opponent piece in play.
            - -10 points extra for an opponent king in play.

        Parameters
        ----------
        player : Player
            Player that the function evaluates the state for.

        Returns
        -------
        int
            Value that represents the advantage for the given player.

        """
        evaluation = 0
        if player is Player.black:
            evaluation += self.num_black_pieces * 10
            evaluation -= self.num_white_pieces * 10
            evaluation += self.num_black_kings * 10
            evaluation -= self.num_white_kings * 10
        elif player is Player.white:
            evaluation -= self.num_black_pieces * 10
            evaluation += self.num_white_pieces * 10
            evaluation -= self.num_black_kings * 10
            evaluation += self.num_white_kings * 10

        return evaluation

    def _evaluate_pieces_position(self, player):
        """Gets a score taking into account the position of the piece.

        The score will be:
            - Positive points for pieces in strong positions.
            - Positive points for the kings being close to opponent pieces.
            - Negative points for opponent pieces in strong positions.
            - Negative points for the opponent kings being close to the player pieces.

        Parameters
        ----------
        player : Player
            Player that the function evaluates the state for.

        Returns
        -------
        int
            Value that represents the advantage for the given player.

        """
        evaluation = 0

        pieces = self.get_all_pieces(player)
        for piece in pieces:
            if player is Player.white:
                if piece.is_king():
                    evaluation += self._kings_distance(piece)
                else:
                    evaluation += constant.POSITIONAL_EVALUATION[piece.position[0]][piece.position[1]]
            elif player is Player.black:
                if piece.is_king():
                    evaluation += self._kings_distance(piece)
                else:
                    evaluation += constant.POSITIONAL_EVALUATION[constant.BOARD_DIMENSION-1-piece.position[0]]\
                        [constant.BOARD_DIMENSION-1-piece.position[1]]

        return evaluation

    def _kings_distance(self, piece: Piece):
        """Calculates the points given by the distance of a king to other pieces.

        The formula is board_dimension (usually 8) - the distance.
        A close distance would result in more points given.
        This heuristic function is useful so kings don't stay away from
        the other pieces and go into the attack at the end game.

        Parameters
        ----------
        piece : Piece
            King that this method evaluates.

        Returns
        -------
        int
            Value that represents the advantage for the given player.

        """
        min_distance = constant.BOARD_DIMENSION - 1
        opponent_pieces = self.get_all_pieces(piece.get_player().other)
        for opp_piece in opponent_pieces:
            distance = abs(piece.position[0] - opp_piece.position[0]) + abs(piece.position[1] - opp_piece.position[1]) / 2
            if distance < min_distance:
                min_distance = distance

        evaluation = constant.BOARD_DIMENSION - min_distance
        return evaluation

    def __deepcopy__(self, memodict={}):
        """Deep-copies the board object."""
        dp = Board()
        dp.board = copy.deepcopy(self.board)
        dp.moves = copy.deepcopy(self.moves)
        dp.num_white_pieces = copy.deepcopy(self.num_white_pieces)
        dp.num_black_pieces = copy.deepcopy(self.num_black_pieces)
        dp.num_white_kings = copy.deepcopy(self.num_white_kings)
        dp.num_black_kings = copy.deepcopy(self.num_black_kings)
        return dp
    
class Board_State():
    def __init__(self, board, parentMove: Move = None):
        #These values are just initial values that don't matter in the functions
        self.board = board #arr
        # self.options1, self.options2 = CanMove(self.board)
        # self.options = self.options1 + self.options2
        self.parentMove = parentMove

    def find_children(self, board):
        children = set()
        #Update the options
        board_copy = copy.deepcopy(board)
        
        boardObj = Board(board_copy)
        options1 = boardObj.get_all_valid_moves(Player.white)
        for option in options1:
            board_copy = boardObj.__deepcopy__()
            board_copy.make_move(option)
            children.add(Board_State(board_copy.board, option))
        return children

    def find_oppchildren(self,board):
        children = set()
        board_copy = copy.deepcopy(board)
        
        boardObj = Board(board_copy)
        options2 = boardObj.get_all_valid_moves(Player.black)
        for option in options2:
            board_copy = boardObj.__deepcopy__()
            board_copy.make_move(option)
            children.add(Board_State(board_copy.board))
        return children


    def find_random_child(self, board):
        board_copy = copy.deepcopy(board)
        
        boardObj = Board(board_copy)
        options1 = boardObj.get_all_valid_moves(Player.white)
        choice = random.choice(options1)
        boardObj.make_move(choice)

        if not self.is_terminal(boardObj.board):
            options2 = boardObj.get_all_valid_moves(Player.black)
            choice = random.choice(options2)
            boardObj.make_move(choice)

        return Board_State(boardObj.board)

    def is_terminal(self,board):
        board_copy = copy.deepcopy(board)
        boardObj = Board(board_copy)

        if boardObj.has_winner():
            return True
        return False

    def reward(self,board):        
        boardObj = Board(board)
        # Display(False, boardObj).print_board()
        # print(boardObj.get_num_black_pieces())
        # print(boardObj.get_num_white_pieces())
        winner = boardObj.has_winner()
        if winner is Player.white:
            return 1
        elif winner is Player.black:
            return -1
        else:
            print("Tie Instance")
            return 0
        
class BoardHash(Board):
    def __init__(self, board: Board = None):
        super().__init__(board.board if board else None)
        self.parent_move: Move
        pass

    def find_children(self, player: Player):
        children: set[BoardHash] = set()
        #Update the options
        self.options = self.get_all_valid_moves(player)
        for move in self.options:
            child = self.simulate_move(move)
            children.add(child)
        return children

    def find_random_child(self, player: Player):
        
        options = self.get_all_valid_moves(player)
        move = random.choice(options)
        new_board = self.simulate_move(move)

        if not new_board.is_terminal():
            options = new_board.get_all_valid_moves(player.other)
            move = random.choice(options)
            new_board = new_board.simulate_move(move)

        return new_board

    def is_terminal(self):
        if len(self.get_all_valid_moves(Player.white)) == 0 or len(self.get_all_valid_moves(Player.black)) == 0:
            return True
        else:
            return False

    def reward(self, player: Player):
        #1 if won, 0 if lost
        if self.get_num_pieces(player) > 0 and self.get_num_pieces(player.other) == 0:
            return 1
        elif self.get_num_pieces(player) == 0 and self.get_num_pieces(player.other) > 0:
            return 0
        else:
            #Tie instances shouldn't really be a thing
            #Someone is winning
            #print("Tie Instance")
            return .5
        
    def __deepcopy__(self, memodict={}):
        """Deep-copies the board object."""
        dp = BoardHash()
        dp.board = copy.deepcopy(self.board)
        dp.moves = copy.deepcopy(self.moves)
        dp.num_white_pieces = copy.deepcopy(self.num_white_pieces)
        dp.num_black_pieces = copy.deepcopy(self.num_black_pieces)
        dp.num_white_kings = copy.deepcopy(self.num_white_kings)
        dp.num_black_kings = copy.deepcopy(self.num_black_kings)
        return dp
        
    def simulate_move(self, move: Move):
        new_board = self.__deepcopy__()
        new_board.make_move(move)
        new_board.parent_move = move
        return new_board

    def hash(self):
        """
        Replace all white pieces with 1, white kings with 2 and black pieces with -1 and black kings with -2.
        Also makes the 2d board array into a 1d array
        
        Returns
        -------
        Array of state of game

        """

        hashArr: list[int] = []
    
        for x in range(constant.BOARD_DIMENSION):
            for y in range(constant.BOARD_DIMENSION):
                piece = self.get_piece((x, y))
                if piece.get_player() == Player.white and piece.is_king():
                    hashArr.append(2)
                elif piece.get_player() == Player.white and not piece.is_king():
                    hashArr.append(1)
                elif piece.get_player() == Player.black and not piece.is_king():
                    hashArr.append(-1)
                elif piece.get_player() == Player.black and piece.is_king():
                    hashArr.append(-2)

        return hashArr
