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
import checkers.constants as constant
from bots.minimaxbot import MiniMaxBot
from bots.randombot import RandomBot
from bots.mctsbot import MCTSBot
from bots.user import User


def main():
    """Game running example."""

    # Pick both players, User or RandomBot require a Player parameter. 
    # MiniMax requires an additional depth parameter
    black_bot = MiniMaxBot(Player.black, 7)
    white_bot = MCTSBot(Player.white, 200)

    # Start Game class selecting how many games will be played.
    game = Game(50)

    # Start the program indicating the white player, the black one,
    # a boolean that requests printing on the console (True prints
    # the board), and who will have the first turn.
    game.simulate(white_bot, black_bot, constant.PRINT_GAME, Player.white)


if __name__ == '__main__':
    main()
