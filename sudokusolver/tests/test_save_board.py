import numpy as np
from ..utils import save_board_to_txt
import os
import pytest

cwd = os.path.dirname(os.path.abspath(__file__))

solved_board = np.array(
    [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)

solved_board_array = [
    '000|007|000\n',
    '000|009|504\n',
    '000|050|169\n',
    '---+---+---\n',
    '080|000|305\n',
    '075|000|290\n',
    '406|000|080\n',
    '---+---+---\n',
    '762|080|000\n',
    '103|900|000\n',
    '000|600|000\n',
]


def cleanup(files_to_remove: list[str]):
    """Remove the files in the list if they exist."""
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)


def test_valid_filepath_and_valid_board():
    # Save the board and asset the file exists
    save_board_to_txt(solved_board, f'{cwd}/test_output1.txt')
    assert os.path.exists(f'{cwd}/test_output1.txt')

    # Reload the board from the saved file and check it has been saved fine
    with open(f'{cwd}/test_output1.txt', 'r') as f:
        reloaded_board = f.readlines()

    assert np.array_equal(reloaded_board, solved_board_array)

    # Cleanup
    cleanup([f'{cwd}/test_output1.txt'])


def test_valid_filepath_and_invalid_board():
    # Invalid shape
    with pytest.raises(ValueError):
        save_board_to_txt(np.array([[1, 2, 3], [4, 5, 6]]), f'{cwd}/test_output1.txt')

    # Contains an invalid value, but valid shape
    with pytest.raises(ValueError):
        copy_of_solved_board = list(np.copy(solved_board))
        copy_of_solved_board[0][3] = 'a'
        save_board_to_txt(copy_of_solved_board, f'{cwd}/test_output1.txt')


def test_invalid_filepath():
    # Incorrect file extension
    with pytest.raises(ValueError):
        save_board_to_txt(solved_board, f'{cwd}/test_output1.csv')

    # A folder that does not exist
    with pytest.raises(FileNotFoundError):
        save_board_to_txt(solved_board, f'{cwd}/random_folder/test_output1.txt')
