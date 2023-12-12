import pytest

from ..utils import handler
import os
import shutil

cwd = f'{os.path.dirname(os.path.abspath(__file__))}/../..'
output_dir = f'{cwd}/sudokusolver/tests/test_outputs'
main_file = f'{cwd}/sudokusolver/__main__.py'


def cleanup(dir):
    """Remove a directory and all of its contents if it exists."""
    if os.path.exists(dir):
        shutil.rmtree(dir)


def test_solvable_sudoku():
    """Test that a solvable sudoku is solved and saved to the correct output file."""
    argv = [main_file, 'sudokusolver/tests/sample_inputs/valid_input1.txt']

    cleanup(output_dir)

    handler(cwd, argv, output_dir)
    assert os.path.exists(f'{output_dir}/output1.txt')

    handler(cwd, argv, output_dir)
    assert os.path.exists(f'{output_dir}/output2.txt')

    cleanup(output_dir)


def test_invalid_sudoku():
    """Test that an invalid sudoku raises a ValueError and does not create an output file."""
    argv = [main_file, 'sudokusolver/tests/sample_inputs/invalid_input1.txt']

    cleanup(output_dir)

    with pytest.raises(ValueError):
        handler(cwd, argv, output_dir)

    assert not os.path.exists(f'{output_dir}/output1.txt')
    cleanup(output_dir)


def test_invalid_argv1():
    """Test that an invalid sudoku raises a ValueError and does not create an output file."""
    argv = [main_file, 'sudokusolver/tests/random_dir/random_file.txt']

    cleanup(output_dir)

    with pytest.raises(FileNotFoundError):
        handler(cwd, argv, output_dir)

    assert not os.path.exists(f'{output_dir}/output1.txt')
    cleanup(output_dir)


def test_unsolvable_sudoku():
    """Test that an unsolvable sudoku does not create an output file."""
    argv = [main_file, 'sudokusolver/tests/sample_inputs/unsolvable_input1.txt']

    cleanup(output_dir)

    handler(cwd, argv, output_dir)
    assert not os.path.exists(f'{output_dir}/output1.txt')

    cleanup(output_dir)
