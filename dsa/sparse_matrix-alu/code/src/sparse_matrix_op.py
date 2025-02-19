#!/usr/bin/env python3
import os

class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, filePath=None):
        """
        Constructor for SparseMatrix.
        Initializes from dimensions or loads from a file.
        """
        print("Initializing SparseMatrix...")
        self.elements = {}  # Dictionary to store non-zero elements: (row, col) -> value
        
        if filePath:
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"Error: File not found at {filePath}")
            self._load_from_file(filePath)
        else:
            if numRows is None or numCols is None:
                raise ValueError("Number of rows and columns must be provided.")
            self.numRows = numRows
            self.numCols = numCols
    
    def _load_from_file(self, filePath):
        """Helper function to load a sparse matrix from a file."""
        print(f"Loading matrix from file: {filePath}")
        with open(filePath, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
            raise ValueError("Input file has wrong format.")

        self.numRows = int(lines[0].split('=')[1])
        self.numCols = int(lines[1].split('=')[1])

        for line in lines[2:]:
            if not (line.startswith('(') and line.endswith(')')):
                raise ValueError("Input file has wrong format.")

            try:
                row, col, value = map(int, line.strip('()').split(','))
                self.setElement(row, col, value)
            except ValueError:
                raise ValueError("Input file has wrong format.")

    def getElement(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def __add__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = SparseMatrix(self.numRows, self.numCols)
        for (row, col), value in {**self.elements, **other.elements}.items():
            result.setElement(row, col, self.getElement(row, col) + other.getElement(row, col))
        return result

    def __sub__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result = SparseMatrix(self.numRows, self.numCols)
        for (row, col), value in {**self.elements, **other.elements}.items():
            result.setElement(row, col, self.getElement(row, col) - other.getElement(row, col))
        return result

    def __mul__(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in the first matrix must match the number of rows in the second matrix.")

        result = SparseMatrix(self.numRows, other.numCols)
        for (i, k), v1 in self.elements.items():
            for j in range(other.numCols):
                v2 = other.getElement(k, j)
                if v2 != 0:
                    result.setElement(i, j, result.getElement(i, j) + v1 * v2)
        return result

    def __str__(self):
        return f"SparseMatrix({self.numRows}x{self.numCols}): {len(self.elements)} non-zero elements"

    def to_file(self, filePath):
        with open(filePath, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")
        print(f"Result saved to {filePath}")


def main():
    print("Starting program...")
    try:
        print("Select operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        
        choice = int(input("Enter choice (1/2/3): "))
        if choice not in [1, 2, 3]:
            raise ValueError("Invalid choice. Please enter 1, 2, or 3.")
        
        # Verify file paths
        file1 = "dsa-sparse_matrix-alu/dsa/sparse_matrix-alu/sample_inputs/matrixfile1.txt"
        file2 = "dsa-sparse_matrix-alu/dsa/sparse_matrix-alu/sample_inputs/matrixfile3.txt"
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise FileNotFoundError("One or both input files are missing.")
        
        matrix1 = SparseMatrix(filePath=file1)
        matrix2 = SparseMatrix(filePath=file2)

        print("Matrix 1 loaded:", matrix1)
        print("Matrix 2 loaded:", matrix2)

        if choice == 1:
            result = matrix1 + matrix2
            output_file = "dsa-sparse_matrix-alu/dsa/sparse_matrix-alu/sample_inputs/result_add.txt"
        elif choice == 2:
            result = matrix1 - matrix2
            output_file = "dsa-sparse_matrix-alu/dsa/sparse_matrix-alu/sample_inputs/result_sub.txt"
        elif choice == 3:
            result = matrix1 * matrix2
            output_file = "dsa-sparse_matrix-alu/dsa/sparse_matrix-alu/sample_inputs/result_mul.txt"
        
        result.to_file(output_file)
        print(f"Operation completed. Result saved to {output_file}")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
