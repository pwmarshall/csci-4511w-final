"""Contains a class that executes checkers games.

It bridges the game state (Board) with the AI (Bots or User).

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

from checkers.board import Board, BoardHash
from checkers.player import Player
from checkers.display import Display
from bots.bot import Bot
from bots.mctsbot import MCTSBot
import checkers.constants as constant

from datetime import datetime


class Game:
    """Class that represents a number of games of checkers.

    Attributes
    -----------
    num_of_games : int
        Number of games that will be performed. Default is 1.
    black_wins : int
        Number of wins by the black player.
    white_wins : int
        Number of wins by the white player.
    ties : int
        Number of ties that had occurred.

    """

    def __init__(self, num_of_games=1):
        """Sets the game system to it's initial stage.

        Parameters
        -----------
        num_of_games : int (Default = 1)
            Number of games that will be simulated or player.

        """
        self.num_of_games = num_of_games
        self.black_wins = 0
        self.white_wins = 0
        self.ties = 0
        self.display = Display()

    def simulate(self, bot_white: Bot, bot_black: Bot, print_game=constant.PRINT_GAME, starting_player=Player.white):
        """Simulates a number of games by two agents.

        Parameters
        -----------
        bot_white : Bot
            Bot that will play for the white side.
        bot_black : Bot
            Bot that will play for the black side.
        print_game : boolean (Default = False)
            If it's True it will print the board at each move.
            If it is not, then no board would be printed.
        starting_player : Player
            The player who would make the first move.

        """
        last_time = datetime.now()
        print(f"Starting simulation at {last_time.time()}")

        for _ in range(self.num_of_games):
            board = BoardHash()
            if isinstance(bot_white, MCTSBot):
                bot_white.reset_tree()
            if isinstance(bot_black, MCTSBot):
                bot_black.reset_tree()
            self.display.assign_board(board)

            current_turn = starting_player
            winner = None
            while winner is None:
                choice = []
                if current_turn == Player.white:
                    if print_game: print("White Turn")
                    choice = bot_white.select_move(board)
                    if print_game: print(f"White choose: ({choice[0][0]}, {choice[0][1]}) to ({choice[1][0]}, {choice[1][1]})")
                else:
                    if print_game: print("Black Turn")
                    choice = bot_black.select_move(board)
                    if print_game: print(f"Black choose: ({choice[0][0]}, {choice[0][1]}) to ({choice[1][0]}, {choice[1][1]})")

                board.make_move(choice)
                self.display.assign_board(board)

                winner = board.has_winner()

                if print_game:
                    self.display.print_board()
                    # Uncomment to see the number of pieces left
                    # self.display.print_pieces_left()

                current_turn = current_turn.other

            if winner is Player.white:
                self.white_wins += 1
                print("White WIN")
            elif winner is Player.black:
                self.black_wins += 1
                print("Black WIN")
            elif winner == "Tie":
                self.ties += 1
                print("TIE")

            print(f"Game {_} done, took {datetime.now() - last_time}")
            last_time = datetime.now()


        print("White wins: " + str(self.white_wins))
        print("Black wins: " + str(self.black_wins))
        print("Ties: " + str(self.ties))
