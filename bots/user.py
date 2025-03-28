"""Contains a user class used to play against the bot.

#NOTE#
    This class is not very developed and was only used to
    test some functionality (and try to beat the bot, obviously!).
    So it only represents the possible moves with coordinates,
    and those can be selected by picking a number.
    The coordinates follow the board top to bottom, starting
    at 0, 0 and ending at 7,7.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

import checkers.constants as constant


def translate_move(move):
    row = str(constant.BOARD_DIMENSION - move[0])
    col = constant.COLUMNS_TO_LETTERS[move[1] + 1]
    return col + row

class User:
    """User class that allows an external agent to pick moves.

    Attributes
    -----------
    player : Player
        The player, or colour, that this player will represent.

    """

    def __init__(self, player):
        """Initiates the User player.

        Parameters
        ----------
        player : Player
            The colour, or player, that this User will play as.

        """
        self.player = player

    def select_move(self, board):
        """Displays the possible moves and allows the user to select one.

        It gets all the valid moves from the board, then prints it into
        the screen with some numbers. The user can pick one of those on
        the command line and that move would be performed.

        Parameters
        -----------
        board : Board
            Board state that will give the position and possible moves.

        Returns
        --------
        [(int, int), (int, int), Pieces[]]
            Move selected by the user.

        """
        # Gets the legal moves.
        candidates = board.get_all_valid_moves(self.player)

        # Loops through the legal moves.
        for i in range(len(candidates)):
            print(str(i) + ' : ' + translate_move(candidates[i][0]) + " to " + translate_move(candidates[i][1]))

        # Checks for the user selected move.
        correct_input = False
        while not correct_input:
            choice = input("Pick move: ")
            if len(candidates) > int(choice) >= 0:
                # Small test to avoid the program to crash on simple mistakes.
                correct_input = True

        return candidates[int(choice)]

