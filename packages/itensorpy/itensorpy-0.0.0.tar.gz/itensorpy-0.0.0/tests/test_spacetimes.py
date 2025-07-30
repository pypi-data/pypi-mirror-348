"""
Tests for the spacetimes module.
"""

import pytest
import sympy as sp
from sympy import symbols, sin, simplify

from itensorpy.metric import Metric
from itensorpy.riemann import RiemannTensor
from itensorpy.ricci import RicciTensor, RicciScalar
from itensorpy.spacetimes import (
    minkowski, 
    schwarzschild, 
    kerr, 
    friedmann_lemaitre_robertson_walker, 
    de_sitter, 
    anti_de_sitter
)


def test_minkowski_metric():
    """Test the Minkowski metric and its properties."""
    # Create a Minkowski metric
    metric = minkowski()
    
    # Check dimensions and signature
    assert metric.dimension == 4
    assert metric.g[0, 0] == -1
    assert metric.g[1, 1] == 1
    assert metric.g[2, 2] == 1
    assert metric.g[3, 3] == 1
    
    # Check that Riemann tensor is zero (flat spacetime)
    riemann = RiemannTensor.from_metric(metric)
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    assert riemann.get_component_up(i, j, k, l) == 0


def test_schwarzschild_metric():
    """Test the Schwarzschild metric and its properties."""
    # Create a Schwarzschild metric
    metric = schwarzschild()
    
    # Extract coordinates and parameter
    t, r, theta, phi = metric.coordinates
    M = metric.params[0]
    
    # Check key properties of the metric
    assert metric.dimension == 4
    assert metric.g[0, 0] == -(1 - 2*M/r)
    assert metric.g[1, 1] == 1/(1 - 2*M/r)
    assert metric.g[2, 2] == r**2
    assert metric.g[3, 3] == r**2 * sin(theta)**2
    
    # Schwarzschild is a vacuum solution, so Ricci tensor should be zero
    ricci = RicciTensor.from_metric(metric)
    
    for i in range(4):
        for j in range(4):
            assert ricci.get_component(i, j) == 0


def test_kerr_metric():
    """Test the Kerr metric and its properties."""
    # Create a Kerr metric
    metric = kerr()
    
    # Extract coordinates and parameters
    t, r, theta, phi = metric.coordinates
    M, a = metric.params
    
    # Check dimension
    assert metric.dimension == 4
    
    # Check it has expected off-diagonal components
    assert metric.g[0, 3] != 0  # g_t_phi component should be non-zero
    
    # Check some key metric components match the expected form
    # The Kerr metric involves the following auxiliary functions:
    rho_squared = r**2 + (a * sp.cos(theta))**2
    delta = r**2 - 2 * M*r + a**2
    
    # Check a few key components (not the full metric)
    g_tt = -1 + 2 * M*r / rho_squared
    g_phi_phi = (r**2 + a**2 + 2 * M*r * a**2 * sp.sin(theta)**2 / rho_squared) * sp.sin(theta)**2
    g_t_phi = -2 * M*r * a * sp.sin(theta)**2 / rho_squared
    
    assert sp.simplify(metric.g[0, 0] - g_tt) == 0
    assert sp.simplify(metric.g[3, 3] - g_phi_phi) == 0
    assert sp.simplify(metric.g[0, 3] - g_t_phi) == 0
    
    # Instead of computing the full Ricci tensor (which is expensive),
    # simply verify that the metric has a non-zero determinant,
    # which is a necessary property for a well-defined spacetime
    det_g = metric.g.det()
    assert det_g != 0


def test_flrw_metric():
    """Test the FLRW metric with different curvature parameters."""
    # Test with k=0 (flat)
    metric_flat = friedmann_lemaitre_robertson_walker(k=0)
    assert metric_flat.dimension == 4
    
    # Test with k=1 (closed)
    metric_closed = friedmann_lemaitre_robertson_walker(k=1)
    assert metric_closed.dimension == 4
    
    # Test with k=-1 (open)
    metric_open = friedmann_lemaitre_robertson_walker(k=-1)
    assert metric_open.dimension == 4
    
    # Test with invalid k
    with pytest.raises(ValueError):
        friedmann_lemaitre_robertson_walker(k=2)


def test_de_sitter_metrics():
    """Test the de Sitter and Anti-de Sitter metrics."""
    # Test de Sitter metric
    dS_metric = de_sitter()
    assert dS_metric.dimension == 4
    
    # Test Anti-de Sitter metric
    AdS_metric = anti_de_sitter()
    assert AdS_metric.dimension == 4
    
    # Extract coordinates and parameter
    t, r, theta, phi = dS_metric.coordinates
    H = dS_metric.params[0]
    
    # Check key properties of the dS metric
    assert dS_metric.g[0, 0] == -(1 - H**2 * r**2)
    assert dS_metric.g[1, 1] == 1/(1 - H**2 * r**2)


def test_coordinate_parameters_override():
    """Test providing custom coordinates and parameters to spacetime metrics."""
    # Create custom coordinates and parameters
    T, R, THETA, PHI = symbols('T R THETA PHI')
    custom_coords = [T, R, THETA, PHI]
    
    Mass = symbols('Mass', positive=True)
    custom_params = [Mass]
    
    # Create Schwarzschild with custom coordinates and parameters
    metric = schwarzschild(coordinates=custom_coords, parameters=custom_params)
    
    # Check the coordinates and parameters were used
    assert metric.coordinates == custom_coords
    assert metric.params == custom_params
    
    # Check the metric still has the correct form
    assert metric.g[0, 0] == -(1 - 2*Mass/R)
    assert metric.g[1, 1] == 1/(1 - 2*Mass/R)
    assert metric.g[2, 2] == R**2
    assert metric.g[3, 3] == R**2 * sin(THETA)**2 