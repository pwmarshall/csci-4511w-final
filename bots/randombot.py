"""Contains a Bot that plays checkers performing random moves.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""
import random


class RandomBot:
    """Bot that selects random moves.

    Attributes
    ----------
    player : Player
        Player that this bot is. It could be white or black.

    """

    def __init__(self, player):
        """Initiates the bot.

        Parameters
        ----------
        player : Player
            Player that this bot is. It could be white or black.

        """
        self.player = player

    def select_move(self, board):
        """Selects a random move given a board state.

        Parameters
        ----------
        board : Board
            Current board state, with a position and a list of possible moves.

        Returns
        --------
        [(int, int), (int, int), Pieces[]]
            Move selected randomly.

        """
        candidates = board.get_all_valid_moves(self.player)
        return random.choice(candidates)
