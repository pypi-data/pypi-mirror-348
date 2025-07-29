#next lib
import numpy as np


def gaussian_elimination(A):
    matrix = np.array(A, dtype=float)  # Convert input to a NumPy array for easy indexing

    rows, cols = matrix.shape  # Rows and columns automatically determined

    # Forward elimination
    for i in range(rows):
        if matrix[i][i] == 0:  # Ensure pivot is nonzero
            for j in range(i + 1, rows):
                if matrix[j][i] != 0:
                    matrix[[i, j]] = matrix[[j, i]]  # Swap rows
                    break

        pivot = matrix[i][i]
        matrix[i] /= pivot  # Normalize leading coefficient to 1

        for j in range(i + 1, rows):
            multiplier = matrix[j][i]
            matrix[j] -= multiplier * matrix[i]  # Eliminate below pivot

    # Backward elimination (Reduced Row Echelon Form)
    for i in range(rows - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            multiplier = matrix[j][i]
            matrix[j] -= multiplier * matrix[i]  # Eliminate above pivot

    solutions = matrix[:, -1]  # Last column contains solutions
    print("Returned Solutions:", solutions)
    print("Returned Reduced Row Echelon Form:\n", matrix)
    return solutions, matrix
