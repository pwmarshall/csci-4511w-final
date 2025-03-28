"""Holds the constants for a checkers game.

(CC) 2020 Alex Ayza, Barcelona, Spain
alexayzaleon@gmail.com
"""

BOARD_DIMENSION = 8
"""int : Dimension of the board.

Usually, a checkers board is 8x8. If this field is modified, the board will shrink
    or grow accordingly.
    
"""

ROWS_OF_PIECES = 3
"""int : Rows that will be filled with pieces.

On the creation of the board, it is filled with pieces.
    This integers represents how many rows will have pieces, including
    both sides. A common checkers game has 3 rows of pieces.
    
"""

MAX_MOVES_WITHOUT_CAPTURE = 50
"""int : Moves that need to pass without a capture before declaring a tie."""

POSITIONAL_EVALUATION = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 3, 0, 3, 0]
]
"""Used to translate how much valuable a piece is in a given position.

This matrix takes into account that the pieces on the first row are strong,
    that the ones about to promote into a king are valuable too, and that the
    control of the center is important.

"""

COLUMNS_TO_LETTERS = {1: 'a',
                      2: 'b',
                      3: 'c',
                      4: 'd',
                      5: 'e',
                      6: 'f',
                      7: 'g',
                      8: 'h'}
"""Used to translate the columns position to letters for user board reading."""
