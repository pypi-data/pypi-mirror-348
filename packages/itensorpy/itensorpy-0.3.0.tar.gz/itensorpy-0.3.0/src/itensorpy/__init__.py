"""
iTensorPy: A Python package for tensor calculations in general relativity.

This package provides tools for working with metrics, computing Christoffel symbols,
Riemann and Ricci tensors, Einstein tensors, and other tensor operations relevant
to general relativity and differential geometry.
"""

__version__ = '0.2.5'

# Import all public classes and functions
from .metric import Metric
from .christoffel import ChristoffelSymbols
from .riemann import RiemannTensor
from .ricci import RicciTensor, RicciScalar
from .einstein import EinsteinTensor
from .curvature import CurvatureInvariants
from .utils import (
    generate_index_riemann,
    generate_index_ricci,
    generate_index_christoffel,
    lower_indices,
    custom_simplify
)
from . import spacetimes
from .matrix_ops import MatrixOps
from .tensor_ops import TensorND
from .differential_ops import Field

__all__ = [
    'Metric', 'ChristoffelSymbols', 'RiemannTensor',
    'RicciTensor', 'RicciScalar', 'EinsteinTensor',
    'CurvatureInvariants', 'spacetimes',
    'generate_index_riemann', 'generate_index_ricci',
    'generate_index_christoffel', 'lower_indices',
    'custom_simplify',
    # New modules
    'MatrixOps', 'TensorND', 'Field'
]
