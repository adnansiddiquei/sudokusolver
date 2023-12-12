import numpy as np
from ..utils import parse_input_file
import os
import pytest

cwd = os.path.dirname(os.path.abspath(__file__))

parsed_board = np.array(
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


def test_valid_filepath_and_valid_board():
    # Perfect board
    assert np.array_equal(
        parse_input_file(f'{cwd}/sample_inputs/valid_input1.txt'), parsed_board
    )

    # Board missing the row separators
    assert np.array_equal(
        parse_input_file(f'{cwd}/sample_inputs/valid_input2.txt'), parsed_board
    )

    # Board missing a few column separators
    assert np.array_equal(
        parse_input_file(f'{cwd}/sample_inputs/valid_input3.txt'), parsed_board
    )

    # Board missing a few column and row separators
    assert np.array_equal(
        parse_input_file(f'{cwd}/sample_inputs/valid_input4.txt'), parsed_board
    )

    # A board with literally just a 9x9 grid of numbers, no separators
    assert np.array_equal(
        parse_input_file(f'{cwd}/sample_inputs/valid_input5.txt'), parsed_board
    )


def test_valid_filepath_and_invalid_board():
    with pytest.raises(ValueError):
        # this one is missing a number at the end of a row
        parse_input_file(f'{cwd}/sample_inputs/invalid_input1.txt')

    with pytest.raises(ValueError):
        # this one has a number > 9
        parse_input_file(f'{cwd}/sample_inputs/invalid_input2.txt')

    with pytest.raises(ValueError):
        # this one is missing a number in the middle of the row, it has been replaced by a space
        parse_input_file(f'{cwd}/sample_inputs/invalid_input3.txt')

    with pytest.raises(ValueError):
        # this one is missing a vertical bar separator
        parse_input_file(f'{cwd}/sample_inputs/invalid_input4.txt')

    with pytest.raises(ValueError):
        # this one is missing a vertical bar separator
        parse_input_file(f'{cwd}/sample_inputs/empty_file.txt')


def test_invalid_filepath():
    with pytest.raises(FileNotFoundError):
        parse_input_file(f'{cwd}/sample_inputs/does_not_exist.txt')

    with pytest.raises(ValueError):
        parse_input_file(f'{cwd}/sample_inputs/not_txt_file.pdf')
