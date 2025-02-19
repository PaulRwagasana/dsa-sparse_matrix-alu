import os

class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, filePath=None):
        """
        Constructor for SparseMatrix.
        Can initialize either from dimensions or from a file.
        """
        print("Initializing SparseMatrix...")  # Debugging
        if filePath:
            self._load_from_file(filePath)
        else:
            if numRows is None or numCols is None:
                raise ValueError("Number of rows and columns must be provided.")
            self.numRows = numRows
            self.numCols = numCols
            self.elements = {}  # Dictionary to store non-zero elements: (row, col) -> value

    def _load_from_file(self, filePath):
        """
        Helper function to load a sparse matrix from a file.
        """
        print(f"Loading matrix from file: {filePath}")  # Debugging
        self.elements = {}
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File not found at {filePath}")  # Debugging
            raise

        # Remove whitespace and empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Read number of rows and columns
        if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
            raise ValueError("Input file has wrong format.")

        self.numRows = int(lines[0].split('=')[1])
        self.numCols = int(lines[1].split('=')[1])

        # Read elements
        for line in lines[2:]:
            if not (line.startswith('(') and line.endswith(')')):
                raise ValueError("Input file has wrong format.")

            # Extract row, column, and value
            row, col, value = map(int, line.strip('()').split(','))
            self.setElement(row, col, value)

    def getElement(self, currRow, currCol):
        """
        Get the value at (currRow, currCol).
        Returns 0 if the element is not stored (implicitly zero).
        """
        if currRow < 0 or currRow >= self.numRows or currCol < 0 or currCol >= self.numCols:
            raise ValueError("Row or column index out of bounds.")
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        """
        Set the value at (currRow, currCol).
        If the value is zero, remove the element from storage.
        """
        if currRow < 0 or currRow >= self.numRows or currCol < 0 or currCol >= self.numCols:
            raise ValueError("Row or column index out of bounds.")

        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def __add__(self, other):
        """
        Add two sparse matrices.
        """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = SparseMatrix(self.numRows, self.numCols)

        # Add elements from self
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value)

        # Add elements from other
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) + value)

        return result

    def __sub__(self, other):
        """
        Subtract two sparse matrices.
        """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result = SparseMatrix(self.numRows, self.numCols)

        # Add elements from self
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value)

        # Subtract elements from other
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) - value)

        return result

    def __mul__(self, other):
        """
        Multiply two sparse matrices.
        """
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in the first matrix must match the number of rows in the second matrix.")

        result = SparseMatrix(self.numRows, other.numCols)

        # Perform multiplication
        for (i, k), v1 in self.elements.items():
            for j in range(other.numCols):
                v2 = other.getElement(k, j)
                if v2 != 0:
                    result.setElement(i, j, result.getElement(i, j) + v1 * v2)

        return result

    def __str__(self):
        """
        String representation of the sparse matrix.
        """
        return f"SparseMatrix({self.numRows}x{self.numCols}): {len(self.elements)} non-zero elements"

    def to_file(self, filePath):
        """
        Save the sparse matrix to a file.
        """
        print(f"Saving result to file: {filePath}")  # Debugging
        with open(filePath, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")


def main():
    """
    Main function to interact with the user and perform matrix operations.
    """
    print("Starting program...")  # Debugging
    try:
        print("Select operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")

        choice = int(input("Enter choice (1/2/3): "))
        if choice not in [1, 2, 3]:
            raise ValueError("Invalid choice. Please enter 1, 2, or 3.")

        # Load matrices from files
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        input_dir = os.path.join(base_dir, "..", "sample_inputs")  # Navigate to the sample_inputs directory

        matrix1 = SparseMatrix(filePath=os.path.join(input_dir, "matrixfile1.txt"))
        matrix2 = SparseMatrix(filePath=os.path.join(input_dir, "matrixfile3.txt"))

        # Perform the selected operation
        if choice == 1:
            result = matrix1 + matrix2
            output_file = os.path.join(input_dir, "result_add.txt")
        elif choice == 2:
            result = matrix1 - matrix2
            output_file = os.path.join(input_dir, "result_sub.txt")
        elif choice == 3:
            result = matrix1 * matrix2
            output_file = os.path.join(input_dir, "result_mul.txt")

        # Save the result to a file
        result.to_file(output_file)
        print(f"Operation completed. Result saved to {output_file}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    print("Calling main()...")  # Debugging
    main()