"""Contains an enumeration that represents a player (white or black) for the game of checkers.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

import enum


class Player(enum.Enum):
    """Representation of a checkers player.

    The enumeration has two different values, white or black, that represents
    the side of the player in the checkers game.
    """
    white = 1
    black = 2

    @property
    def other(self):
        """Returns the opposite player"""
        return Player.black if self is Player.white else Player.white
