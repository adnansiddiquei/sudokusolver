import pytest
import numpy as np
import numpy.ma as ma

from sudokusolver import BacktrackingSolver

# The unsolved and solved boards below are from: https://sandiway.arizona.edu/sudoku/examples.html
unsolved_board = np.array(
    [
        [0, 0, 2, 6, 0, 7, 0, 1, 0],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]
)

# This is unsolved_board, with everything but the last line AND positions [6, 0] and [6, 6] solved
partially_solved_board = np.array(
    [
        [0, 3, 5, 2, 6, 9, 7, 8, 0],
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [0, 1, 9, 3, 2, 6, 0, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]
)

# This is fully solved version of unsolved_board and partially_solved_board
solved_board = np.array(
    [
        [4, 3, 5, 2, 6, 9, 7, 8, 1],
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 3, 2, 6, 8, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9],
    ]
)

# This is an unsolvable, but completely valid board.
# Board acquired from http://sudopedia.enjoysudoku.com/Invalid_Test_Cases.html
unsolvable_valid_board = np.array(
    [
        [0, 0, 9, 0, 2, 8, 7, 0, 0],
        [8, 0, 6, 0, 0, 4, 0, 0, 5],
        [0, 0, 3, 0, 0, 0, 0, 0, 4],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 7, 1, 3, 4, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2],
        [3, 0, 0, 0, 0, 0, 5, 0, 0],
        [9, 0, 0, 4, 0, 0, 8, 0, 7],
        [0, 0, 1, 2, 5, 0, 3, 0, 0],
    ]
)


def test_incorrect_board_shape():
    """
    BacktrackingSolver should raise a ValueError if the board is not a 9x9 square.
    """
    with pytest.raises(ValueError):
        BacktrackingSolver().solve(np.array([[0, 1]]))


def test_invalid_board():
    """
    Tests that the BacktrackingSolver.is_valid == False and BacktrackingSolver.is_solvable == False when the
    board is not valid, and therefore unsolvable:
        - The board contains values other than 0-9
        - The board contains duplicate values in a row
        - The board contains duplicate values in a column
        - The board contains duplicate values in a 3x3 square
    """
    # The board contains values other than 0-9
    backtracking_solver = BacktrackingSolver()
    bad_board = unsolved_board.copy()
    bad_board[6, 4] = 10
    BacktrackingSolver().solve(bad_board)

    assert (
        backtracking_solver.is_valid is False
        and backtracking_solver.is_solvable is False
        and backtracking_solver.is_solved is False
    )

    # The board contains duplicate values in a row
    backtracking_solver = BacktrackingSolver()
    bad_board = unsolved_board.copy()
    bad_board[1, 1] = 4
    bad_board[1, 7] = 4
    BacktrackingSolver().solve(bad_board)

    assert (
        backtracking_solver.is_valid is False
        and backtracking_solver.is_solvable is False
        and backtracking_solver.is_solved is False
    )

    # The board contains duplicate values in a column
    backtracking_solver = BacktrackingSolver()
    bad_board = unsolved_board.copy()
    bad_board[1, 6] = 8
    bad_board[7, 6] = 8
    BacktrackingSolver().solve(bad_board)

    assert (
        backtracking_solver.is_valid is False
        and backtracking_solver.is_solvable is False
        and backtracking_solver.is_solved is False
    )

    # The board contains duplicate values in a 3x3 square
    backtracking_solver = BacktrackingSolver()
    bad_board = unsolved_board.copy()
    bad_board[0, 0] = 3
    bad_board[1, 1] = 3
    BacktrackingSolver().solve(bad_board)

    assert (
        backtracking_solver.is_valid is False
        and backtracking_solver.is_solvable is False
        and backtracking_solver.is_solved is False
    )


def test_unsolvable_board():
    """
    Tests that BacktrackingSolver.is_valid == True and BacktrackingSolver.is_solvable == False when a valid board
    is passed in, but it is not a solvable board
    """
    backtracking_solver = BacktrackingSolver().solve(unsolvable_valid_board)

    assert (
        backtracking_solver.is_valid is True
        and backtracking_solver.is_solvable is False
        and backtracking_solver.is_solved is False
    )


def test_valid_board():
    """
    Tests that the solver solves a valid board.
        - tests that it solves an unsolved board
        - tests that it solves a board and leaves the initial values unchanged
    """
    backtracking_solver = BacktrackingSolver().solve(partially_solved_board)

    # Check that the board is solved
    assert np.array_equal(backtracking_solver.board, solved_board)

    # Check that these are correctly set
    assert (
        backtracking_solver.is_valid is True
        and backtracking_solver.is_solvable is True
        and backtracking_solver.is_solved is True
    )

    # Check that the initial values are unchanged

    # First, create a masked array duplicate of backtracking_solver.board, with everything except the initial values
    # masked out
    initial_values_in_partially_solved_board = ma.array(
        backtracking_solver.board, mask=unsolved_board == 0
    )

    # Second, place the same mask on solved_board
    initial_values_in_solved_board = ma.array(
        solved_board, mask=initial_values_in_partially_solved_board.mask
    )

    # Check that the un-masked (initial) values are equal
    assert ma.allequal(
        initial_values_in_partially_solved_board, initial_values_in_solved_board
    )
