"""
Tests for error handling in iTensorPy.

These tests verify that appropriate errors are raised when the package is used incorrectly.
"""

import pytest
import sympy as sp
from sympy import symbols

from itensorpy.metric import Metric
from itensorpy.christoffel import ChristoffelSymbols
from itensorpy.riemann import RiemannTensor
from itensorpy.ricci import RicciTensor, RicciScalar
from itensorpy.einstein import EinsteinTensor
from itensorpy.spacetimes import minkowski


def test_metric_initialization_errors():
    """Test that errors are raised when metric is initialized incorrectly."""
    # Empty coordinates list should raise error
    with pytest.raises(ValueError):
        Metric(components={}, coordinates=[])
    
    # Creating metric with dictionary but wrong indices should raise errors
    t, x, y, z = symbols('t x y z')
    coordinates = [t, x, y, z]
    
    # Out of range index
    with pytest.raises(IndexError):
        Metric(components={(0, 4): 1}, coordinates=coordinates)


def test_christoffel_errors():
    """Test that errors are raised when Christoffel symbols are accessed incorrectly."""
    # Initialize empty ChristoffelSymbols
    christoffel = ChristoffelSymbols()
    
    # Trying to get component without computing should raise error
    with pytest.raises(ValueError):
        christoffel.get_component(0, 0, 0)
    
    # Trying to get nonzero components without computing should raise error
    with pytest.raises(ValueError):
        christoffel.get_nonzero_components()


def test_riemann_errors():
    """Test that errors are raised when Riemann tensor is accessed incorrectly."""
    # Initialize empty RiemannTensor
    riemann = RiemannTensor()
    
    # Trying to get component without computing should raise error
    with pytest.raises(ValueError):
        riemann.get_component_up(0, 0, 0, 0)
    
    with pytest.raises(ValueError):
        riemann.get_component_down(0, 0, 0, 0)
    
    # Trying to get nonzero components without computing should raise error
    with pytest.raises(ValueError):
        riemann.get_nonzero_components_down()


def test_ricci_errors():
    """Test that errors are raised when Ricci tensor is accessed incorrectly."""
    # Initialize empty RicciTensor
    ricci = RicciTensor()
    
    # Trying to get component without computing should raise error
    with pytest.raises(ValueError):
        ricci.get_component(0, 0)
    
    # Trying to get nonzero components without computing should raise error
    with pytest.raises(ValueError):
        ricci.get_nonzero_components()
    
    # Initialize empty RicciScalar
    scalar = RicciScalar()
    
    # Trying to get value without computing should raise error
    with pytest.raises(ValueError):
        scalar.get_value()


def test_einstein_errors():
    """Test that errors are raised when Einstein tensor is accessed incorrectly."""
    # Initialize empty EinsteinTensor
    einstein = EinsteinTensor()
    
    # Trying to get components without computing should raise error
    with pytest.raises(ValueError):
        einstein.get_component_lower(0, 0)
    
    with pytest.raises(ValueError):
        einstein.get_component_upper(0, 0)
    
    # Trying to get nonzero components without computing should raise error
    with pytest.raises(ValueError):
        einstein.get_nonzero_components_lower()
    
    with pytest.raises(ValueError):
        einstein.get_nonzero_components_upper()


def test_mixed_metric_errors():
    """Test errors from mixing metrics from different manifolds."""
    # Create a metric
    metric = minkowski()
    
    # Create Ricci tensor and scalar from this metric
    ricci = RicciTensor.from_metric(metric)
    scalar = RicciScalar.from_metric(metric)
    
    # Create another metric with different coordinates
    t, r, theta = symbols('t r theta')
    other_metric = Metric(components=sp.diag(-1, 1, r**2), coordinates=[t, r, theta])
    
    # Trying to create Einstein tensor with mismatched metrics should raise error
    with pytest.raises(ValueError):
        # This implicitly tries to use ricci.metric for both tensors
        scalar.metric = other_metric
        EinsteinTensor.from_ricci(ricci, scalar) 