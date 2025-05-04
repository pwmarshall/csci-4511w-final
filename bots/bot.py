
from checkers.board import Board, Move, Position
from abc import ABC, abstractmethod


class Bot(ABC):
    @abstractmethod
    def select_move(self, board: Board) -> Move:
        pass