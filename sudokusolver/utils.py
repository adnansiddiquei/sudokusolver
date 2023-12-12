import numpy as np
import re
from numpy.typing import NDArray


def save_board_to_txt(board: NDArray[np.int8] | list, output_file: str) -> None:
    """Save a sudoku board to a .txt file.

    Parameters
    ----------
    board
        A 9x9 numpy array representing the sudoku board. 0's represent empty cells.
    output_file
        The path to the .txt file to save the sudoku board to.
    """
    # Check that the file extension is .txt
    file_extension = output_file.split('.')[-1]

    if file_extension != 'txt':
        raise ValueError(
            'Output file must be a .txt file. Please check the output file extension is .txt.'
        )

    # Check that the board is a list or numpy array
    if not isinstance(board, list) and not isinstance(board, np.ndarray):
        raise TypeError(
            'Provided board must be a list or numpy array. Please check the board is a list or numpy array, '
            'and try again.'
        )

    # Convert the board to a numpy array if it is a list
    if isinstance(board, list):
        try:
            board = np.array(board, dtype=np.int8)
        except ValueError:
            raise ValueError(
                'Provided board must be a 9x9 array of ints, containing no non-numerical characters. '
                'Please check the board is an array of ints, and try again.'
            )
    else:
        # Check that the board contains only ints
        if board.dtype != int:
            raise TypeError(
                'Provided board must be a 9x9 array of ints. Please check the board is an array of ints, '
                'and try again.'
            )

    # Check that the board is 9x9
    if board.shape != (9, 9):
        raise ValueError(
            'Provided board must be 9x9. Please check the board is 9x9, and try again.'
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

    The provided board must be formatted like below:
    ```
    000|007|000
    000|009|504
    000|050|169
    ---+---+---
    080|000|305
    075|000|290
    406|000|080
    ---+---+---
    762|080|000
    103|900|000
    000|600|000
    ```

    Parameters
    ----------
    input_file
        The path to the .txt file containing the sudoku board.

    Returns
    -------
    np.NDArray
        A 9x9 numpy array representing the sudoku board. 0's represent empty cells.
    """
    # Check that the file extension is .txt
    file_extension = input_file.split('.')[-1]

    if file_extension != 'txt':
        raise ValueError(
            'Input file must be a .txt file. Please check the input file extension is .txt.'
        )

    # Try reading the file and reading it in
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(
            'Input file not found. Please check the input file path is correct.'
        )

    lines = [line.strip() for line in lines]

    # This regex matches a line of numbers, with optional | separators
    num_line = r'(\d{3}\|?\d{3}\|?\d{3})'

    # Check that the file contains 9 rows of numbers
    if np.sum([bool(re.match(num_line, line)) for line in lines]) != 9:
        raise ValueError(
            'Input file does not contain 9 rows of numbers. Please check the input file contains 9 rows of '
            'numbers, and is formatted correctly.'
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
