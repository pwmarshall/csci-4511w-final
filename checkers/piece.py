"""Contains a class representing a piece for the game of checkers.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

from checkers.player import Player
from checkers.types import *

class Piece:
    """Representation of a game piece in checkers.

    Attributes
    -----------
    position : (row, col)
        Where the piece is located.
    player : Player
        Player who owns the piece. It defines the color of the piece.
    king : boolean
        Says if the piece has been converted to a king or not.

    """

    def __init__(self, position: Position, player: Player):
        """Initiates a piece.

        Parameters
        -----------
        position : (row, col)
            Where the piece is located.
        player : Player
            Player who owns the piece. It defines the color of the piece.

        """
        self.position = position
        self.player = player
        self.king = False  # A piece is not a king by default

    def make_king(self):
        """Turns the piece into a king."""
        self.king = True

    def move(self, position: Position):
        """Moves the piece to a new position.

        Parameters
        -----------
        position: Position
            the new position
        """
        self.position = position


    def get_player(self) -> Player:
        """Gets the player, also known as the colour, that owns the piece.

        Returns
        -------
        Player
            The player who owns the piece.
        """
        return self.player

    def is_king(self):
        """Gets if a piece is king.

        Returns
        --------
        boolean
            True if the piece is a king, False otherwise.
        """
        return self.king
