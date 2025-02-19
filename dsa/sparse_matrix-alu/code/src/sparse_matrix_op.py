class SparseMatrix:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Remove any whitespace and empty lines
        lines = [line.strip() for line in lines if line.strip()]
        
        # Read the number of rows and columns
        if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
            raise ValueError("Input file has wrong format")
        
        numRows = int(lines[0].split('=')[1])
        numCols = int(lines[1].split('=')[1])
        
        matrix = cls(numRows, numCols)
        
        # Read the elements
        for line in lines[2:]:
            if not (line.startswith('(') and line.endswith(')')):
                raise ValueError("Input file has wrong format")
            
            row, col, value = map(int, line.strip('()').split(','))
            matrix.setElement(row, col, value)
        
        return matrix

    def getElement(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def __add__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")
        
        result = SparseMatrix(self.numRows, self.numCols)
        
        # Add elements from self
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value)
        
        # Add elements from other
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) + value)
        
        return result

    def __sub__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        
        result = SparseMatrix(self.numRows, self.numCols)
        
        # Add elements from self
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value)
        
        # Subtract elements from other
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) - value)
        
        return result

    def __mul__(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        
        result = SparseMatrix(self.numRows, other.numCols)
        
        for (i, k), v1 in self.elements.items():
            for j in range(other.numCols):
                v2 = other.getElement(k, j)
                if v2 != 0:
                    result.setElement(i, j, result.getElement(i, j) + v1 * v2)
        
        return result

    def to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")
