"""
Implementation of the BacktrackingSolver class, and any associated helper functions.
"""

import numpy as np
import numpy.ma as ma

from numpy.typing import NDArray


class BacktrackingSolver:
    """A class for solving sudoku puzzles using a backtracking algorithm.

    Attributes
    ----------
    board : np.NDArray
        A 9x9 numpy array representing the sudoku board. After the board is solved with ``BacktrackingSolver.solve()``,
        this attribute will hold the solved board. If solver fails, then this will hold the partially solved board that
        the solver managed to reach before realising that the board is not solvable.
    unsolved_board : np.NDArray
        The raw unsolved board that was passed into ``BacktrackingSolver.solve()``.
    is_solved : bool
        A boolean representing whether the board has been solved or not. ``True`` if the board has been solved,
        ``False`` otherwise. It will be ``None`` if ``BacktrackingSolver.solve()`` has not been called or the board
        failed to be solved after calling this method.
    is_solvable : bool
        A boolean representing whether the board is solvable or not. If the board fails to be solved after calling
        ``BacktrackingSolver.solve()``, this attribute will be ``False``. Otherwise, it will be ``None``.
    is_valid : bool
        A boolean representing whether the board that was passed into ``BacktrackingSolver.solve()`` is valid a valid
        sudoku board - i.e., does the board satisfy the constraints of sudoku.

    Examples
    --------
    >>> from sudokusolver import BacktrackingSolver
    >>> unsolved_board = [
    ...     [0, 0, 0, 0, 0, 7, 0, 0, 0],
    ...     [0, 0, 0, 0, 0, 9, 5, 0, 4],
    ...     [0, 0, 0, 0, 5, 0, 1, 6, 9],
    ...     [0, 8, 0, 0, 0, 0, 3, 0, 5],
    ...     [0, 7, 5, 0, 0, 0, 2, 9, 0],
    ...     [4, 0, 6, 0, 0, 0, 0, 8, 0],
    ...     [7, 6, 2, 0, 8, 0, 0, 0, 0],
    ...     [1, 0, 3, 9, 0, 0, 0, 0, 0],
    ...     [0, 0, 0, 6, 0, 0, 0, 0, 0]
    ... ]
    >>> solver = BacktrackingSolver().solve(unsolved_board)
    >>> print(solver.board)
    array([[2, 5, 9, 1, 3, 7, 6, 4, 8],
       [6, 1, 7, 8, 2, 9, 5, 3, 4],
       ...
    """

    def __init__(self):
        self.is_solved, self.is_solvable, self.is_valid = None, None, None
        self.board, self.unsolved_board = None, None

        self._r0, self._c0 = None, None
        self._editable_cells = None

    def _is_board_filled(self) -> bool:
        return np.sum(self.board > 0) == 81

    def _is_board_valid(self) -> bool:
        for r in range(9):
            for c in range(9):
                if self._sudoku_constraint_violated(r, c):
                    return False
        return True

    def _is_cell_editable(self, r: int, c: int) -> bool:
        """
        Returns whether the cell at the given co-ordinates is editable or not. I.e., whether it is one of the cells
        that was originally filled with a 0.

        Parameters
        ----------
        r
            Row index of cell.
        c
            Column index of cell.

        Returns
        -------
        bool
            ``True`` if the cell is editable, ``False`` otherwise.
        """
        return self._editable_cells[r, c]

    def _row_constraint_violated(self, r: int, c: int) -> bool:
        row = ma.masked_array(self.board[r, :])
        row[c] = ma.masked
        row[np.where(row == 0)] = ma.masked

        return self.board[r, c] in row

    def _col_constraint_violated(self, r: int, c: int) -> bool:
        col = ma.masked_array(self.board[:, c])
        col[r] = ma.masked
        col[np.where(col == 0)] = ma.masked

        return self.board[r, c] in col

    def _box_constraint_violated(self, r: int, c: int) -> bool:
        r_range = np.floor(r / 3).astype(int)
        c_range = np.floor(c / 3).astype(int)

        board = ma.masked_array(self.board)
        board[r, c] = ma.masked
        box = board[r_range * 3 : r_range * 3 + 3][:, c_range * 3 : c_range * 3 + 3]
        box[np.where(box == 0)] = ma.masked

        return self.board[r, c] in box

    def _range_violated(self, r: int, c: int) -> bool:
        return self.board[r, c] > 9

    def _sudoku_constraint_violated(self, r: int, c: int) -> bool:
        return (
            self._row_constraint_violated(r, c)
            or self._col_constraint_violated(r, c)
            or self._box_constraint_violated(r, c)
            or self._range_violated(r, c)
        )

    @staticmethod
    def _proceed_to_next_cell(r: int, c: int) -> tuple[int, int]:
        c_next = c + 1 if c < 8 else 0
        r_next = r + 1 if c == 8 else r

        return r_next, c_next

    @staticmethod
    def _backtrack_to_prev_cell(r: int, c: int) -> tuple[int, int]:
        c_prev = c - 1 if c > 0 else 8
        r_prev = r - 1 if c == 0 and r > 0 else r

        return r_prev, c_prev

    def _proceed_until_editable(self, r: int, c: int) -> tuple[int, int]:
        r, c = self._proceed_to_next_cell(r, c)

        while not self._is_cell_editable(r, c):
            r, c = self._proceed_to_next_cell(r, c)

        return r, c

    def _backtrack_until_editable(self, r: int, c: int) -> tuple[int, int]:
        r, c = self._backtrack_to_prev_cell(r, c)

        while not self._is_cell_editable(r, c):
            r, c = self._backtrack_to_prev_cell(r, c)

        return r, c

    def solve(self, unsolved_board: NDArray | list) -> 'BacktrackingSolver':
        """Solves the sudoku puzzle using backtracking.

        If the board is successfully solved, then ``BacktrackingSolver.board`` will hold the solved board and
        ``BacktrackingSolver.is_solved`` will be ``True``. If the board is not solvable, then
        ``BacktrackingSolver.board`` will hold a partial solution at the point that this function determined that the
        board is not solvable, and ``BacktrackingSolver.is_solvable`` will be ``False``. If the board is invalid, i.e.,
        it does not satisfy the constraints of sudoku, then ``BacktrackingSolver.is_valid`` will be ``False``.

        Parameters
        ----------
        unsolved_board
            A 9x9 numpy array or list representing the unsolved sudoku board. The board must only contain values between
            0-9, where 0 represents an empty cell.

        Returns
        -------
        BacktrackingSolver
        """
        self.is_solved = False
        self.is_solvable = True
        self.is_valid = True

        # Raise an error if the provided board is not a numpy array or list
        if not isinstance(unsolved_board, np.ndarray) and not isinstance(
            unsolved_board, list
        ):
            raise ValueError('Provided board must be a numpy array, or a list.')

        self.unsolved_board = np.array(unsolved_board)

        # Raise an error if the provided board is not the correct shape
        if not self.unsolved_board.shape == (9, 9):
            raise ValueError('Provided board must be 9x9.')

        # these are all th cells that our algorithm is allowed to edit
        self._editable_cells = self.unsolved_board == 0

        # This is the working board, this where we will make edits
        self.board = np.copy(self.unsolved_board)

        # Raise an error if the provided board is not valid
        if not self._is_board_valid():
            self.is_solved, self.is_solvable, self.is_valid = False, False, False
            return self

        # Find and set the co-ords of the first editable cell
        self._r0, self._c0 = np.argwhere(self._editable_cells)[0]

        r = self._r0
        c = self._c0

        while not self.is_solved and self.is_solvable:
            self.board[r, c] += 1

            if self._sudoku_constraint_violated(
                r, c
            ):  # If any constraints have been violated
                if self._range_violated(
                    r, c
                ):  # and one of them is the range constraint, self.board[r, c] == 10
                    if (
                        r == self._r0 and c == self._c0
                    ):  # And this is the first editable cell
                        self.is_solvable = (
                            False  # Then the board is not solvable. Exit loop.
                        )
                    else:  # otherwise
                        self.board[r, c] = 0  # reset the cell to 0
                        r, c = self._backtrack_until_editable(
                            r, c
                        )  # and proceed backwards

            else:  # If no constraints have been violated
                if (
                    self._is_board_filled() and self._is_board_valid()
                ):  # and all the cells have been filled, and is valid
                    self.is_solved = True  # Board is is_solved. Exit loop.
                else:  # otherwise
                    r, c = self._proceed_until_editable(
                        r, c
                    )  # proceed to the next editable cell

        return self
