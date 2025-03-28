"""Contains a class that is used to display a board.

Currently it only prints in the console.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

from checkers.player import Player
import checkers.constants as constant


class Display:
    """Class used to show a board and other stats in the screen.

    Attributes
    ----------
    board : Board
        Board used to gather the information and that will
        be shown on the screen.

    """

    def __init__(self, board=None):
        """Initiates the display with a board to show.

        Parameters
        -----------
        board : Board
            Board that will be assigned as the board to display
            on the screen.

        """
        self.board = board

    def assign_board(self, board):
        """Assigns a board to the display.

        Parameters
        ----------
        board : Board
            Board that will be assigned as the board to display
            on the screen.

        """
        self.board = board

    def print_board(self):
        """Prints the grid of the board onscreen.

        The dots represent blank spaces.
        w represents a white piece.
        b represents a black piece.
        W represents a white king.
        B represents a black king.

        """
        print()
        print("     ------------------------")
        for row in range(constant.BOARD_DIMENSION):
            line = [' ' + str(constant.BOARD_DIMENSION - row) + ' | ']
            for col in range(constant.BOARD_DIMENSION):
                piece = self.board.get_piece((row, col))
                if piece is None:
                    line.append(' . ')
                elif piece.get_player() is Player.white and piece.is_king():
                    line.append(' W ')
                elif piece.get_player() is Player.black and piece.is_king():
                    line.append(' B ')
                elif piece.get_player() is Player.white:
                    line.append(' w ')
                else:
                    line.append(' b ')
            line.append(" | ")
            print('%s' % (''.join(line)))
        print("     ------------------------")
        print("      a  b  c  d  e  f  g  h ")
        print()

    def print_pieces_left(self):
        """Displays the number of pieces left on each side."""
        print("Black: " + str(self.board.get_num_black_pieces()))
        print("White: " + str(self.board.get_num_white_pieces()))
