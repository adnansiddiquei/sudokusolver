import numpy as np
from ..utils import has_non_zero_duplicates
import pytest


def test_no_duplicates():
    assert not has_non_zero_duplicates(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    assert not has_non_zero_duplicates([9, 7, 8, 4, 3, 2, 6, 5, 1])


def test_duplicates():
    assert has_non_zero_duplicates(np.array([1, 2, 3, 8, 5, 6, 7, 8, 9]))
    assert has_non_zero_duplicates([9, 7, 8, 4, 3, 2, 2, 5, 1])


def test_errors():
    # Should raise error if anything other than an array is passed in
    with pytest.raises(TypeError):
        has_non_zero_duplicates('test string')

    with pytest.raises(TypeError):
        has_non_zero_duplicates(123)

    # Should raise error if an array of non-ints is passed in
    with pytest.raises(TypeError):
        has_non_zero_duplicates(
            ['hello', 'there', 'this', 'is', 'an', 'array', 'of', 'strings']
        )

    with pytest.raises(TypeError):
        has_non_zero_duplicates([1.2, 5.2])

    # Should raise error if a non 1-D array is passed in
    with pytest.raises(ValueError):
        has_non_zero_duplicates([[1, 2], [3, 4]])

    with pytest.raises(ValueError):
        has_non_zero_duplicates(np.array([[1, 2], [3, 4]]))
