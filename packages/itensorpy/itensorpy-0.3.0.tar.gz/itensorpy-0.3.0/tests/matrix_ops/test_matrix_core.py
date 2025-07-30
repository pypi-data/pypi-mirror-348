import pytest
import numpy as np
from sympy import Matrix, ImmutableMatrix
from itensorpy.matrix_ops.core import MatrixOps

class TestMatrixOps:
    
    def test_init_from_lists(self):
        data = [[1, 2], [3, 4]]
        mat = MatrixOps(data)
        assert mat.shape == (2, 2)
        assert mat.mat[0, 0] == 1
        assert mat.mat[0, 1] == 2
        assert mat.mat[1, 0] == 3
        assert mat.mat[1, 1] == 4
    
    def test_init_from_sympy_matrix(self):
        sym_mat = Matrix([[1, 2], [3, 4]])
        mat = MatrixOps(sym_mat)
        assert mat.shape == (2, 2)
        assert mat.mat == sym_mat
    
    def test_init_from_sympy_immutable_matrix(self):
        sym_mat = ImmutableMatrix([[1, 2], [3, 4]])
        mat = MatrixOps(sym_mat)
        assert mat.shape == (2, 2)
        assert mat.mat == sym_mat
    
    def test_transpose(self):
        data = [[1, 2], [3, 4]]
        mat = MatrixOps(data)
        transposed = mat.T
        assert transposed[0, 0] == 1
        assert transposed[0, 1] == 3
        assert transposed[1, 0] == 2
        assert transposed[1, 1] == 4
    
    def test_to_numpy(self):
        data = [[1, 2], [3, 4]]
        mat = MatrixOps(data)
        np_array = mat.to_numpy()
        assert isinstance(np_array, np.ndarray)
        assert np_array.shape == (2, 2)
        assert np.array_equal(np_array, np.array([[1, 2], [3, 4]])) 