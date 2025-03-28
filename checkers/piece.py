"""Contains a class representing a piece for the game of checkers.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""


class Piece:
    """Representation of a game piece in checkers.

    Attributes
    -----------
    row : int
        Row where the piece is located.
    col : int
        Column where the piece is located.
    player : Player
        Player who owns the piece. It defines the color of the piece.
    king : boolean
        Says if the piece has been converted to a king or not.

    """

    def __init__(self, row, col, player):
        """Initiates a piece.

        Parameters
        -----------
        row : int
            Row where the piece is located.
        col : int
            Column where the piece is located.
        player : Player
            Player who owns the piece. It defines the color of the piece.

        """
        self.row = row
        self.col = col
        self.player = player
        self.king = False  # A piece is not a king by default

    def make_king(self):
        """Turns the piece into a king."""
        self.king = True

    def move(self, row, col):
        """Moves the piece to a new position.

        Parameters
        -----------
        row : int
            Row of the new position.
        col : int
            Column of the new position.

        """
        self.row = row
        self.col = col

    def get_player(self):
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
