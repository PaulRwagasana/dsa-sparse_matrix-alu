from sparse_matrix_op import SparseMatrix

sparse_matrix_one = '../sample_inputs/easy_sample_03_1.txt'
sparse_matrix_two = '../sample_inputs/easy_sample_03_2.txt'
sparse_matrix_three = '../sample_inputs/easy_sample_02_2.txt'
sparse_matrix_four = '../sample_inputs/easy_sample_02_3.txt'


def main():
    

    operation = input("Enter operation (Add, Subtract, Multiply): ").strip().lower()

    try:
        matrix1 = SparseMatrix(matrix_file_path=sparse_matrix_one)
        matrix2 = SparseMatrix(matrix_file_path=sparse_matrix_two)
        matrix3 = SparseMatrix(matrix_file_path=sparse_matrix_three)
        matrix4 = SparseMatrix(matrix_file_path=sparse_matrix_four)

        if operation == "add":
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            result = matrix3.multiply(matrix4)
        else:
            print("Invalid operation. Please enter Add, Subtract, or Multiply.")
            return

        result.print_readable()
    
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()