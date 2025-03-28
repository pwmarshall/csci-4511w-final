"""Main class used to start games.

#NOTE#
    To use, select two players, initiate a Game class
    introducing the number of games to be played, and
    simulate.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

from checkers.game import Game
from checkers.player import Player
from bots.checkersbot import CheckersBot
from bots.randombot import RandomBot
from bots.user import User


def main():
    """Game running example."""

    # Pick both players, User or RandomBot require a Player parameter...
    black_bot = CheckersBot(Player.black, 6)
    # ...and CheckerBot does too. An optional parameter is an integer
    # that represents the depth for the Bot. By default is 6.
    white_bot = CheckersBot(Player.white, 6)

    # Start Game class selecting how many games will be played.
    game = Game(10)

    # Start the program indicating the white player, the black one,
    # a boolean that requests printing on the console (True prints
    # the board), and who will have the first turn.
    game.simulate(white_bot, black_bot, False, Player.white)


if __name__ == '__main__':
    main()
