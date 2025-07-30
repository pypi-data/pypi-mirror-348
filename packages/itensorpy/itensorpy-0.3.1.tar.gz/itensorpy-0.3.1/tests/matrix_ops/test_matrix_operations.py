import pytest
import numpy as np
from sympy import Matrix, symbols, simplify
from itensorpy.matrix_ops.core import MatrixOps

class TestMatrixMultiplication:
    
    def test_matrix_multiplication(self):
        mat1 = MatrixOps([[1, 2], [3, 4]])
        mat2 = MatrixOps([[2, 0], [1, 3]])
        
        result = mat1.multiply(mat2)
        expected = Matrix([[4, 6], [10, 12]])
        
        assert result.shape == (2, 2)
        for i in range(2):
            for j in range(2):
                assert result.mat[i, j] == expected[i, j]
    
    def test_matrix_multiplication_symbolic(self):
        a, b, c, d = symbols('a b c d')
        mat1 = MatrixOps([[a, b], [c, d]])
        mat2 = MatrixOps([[1, 0], [0, 1]])
        
        result = mat1.multiply(mat2)
        assert result.shape == (2, 2)
        assert result.mat[0, 0] == a
        assert result.mat[0, 1] == b
        assert result.mat[1, 0] == c
        assert result.mat[1, 1] == d

class TestMatrixDeterminant:
    
    def test_determinant_2x2(self):
        mat = MatrixOps([[1, 2], [3, 4]])
        det = mat.determinant()
        assert det == -2
    
    def test_determinant_3x3(self):
        mat = MatrixOps([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        det = mat.determinant()
        assert det == 0
    
    def test_determinant_symbolic(self):
        a, b, c, d = symbols('a b c d')
        mat = MatrixOps([[a, b], [c, d]])
        det = mat.determinant()
        assert simplify(det - (a*d - b*c)) == 0

class TestMatrixEigen:
    
    def test_eigenvalues(self):
        mat = MatrixOps([[3, 1], [1, 3]])
        eigenvals = mat.eigenvalues()
        # Eigenvalues should be 2 and 4
        assert set([float(val) for val in eigenvals]) == {2.0, 4.0}
    
    def test_eigenvectors(self):
        mat = MatrixOps([[3, 1], [1, 3]])
        eigenvecs = mat.eigenvectors()
        # Check that we got the correct number of eigenvectors
        assert len(eigenvecs) == 2

class TestMatrixLinearSolve:
    
    def test_linear_solve(self):
        # System: 2x + y = 5, x + 3y = 10
        A = MatrixOps([[2, 1], [1, 3]])
        b = MatrixOps([[5], [10]])
        
        # Solution should be x=1, y=3
        solution = A.solve(b)
        assert solution.shape == (2, 1)
        assert float(solution.mat[0, 0]) == 1.0
        assert float(solution.mat[1, 0]) == 3.0
    
    def test_linear_solve_symbolic(self):
        a, b, c, d, e, f = symbols('a b c d e f')
        A = MatrixOps([[a, b], [c, d]])
        B = MatrixOps([[e], [f]])
        
        # This should return a symbolic solution
        solution = A.solve(B)
        assert solution.shape == (2, 1) 