import numpy as np
import re
from numpy.typing import NDArray


def save_board_to_txt(board: NDArray[np.int8] | list, output_file: str) -> None:
    pass


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
