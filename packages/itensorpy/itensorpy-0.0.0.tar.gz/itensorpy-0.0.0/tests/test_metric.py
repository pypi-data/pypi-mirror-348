"""
Tests for the metric module.
"""

import pytest
import sympy as sp
from sympy import symbols, diag, sin

from itensorpy.metric import Metric
from itensorpy.spacetimes import schwarzschild


def test_metric_initialization():
    """Test basic initialization of a metric tensor."""
    t, r, theta, phi = symbols('t r theta phi')
    coordinates = [t, r, theta, phi]
    
    # Create diagonal metric
    g = diag(-1, 1, r**2, r**2 * sin(theta)**2)
    metric = Metric(components=g, coordinates=coordinates)
    
    assert metric.dimension == 4
    assert metric.g[0, 0] == -1
    assert metric.g[1, 1] == 1
    assert metric.g[2, 2] == r**2
    assert metric.g[3, 3] == r**2 * sin(theta)**2
    
    # Test metric with dictionary input
    components = {
        (0, 0): -1,
        (1, 1): 1,
        (2, 2): r**2,
        (3, 3): r**2 * sin(theta)**2
    }
    metric2 = Metric(components=components, coordinates=coordinates)
    
    assert metric2.dimension == 4
    assert metric2.g[0, 0] == -1
    assert metric2.g[1, 1] == 1
    assert metric2.g[2, 2] == r**2
    assert metric2.g[3, 3] == r**2 * sin(theta)**2


def test_metric_inverse():
    """Test calculation of inverse metric."""
    # Use a simple Minkowski metric
    t, x, y, z = symbols('t x y z')
    coordinates = [t, x, y, z]
    
    g = diag(-1, 1, 1, 1)
    metric = Metric(components=g, coordinates=coordinates)
    
    g_inv = metric.inverse
    
    assert g_inv[0, 0] == -1
    assert g_inv[1, 1] == 1
    assert g_inv[2, 2] == 1
    assert g_inv[3, 3] == 1
    
    # Test with r-dependent components
    r, theta, phi = symbols('r theta phi')
    g2 = diag(1, r**2, r**2 * sin(theta)**2)
    metric2 = Metric(components=g2, coordinates=[r, theta, phi])
    
    g2_inv = metric2.inverse
    
    assert g2_inv[0, 0] == 1
    assert g2_inv[1, 1] == 1/r**2
    assert g2_inv[2, 2] == 1/(r**2 * sin(theta)**2)


def test_schwarzschild_metric():
    """Test the Schwarzschild metric."""
    # Use predefined Schwarzschild metric
    metric = schwarzschild()
    
    # Extract coordinates and parameters
    t, r, theta, phi = metric.coordinates
    M = metric.params[0]
    
    # Check metric components
    assert sp.simplify(metric.g[0, 0] - (-(1 - 2*M/r))) == 0
    assert sp.simplify(metric.g[1, 1] - (1/(1 - 2*M/r))) == 0
    assert sp.simplify(metric.g[2, 2] - r**2) == 0
    assert sp.simplify(metric.g[3, 3] - (r**2 * sin(theta)**2)) == 0
    
    # Check inverse components
    g_inv = metric.inverse
    assert sp.simplify(g_inv[0, 0] - (-1/(1 - 2*M/r))) == 0
    assert sp.simplify(g_inv[1, 1] - (1 - 2*M/r)) == 0
    assert sp.simplify(g_inv[2, 2] - (1/r**2)) == 0
    assert sp.simplify(g_inv[3, 3] - (1/(r**2 * sin(theta)**2))) == 0


def test_component_access():
    """Test accessing metric components."""
    t, r, theta, phi = symbols('t r theta phi')
    coordinates = [t, r, theta, phi]
    
    # Create metric
    g = diag(-1, 1, r**2, r**2 * sin(theta)**2)
    metric = Metric(components=g, coordinates=coordinates)
    
    # Test component access
    assert metric.component(0, 0) == -1
    assert metric.component(1, 1) == 1
    assert metric.component(2, 2) == r**2
    assert metric.component(3, 3) == r**2 * sin(theta)**2
    
    # Test inverse component access
    assert metric.inverse_component(0, 0) == -1
    assert metric.inverse_component(1, 1) == 1
    assert metric.inverse_component(2, 2) == 1/r**2
    assert metric.inverse_component(3, 3) == 1/(r**2 * sin(theta)**2)
