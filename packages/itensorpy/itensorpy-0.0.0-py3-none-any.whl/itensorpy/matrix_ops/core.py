# core.py

from sympy import Matrix as _SymMatrix
from sympy import ImmutableMatrix as _SymImMatrix

from .multiplication import MultiplicationMixin
from .determinant    import DeterminantMixin
from .eigen          import EigenMixin
from .linear_solve   import LinearSolveMixin

class MatrixOps(MultiplicationMixin,
                DeterminantMixin,
                EigenMixin,
                LinearSolveMixin):
    

    def __init__(self, data):
        # Akceptujemy: listę list, numpy.ndarray, sympy.Matrix/ImmutableMatrix
        if isinstance(data, (_SymMatrix, _SymImMatrix)):
            self.mat = data
        else:
            self.mat = _SymMatrix(data)

    @property
    def shape(self):
        return self.mat.shape

    @property
    def T(self):
        return self.mat.T

    def to_numpy(self):
        return __import__('numpy').array(self.mat.tolist())
