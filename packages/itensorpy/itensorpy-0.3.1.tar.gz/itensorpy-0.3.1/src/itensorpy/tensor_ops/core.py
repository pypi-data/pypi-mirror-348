# src/itensorpy/tensor_ops/core.py

import numpy as _np
from sympy import MutableDenseNDimArray as _SymArray
from collections.abc import Iterable as _Iterable

from .arithmetic import ArithmeticMixin
from .shape import ShapeMixin
from .contraction import ContractionMixin
from .einsum import EinsumMixin

class TensorND(ArithmeticMixin, ShapeMixin, ContractionMixin, EinsumMixin):
    """
    Główna klasa n-wymiarowych tensorów.
    Przyjmuje na wejściu:
      - sympy.MutableDenseNDimArray,
      - numpy.ndarray,
      - dowolne zagnieżdżone listy/tuple.
    Przechowuje wewnętrznie sympy.MutableDenseNDimArray.
    """

    def __init__(self, data):
        # 1) NumPy → konwertujemy przez listy
        if isinstance(data, _np.ndarray):
            data = data.tolist()

        # 2) list/tuple lub Iterable → budujemy sympy-ową tablicę
        if isinstance(data, (list, tuple)) or (isinstance(data, _Iterable) and not isinstance(data, (str, bytes))):
            self.data = _SymArray(data)
        # 3) już sympy MutableDenseNDimArray
        elif isinstance(data, _SymArray):
            self.data = data
        else:
            raise TypeError(
                f"TensorND: nieobsługiwany typ danych {type(data).__name__}"
            )

        # Kształt i wymiar
        self._shape = tuple(self.data.shape)
        self._ndim = len(self._shape)

    @property
    def shape(self):
        """Zwraca krotkę (d1, d2, ..., dn)."""
        return self._shape

    @property
    def ndim(self):
        """Liczba wymiarów tensora."""
        return self._ndim

    @classmethod
    def from_numpy(cls, array: _np.ndarray):
        """Buduje TensorND z numpy.ndarray."""
        return cls(array)

    def to_numpy(self):
        """Zwraca numpy.ndarray z danych."""
        return _np.array(self.data.tolist())
