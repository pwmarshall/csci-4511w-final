"""Contains a Bot that plays checkers and a class that acts as a node.

#NOTE#
    To create your own heuristic function to evaluate a board state,
    create a bot class that inherits CheckersBot and override the
    _evaluate method implementing your own heuristic. In the current
    class, the evaluation function is the same as the Board class.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""
import copy
from datetime import datetime


class Choice:
    """Represents a possible choice for the bot.

    Attributes
    ----------
    move : [(int, int), (int, int), Piece[]]
        Move that could be performed in the board.
    value : int
        Represents the advantage that the player has.
        Positive is good, negative is bad.
    depth : int
        Depth where this choice was found in the search.

    """

    def __init__(self, move, value, depth):
        """Initiates the choice with the assigned values.

        Parameters
        -----------
        move : [(int, int), (int, int), Piece[]]
            Move that could be performed in the board.
        value : int
            Represents the advantage that the player has.
            Positive is good, negative is bad.
        depth : int
            Depth where this choice was found in the search.

        """

        self.move = move
        self.value = value
        self.depth = depth

    def __str__(self):
        """Gets a string representing the choice.

        Returns
        -------
        str
            Formatted as MOVE : VALUE

        """
        return str(self.move) + ": " + str(self.value)


class CheckersBot:
    """Bot that selects a move given a checkers board state.

    It is implemented with a minimax algorithm with
    a alpha beta pruning technique. Bases the choices
    on a heuristic algorithm provided by the Board class.

    Attributes
    ----------
    player : Player
        Player that this bot is. It could be white or black.
    depth : int (Default = 6)
        The depth that the algorithm will have. More depth will
        make the system better, but it will also take longer to
        process.

    """

    def __init__(self, player, depth=6):
        """Assigns the player and depth values to it's own variables.

        Parameters
        ----------
        player : Player
            Player that this bot is. It could be white or black.
        depth : int (Default = 6)
            The depth that the algorithm will have. More depth will
            make the system better, but it will also take longer to
            process.

        """

        self.player = player
        self.depth = depth

    def alpha_beta_search(self, board, is_max, current_player, depth, alpha, beta):
        """Minimax algorithm with alpha beta pruning.

        Searches through all the options in the depth selected,
        and returns the one with the best heuristic value.

        Parameters
        ----------
        board : Board
            Board state in which the decision has to be taken.
        is_max : boolean
            Shows if the currents search is max or not.
            Usually used to show if it's the player's
            turn or the opponent's turn.
        current_player : Player
            Indicates which turn it is.
        depth : int
            Current depth of the search.
        alpha : int
            Maximum value found.
        beta : int
            Minimum value found.

        """

        # If the board has a winner stops the search
        winner = board.has_winner()
        if winner == self.player:
            return Choice(board.last_move(), 1000 - depth, depth)
        elif winner == self.player.other:
            return Choice(board.last_move(), -1000 + depth, depth)
        elif winner == "Tie":
            return Choice(board.last_move(), 0 + depth, depth)
        elif depth == self.depth:
            # If the desired depth has been reached, return the current move
            return Choice(board.last_move(), self._evaluate(board), depth)

        # Otherwise, call minimax on each possible board combination
        max_choice = None
        min_choice = None
        candidates = board.get_all_valid_moves(current_player)
        for i in range(len(candidates)):
            move = candidates[i]
            new_board = copy.deepcopy(board)
            new_board.make_move(move)
            result = self.alpha_beta_search(new_board, not is_max, current_player.other, depth + 1, alpha, beta)
            result.move = new_board.last_move()

            if is_max:
                alpha = max(result.value, alpha)
                if alpha >= beta:
                    return result

                if max_choice is None or result.value > max_choice.value:
                    max_choice = result

            else:
                beta = min(result.value, beta)
                if alpha >= beta:
                    return result

                if min_choice is None or result.value < min_choice.value:
                    min_choice = result

        if is_max:
            return max_choice
        else:
            return min_choice

    def select_move(self, board):
        """Selects a move given a board state.

        Parameters
        ----------
        board : Board
            Current board state, with a position and a list of possible moves.

        Returns
        --------
        [(int, int), (int, int), Pieces[]]
            Move selected by the AI.
        """
        choice = self.alpha_beta_search(board, True, self.player, 0, -1000, 1000)
        return choice.move

    def _evaluate(self, board):
        """Evaluates the board state with an integer.

        #NOTE#
            This method is only here to provide a system for creating new bots
            with different heuristic functions to evaluate the board. Currently
            the evaluation function is the same as the board one, but it could be
            changed creating a class that inherits this one and overrides this
            method.

        Parameters
        -----------
        board : Board
            Board state with a position to evaluate.

        Returns
        --------
        int
            Representing the current advantage for the player.
        """
        return board.evaluate(self.player)
