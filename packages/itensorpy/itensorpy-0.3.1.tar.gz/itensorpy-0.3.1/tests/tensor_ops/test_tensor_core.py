import pytest
import numpy as np
from sympy import symbols, MutableDenseNDimArray
from itensorpy.tensor_ops.core import TensorND

class TestTensorNDCore:
    
    def test_init_from_list(self):
        data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        tensor = TensorND(data)
        assert tensor.shape == (2, 2, 2)
        assert tensor.ndim == 3
    
    def test_init_from_numpy(self):
        np_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        tensor = TensorND(np_array)
        assert tensor.shape == (2, 2, 2)
        assert tensor.ndim == 3
    
    def test_init_from_sympy_array(self):
        sym_array = MutableDenseNDimArray([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        tensor = TensorND(sym_array)
        assert tensor.shape == (2, 2, 2)
        assert tensor.ndim == 3
    
    def test_init_invalid_type(self):
        with pytest.raises(TypeError):
            TensorND(42)  # Invalid type should raise TypeError
    
    def test_from_numpy_class_method(self):
        np_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        tensor = TensorND.from_numpy(np_array)
        assert tensor.shape == (2, 2, 2)
        assert tensor.ndim == 3
    
    def test_to_numpy(self):
        data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        tensor = TensorND(data)
        np_array = tensor.to_numpy()
        assert isinstance(np_array, np.ndarray)
        assert np_array.shape == (2, 2, 2)
        assert np.array_equal(np_array, np.array(data))
    
    def test_symbolic_tensors(self):
        a, b, c, d = symbols('a b c d')
        data = [[a, b], [c, d]]
        tensor = TensorND(data)
        assert tensor.shape == (2, 2)
        assert tensor.ndim == 2
        assert tensor.data[0, 0] == a
        assert tensor.data[0, 1] == b
        assert tensor.data[1, 0] == c
        assert tensor.data[1, 1] == d 