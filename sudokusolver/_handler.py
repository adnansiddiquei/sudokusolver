import numpy as np
import re
import os
import time
from .utils import parse_input_file, save_board_to_txt

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

    Raises
    ------
    ValueError
        If the incorrect number of command line arguments have been passed.
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
