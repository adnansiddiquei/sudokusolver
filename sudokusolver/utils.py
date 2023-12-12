import numpy as np
import re
from numpy.typing import NDArray
import os
import time

from ._backtracking_solver import BacktrackingSolver


def handler(cwd: str, argv: list, output_dir: str = None) -> None:
    """Handle the command line arguments passed to the script.

    Parameters
    ----------
    cwd
        The current working directory, the directory the script was called from.
    argv
        The command line arguments passed to the script.
    output_dir
        The directory to save the output file to. If ``None``, then the output file will be saved to
        ``{cwd}/sudokusolver/outputs``.
    """
    # Check that the correct number of arguments have been passed
    if len(argv) != 2:
        raise ValueError(
            '(sudokusolver) Please provide the input path as a command line arguments. '
            'For example: `python -m sudokusolver sudokusolver/inputs/input.txt`'
        )

    # Parse the input file
    input_file = f'{cwd}/{argv[1]}'
    board = parse_input_file(input_file)

    # This will be the directory that the output file is saved to, it points to sudokusolver/outputs
    output_dir = f'{argv[0]}'[0:-11] + 'outputs' if output_dir is None else output_dir

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def compute_output_file_name(dir):
        """Computes the file name for the output file, based on the existing files in the output directory."""
        # Get all the files matching the regex pattern output\d+\.txt
        file_list = os.listdir(dir)
        output_files = [
            filename for filename in file_list if re.match(r'output\d+\.txt', filename)
        ]

        # Get all the numbers already in those files
        numbers = [
            int(re.search(r'output(\d+)\.txt', filename).group(1))
            for filename in output_files
        ]
        sorted_numbers = np.sort(numbers)

        # Find the next lowest number
        if len(sorted_numbers) == 0:
            return f'{dir}/output1.txt'
        else:
            for i, num in enumerate(sorted_numbers):
                if num != i + 1:
                    # if we find a gap in the numbers, i.e., we have output1.txt and output3.txt
                    return f'{dir}/output{i + 1}.txt'
            else:
                # if we don't have a gap, then just return the next number in the sequence
                return f'{dir}/output{i + 2}.txt'

    output_filepath = compute_output_file_name(output_dir)

    print('Solving sudoku...\n')

    start_time = time.time()
    solver = BacktrackingSolver().solve(board)

    end_time = time.time()
    duration = end_time - start_time

    if solver.is_solved:
        save_board_to_txt(solver.board, output_filepath)
        print(f'Sudoko board has been solved. It was solved in {duration:.2f} seconds.')
        print(f'The solved board has been saved to {output_filepath}.')
    elif not solver.is_solvable and not solver.is_valid:
        print('The provided board is not valid. It violates the sudoku constraints.')
    elif not solver.is_solvable and solver.is_valid:
        print('The provided board is not solvable, it has no solutions.')

    print('')


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
                '(sudokusolver)  Provided board must be a 9x9 array of ints, containing no non-numerical characters. '
                'Please check the board is an array of ints, and try again.'
            )
    else:
        # Check that the board contains only ints
        if not np.issubdtype(board.dtype, np.integer):
            raise TypeError(
                '(sudokusolver)  Provided board must be a 9x9 array of ints. Please check the board is an array of '
                'ints, and try again.'
            )

    # Check that the board is 9x9
    if board.shape != (9, 9):
        raise ValueError(
            '(sudokusolver)  Provided board must be 9x9. Please check the board is 9x9, and try again.'
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
            '(sudokusolver)  Input file does not contain 9 rows of numbers. Please check the input file contains 9 rows '
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
