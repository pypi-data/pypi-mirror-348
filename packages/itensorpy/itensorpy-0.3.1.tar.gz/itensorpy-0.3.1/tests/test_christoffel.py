"""
Tests for the Christoffel symbols module.
"""

import pytest
import sympy as sp
from sympy import symbols, sin, cos, diff, simplify

from itensorpy.metric import Metric
from itensorpy.christoffel import ChristoffelSymbols
from itensorpy.spacetimes import schwarzschild


def test_christoffel_from_metric():
    """Test computing Christoffel symbols from a metric."""
    # Use a simple 2D metric
    r, theta = symbols('r theta')
    coordinates = [r, theta]
    
    # Metric for a 2D sphere
    g = sp.Matrix([[1, 0], [0, r**2]])
    metric = Metric(components=g, coordinates=coordinates)
    
    # Compute Christoffel symbols
    christoffel = ChristoffelSymbols.from_metric(metric)
    
    # Check specific known components for the 2D sphere
    assert christoffel.get_component(0, 1, 1) == 0
    assert christoffel.get_component(1, 0, 1) == 1/r
    assert christoffel.get_component(1, 1, 0) == 1/r
    
    # The rest should be zero
    assert christoffel.get_component(0, 0, 0) == 0
    assert christoffel.get_component(0, 0, 1) == 0
    assert christoffel.get_component(0, 1, 0) == 0
    assert christoffel.get_component(1, 0, 0) == 0
    
    # Test the non-zero components method
    nonzero = christoffel.get_nonzero_components()
    assert len(nonzero) == 2  # Only two non-zero components for 2D sphere
    assert (1, 0, 1) in nonzero
    assert (1, 1, 0) in nonzero


def test_schwarzschild_christoffel():
    """Test Christoffel symbols for the Schwarzschild metric."""
    # Create Schwarzschild metric
    metric = schwarzschild()
    t, r, theta, phi = metric.coordinates
    M = metric.params[0]
    
    # Compute Christoffel symbols
    christoffel = ChristoffelSymbols.from_metric(metric)
    
    # Check some specific known components using sympy's simplify to compare
    # the mathematical equivalence rather than exact string matching
    assert simplify(christoffel.get_component(0, 0, 1) - M/(r**2 * (1 - 2*M/r))) == 0
    assert simplify(christoffel.get_component(1, 0, 0) - M*(1 - 2*M/r)/(r**2)) == 0
    assert simplify(christoffel.get_component(1, 1, 1) - (-M/(r**2 * (1 - 2*M/r)))) == 0
    assert simplify(christoffel.get_component(1, 2, 2) - (-(1 - 2*M/r)*r)) == 0
    assert simplify(christoffel.get_component(1, 3, 3) - (-(1 - 2*M/r)*r*sin(theta)**2)) == 0
    assert simplify(christoffel.get_component(2, 1, 2) - 1/r) == 0
    assert simplify(christoffel.get_component(2, 3, 3) - (-sin(theta)*cos(theta))) == 0
    assert simplify(christoffel.get_component(3, 1, 3) - 1/r) == 0
    assert simplify(christoffel.get_component(3, 2, 3) - cos(theta)/sin(theta)) == 0


def test_manual_christoffel_calculation():
    """Test manual calculation of Christoffel symbols."""
    # Create a simple metric
    t, x = symbols('t x')
    coordinates = [t, x]
    
    # Metric with time-dependent component
    g = sp.Matrix([[-1, 0], [0, t**2]])
    metric = Metric(components=g, coordinates=coordinates)
    
    # Calculate one Christoffel symbol manually
    # For Γ^1_01, we need: (1/2)g^1σ(∂_0 g_σ1 + ∂_1 g_0σ - ∂_σ g_01)
    # Since g^11 = 1/t^2, g_11 = t^2, and other terms are zero or don't contribute
    # Γ^1_01 = (1/2)(1/t^2)(∂_0 g_11) = (1/2)(1/t^2)(2t) = 1/t
    
    christoffel = ChristoffelSymbols.from_metric(metric)
    assert sp.simplify(christoffel.get_component(1, 0, 1) - 1/t) == 0
    
    # Another component: Γ^1_10 = Γ^1_01 by symmetry
    assert sp.simplify(christoffel.get_component(1, 1, 0) - 1/t) == 0
    
    # Check a component that should be zero
    assert christoffel.get_component(0, 0, 0) == 0
    assert christoffel.get_component(0, 1, 1) == 0 