# src/itensorpy/tensor_ops/arithmetic.py
import sympy as sp
from sympy.tensor.array import tensorproduct

class ArithmeticMixin:
    """
    Mixin zawierający operacje arytmetyczne dla tensorów.
    """

    def add(self, other):
        """
        Dodawanie tensorów tej samej wielkości.
        Parametry:
            other (TensorND): Tensor do dodania
        Zwraca:
            TensorND: Nowy tensor z sumą elementów
        """
        if not hasattr(other, 'data'):
            raise TypeError("other must be a TensorND instance")
        
        if self.shape != other.shape:
            raise ValueError(f"Cannot add tensors with different shapes: {self.shape} vs {other.shape}")
        
        result = self.data + other.data
        return self.__class__(result)
    
    def subtract(self, other):
       
        if not hasattr(other, 'data'):
            raise TypeError("other must be a TensorND instance")
        
        if self.shape != other.shape:
            raise ValueError(f"Cannot subtract tensors with different shapes: {self.shape} vs {other.shape}")
        
        result = self.data - other.data
        return self.__class__(result)
    
    def multiply_scalar(self, scalar):
       
        result = self.data * scalar
        return self.__class__(result)

    def __mul__(self, other):
        # tensor * tensor (elementwise) albo tensor * skalar
        if hasattr(other, 'data'):
            self._check_shape_match(other)
            return self.__class__(self.data * other.data)
        else:
            return self.__class__(self.data * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # tensor / tensor (elementwise) albo tensor / skalar
        if hasattr(other, 'data'):
            self._check_shape_match(other)
            return self.__class__(self.data / other.data)
        else:
            return self.__class__(self.data / other)

    def __matmul__(self, other):
        # zawsze tensorprodukt, wspiera dowolne wymiary
        return self.__class__(tensorproduct(self.data, other.data))
