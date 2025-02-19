
class SparseMatrix:
    def __init__(self, num_rows=None, num_cols=None, matrix_file_path=None):
        self.rows = 0
        self.cols = 0
        self.data = {}  # Dictionary to store (row, col): value

        if matrix_file_path:
            self.load_from_file(matrix_file_path)
        elif num_rows is not None and num_cols is not None:
            self.rows = num_rows
            self.cols = num_cols
        else:
            raise ValueError(
                "Must provide either file path or row/col dimensions")

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f]  # Remove whitespace

                self.rows = self.split_function(lines[0])
                self.cols = self.split_function(lines[1])


                for line in lines[2:]:
                    if not line:
                        continue
                    line = line.replace(" ", "")
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    parts = self.manual_split(line[1:-1])
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")
                    row, col, value = self.convert_to_int(parts)
                    self.set_element(row, col, value)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except ValueError as e:
            raise ValueError(f"Input file has wrong format: {e}")
        
    def manual_split(self, comma_separated_str):
        parts = []
        current = ""
        for char in comma_separated_str:
            if char == ",":
                parts.append(current)
                current = ""
            else:
                current += char
        parts.append(current)  # Append the last part
        return parts


        
    def convert_to_string(self, line):
        if num == 0:
            return "0"
        result = ""
        negative = num < 0
        num = -num if negative else num
        while num > 0:
            result = chr((num % 10) + ord('0')) + result
            num //= 10
        return "-" + result if negative else result
    
    def split_function(self, line):
        """Extracts the number after '=' in a line manually."""
        found = False
        num_str = ""
        for char in line:
            if found:
                num_str += char
            if char == '=':
                found = True
        return self.convert_to_int([num_str])[0]
    
    def convert_to_int(self, str_list):
        """Manually converts a list of strings to integers."""
        int_list = []
        for s in str_list:
            num = 0
            sign = 1
            if s[0] == '-':  # Handle negative numbers
                sign = -1
                s = s[1:]
            for char in s:
                num = num * 10 + (ord(char) - ord('0'))  # Convert character to integer
            int_list.append(num * sign)
        return int_list

    def set_element(self, row, col, value):
        self.data[(row, col)] = value

    def get_element(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data.get((row, col), 0)  # Default to 0 if not found
        else:
            raise IndexError("Row or column index out of bounds")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices must have the same dimensions for addition")
        result = SparseMatrix(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                # print(self.get_element(row, col), other.get_element(row, col))
                result.set_element(row, col, self.get_element(
                    row, col) + other.get_element(row, col))
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices must have the same dimensions for subtraction")

        result = SparseMatrix(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                result.set_element(row, col, self.get_element(
                    row, col) - other.get_element(row, col))
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(
            "Number of columns in first matrix must be equal to number of rows in second matrix for multiplication"
        )
        

        result = SparseMatrix(self.rows, other.cols)

        for (i, k), val1 in self.data.items():  # Iterate only over nonzero elements
            for j in range(other.cols):
                val2 = other.get_element(k, j)
                if val2 != 0:
                    if (i, j) in result.data:
                        result.data[(i, j)] += val1 * val2
                    else:
                        result.data[(i, j)] = val1 * val2

        return result

    


    def __str__(self):
        matrix_str = ""
        for i in range(self.rows):
            row_str = ""
            for j in range(self.cols):
                row_str += self.convert_to_string(self.get_element(i, j)) + " "
            matrix_str += row_str + "\n"
        return matrix_str

    def print_readable(self, max_rows=10, max_cols=10):
        """Prints a readable representation of the sparse matrix.

        Args:
            max_rows (int, optional): Maximum number of rows to print. Defaults to 10.
            max_cols (int, optional): Maximum number of columns to print. Defaults to 10.
        """

        if self.rows > max_rows or self.cols > max_cols:
            print(
                f"Matrix is large ({self.rows}x{self.cols}). Showing only top-left {max_rows}x{max_cols} elements.")

        for i in range(min(self.rows, max_rows)):
            row_str = ""
            for j in range(min(self.cols, max_cols)):
                row_str += str(self.get_element(i, j)).rjust(5) + \
                    " "
            print(row_str)

        if self.rows > max_rows or self.cols > max_cols:
            print("...")
