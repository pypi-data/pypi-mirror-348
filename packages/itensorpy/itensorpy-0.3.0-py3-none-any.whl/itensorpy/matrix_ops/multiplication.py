# multiplication.py

from sympy import Matrix

class MultiplicationMixin:
   
    def multiply(self, other):
        """Multiply this matrix by another matrix"""
        if not hasattr(other, 'mat'):
            raise TypeError("other must be MatrixOps")
        return self.__class__(self.mat * other.mat)

    def matmul(self, other):
        """Alias for multiply"""
        return self.multiply(other)

    def inverse(self):
        """Compute the inverse of this matrix"""
        try:
            inv = self.mat.inv()
        except Exception as e:
            raise ValueError(f"inverse: matrix is singular ({e})")
        return self.__class__(inv)
