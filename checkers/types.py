# from checkers.piece import Piece #circular import

type Position = tuple[int, int] #Position (row, col)
type Move = tuple[Position, Position, list["Piece"]] #Move (position, next_position, pieces_to_delete)
