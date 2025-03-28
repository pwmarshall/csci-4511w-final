"""Contains a class that executes checkers games.

It bridges the game state (Board) with the AI (Bots or User).

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

from checkers.board import Board
from checkers.player import Player
from checkers.display import Display


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

    def simulate(self, bot_white, bot_black, print_game=False, starting_player=Player.white):
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
        for _ in range(self.num_of_games):
            board = Board()
            self.display.assign_board(board)

            current_turn = starting_player
            winner = None
            while winner is None:
                choice = []
                if current_turn == Player.white:
                    choice = bot_white.select_move(board)
                else:
                    choice = bot_black.select_move(board)
                board.make_move(choice)

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


        print("White wins: " + str(self.white_wins))
        print("Black wins: " + str(self.black_wins))
        print("Ties: " + str(self.ties))
