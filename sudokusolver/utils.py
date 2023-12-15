import numpy as np
import re
from numpy.typing import NDArray
import os
from ctypes import CDLL, c_int, POINTER

# Create a function to interface the cutils.c has_non_zero_duplicates function
cwd = os.path.dirname(os.path.abspath(__file__))
cutils = CDLL(f'{cwd}/cutils.so')

cutils.has_non_zero_duplicates.argtypes = [POINTER(c_int), c_int]
cutils.has_non_zero_duplicates.restype = c_int


def has_non_zero_duplicates(arr: NDArray[np.integer] | list) -> bool:
    """Check if a 1-dimensional array contains any non-zero duplicates.

    Parameters
    ----------
    arr
        The 1-dimensional array to check.

    Returns
    -------
    bool
        True if the array contains non-zero duplicates, False otherwise.
    """
    # Error handling
    type_error_message = (
        '(sudokusolver) Provided array must be a numpy array or list of ints. Please check the array is a '
        'numpy array or list of ints, and try again.'
    )

    value_error_message = (
        '(sudokusolver) Provided array must be 1-dimensional. Please check the array is 1-dimensional,'
        ' and try again.'
    )

    # Check that the array is a numpy array or list
    if not isinstance(arr, np.ndarray) and not isinstance(arr, list):
        raise TypeError(type_error_message)

    arr = np.array(arr)

    # Check that the array contains only ints
    if not np.issubdtype(arr.dtype, np.integer):
        raise TypeError(type_error_message)

    # Check that the array is 1-d
    if arr.ndim != 1:
        raise ValueError(value_error_message)

    arr_len = len(arr)
    arr = (c_int * arr_len)(*arr)

    return bool(cutils.has_non_zero_duplicates(arr, arr_len))


def save_board_to_txt(board: NDArray[np.int8] | list, output_file: str) -> None:
    """Save a sudoku board to a .txt file.

    Parameters
    ----------
    board
        A 9x9 numpy array representing the sudoku board. 0's represent empty cells.
    output_file
        The path to the .txt file to save the sudoku board to.

    Raises
    ------
    ValueError
        If any of the following occur: the file extension of the output file is not .txt; the board is not a list or
        numpy array; the board is not 9x9.
    TypeError
        If the board contains non-ints.
    """
    # Check that the file extension is .txt
    file_extension = output_file.split('.')[-1]

    if file_extension != 'txt':
        raise ValueError(
            '(sudokusolver) Output file must be a .txt file. Please check the output file extension is .txt.'
        )

    # Check that the board is a list or numpy array
    if not isinstance(board, list) and not isinstance(board, np.ndarray):
        raise TypeError(
            '(sudokusolver) Provided board must be a list or numpy array. Please check the board is a list or numpy '
            'array, and try again.'
        )

    # Convert the board to a numpy array if it is a list
    if isinstance(board, list):
        try:
            board = np.array(board, dtype=np.int8)
        except ValueError:
            raise ValueError(
                '(sudokusolver) Provided board must be a 9x9 array of ints, containing no non-numerical characters. '
                'Please check the board is an array of ints, and try again.'
            )
    else:
        # Check that the board contains only ints
        if not np.issubdtype(board.dtype, np.integer):
            raise TypeError(
                '(sudokusolver) Provided board must be a 9x9 array of ints. Please check the board is an array of '
                'ints, and try again.'
            )

    # Check that the board is 9x9
    if board.shape != (9, 9):
        raise ValueError(
            '(sudokusolver) Provided board must be 9x9. Please check the board is 9x9, and try again.'
        )

    # Convert the board to a string
    def convert_num_line_to_str(line):
        """Converts a list of ints into a string of numbers, with | separators after every 3 numbers."""
        return ''.join(
            [
                f'{num}|' if (i + 1) % 3 == 0 and i != 8 else f'{num}'
                for i, num in enumerate(line)
            ]
        )

    rendered_lines = []

    for i, line in enumerate(board):
        rendered_lines += [convert_num_line_to_str(line)]

        # Add a separator line after every 3 lines
        if (i + 1) % 3 == 0 and i != 8:
            rendered_lines += ['---+---+---']

    rendered_lines = [f'{line}\n' for line in rendered_lines]

    # Write the string to the output file, overwriting any existing file
    try:
        with open(output_file, 'w') as f:
            f.writelines(rendered_lines)
    except FileNotFoundError:
        # The default error is good enough here
        raise


def parse_input_file(input_file: str) -> NDArray[np.int8]:
    """Parse a .txt file containing a sudoku board into a numpy array.

    See sudokusolver/inputs/input.txt for an example of the expected format.

    Parameters
    ----------
    input_file
        The path to the .txt file containing the sudoku board.

    Raises
    ------
    ValueError
        If any of the following occur: the file extension of the input file is not .txt; the file does not contain
        exactly 9 rows of numbers; the file contains non-numerical characters; the file contains numbers outside the
        range 0-9.
    FileNotFoundError
        If the input file does not exist.

    Returns
    -------
    np.NDArray
        A 9x9 numpy array representing the sudoku board. 0's represent empty cells.
    """
    # Check that the file extension is .txt
    file_extension = input_file.split('.')[-1]

    if file_extension != 'txt':
        raise ValueError(
            '(sudokusolver) Input file must be a .txt file. Please check the input file extension is .txt.'
        )

    # Try reading the file and reading it in
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(
            '(sudokusolver) Input file not found. Please check the input file path is correct.'
        )

    lines = [line.strip() for line in lines]

    # This regex matches a line of numbers, with optional | separators
    num_line = r'(\d{3}\|?\d{3}\|?\d{3})'

    # Check that the file contains 9 rows of numbers
    if np.sum([bool(re.match(num_line, line)) for line in lines]) != 9:
        raise ValueError(
            '(sudokusolver) Input file does not contain 9 rows of numbers. Please check the input file contains 9 rows '
            'of numbers, and is formatted correctly.'
        )

    # Render the lines into a numpy array
    def convert_num_line_to_list(line):
        """Converts a string of numbers into a list of ints, after removing any | separators."""
        return [int(num) for num in line.replace('|', '')]

    rendered_lines = []

    for line in lines:
        # Skip through any arbitrary lines that don't match the regex
        if re.match(num_line, line):
            rendered_lines += [convert_num_line_to_list(line)]

    return np.array(rendered_lines, dtype=np.int8)
