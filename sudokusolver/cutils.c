#include <stdio.h>

/**
 * Checks if there are duplicate numbers in an integer array of arbitrary length, ignoring zeros.
 *
 * @param array A pointer to the first element of the array to be checked.
 * @param length The number of elements in the array (should be 9 for a sudoku row, column or box).
 *
 * @return An integer where 1 represents that a duplicate was found and 0 means no duplicates.
 */
int has_non_zero_duplicates(int *array, int length) {
    for (int i = 0; i < length - 1; i++) { // Loop over each element in the array
        if (array[i] != 0) { // Ignore zeros
            for (int j = i + 1; j < length; j++) { // Loop over each element after the current element
                if (array[i] == array[j]) {
                    return 1; // Found a duplicate
                }
            }
        }
    }

    return 0; // No duplicates found
}
