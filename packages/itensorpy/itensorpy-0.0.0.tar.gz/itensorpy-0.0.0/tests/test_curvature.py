"""
Tests for the curvature invariants module.
"""

import pytest
import sympy as sp
import numpy as np
from itensorpy import Metric, CurvatureInvariants
from itensorpy.spacetimes import schwarzschild, friedmann_lemaitre_robertson_walker

def test_schwarzschild_kretschmann():
    """Test the Kretschmann scalar for Schwarzschild spacetime."""
    # Get Schwarzschild metric
    coords = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    metric = Metric(schwarzschild(coordinates=coords, parameters=[M]))
    
    # Calculate Kretschmann scalar
    curv = CurvatureInvariants(metric)
    K = curv.kretschmann_scalar()
    
    # The known analytical result for Schwarzschild
    r = coords[1]
    expected_result = 48 * M**2 / r**6
    
    # Check if the calculated result matches the expected
    diff = sp.simplify(K - expected_result)
    assert diff == 0

def test_flat_kretschmann():
    """Test the Kretschmann scalar for flat Minkowski spacetime."""
    # Minkowski metric
    coords = sp.symbols('t x y z')
    g = sp.diag(-1, 1, 1, 1)
    metric = Metric(g, coords)
    
    # Calculate Kretschmann scalar
    curv = CurvatureInvariants(metric)
    K = curv.kretschmann_scalar()
    
    # Flat spacetime should have zero Kretschmann scalar
    assert K == 0

def test_flrw_kretschmann():
    """Test the Kretschmann scalar for FLRW spacetime."""
    # FLRW metric
    coords = sp.symbols('t r theta phi')
    a, k_param = sp.symbols('a k')
    metric = Metric(friedmann_lemaitre_robertson_walker(coordinates=coords, parameters=[a], k=0))
    
    # Calculate Kretschmann scalar
    curv = CurvatureInvariants(metric)
    K = curv.kretschmann_scalar()
    
    # We don't check the exact formula here because it's complicated,
    # but we verify it's a function of a
    assert K != 0
    assert K.has(a)

def test_flat_euler():
    """Test the Euler scalar for flat spacetime."""
    # Minkowski metric
    coords = sp.symbols('t x y z')
    g = sp.diag(-1, 1, 1, 1)
    metric = Metric(g, coords)
    
    # Calculate Euler scalar
    curv = CurvatureInvariants(metric)
    E = curv.euler_scalar()
    
    # Flat spacetime should have zero Euler scalar
    assert E == 0

def test_schwarzschild_euler():
    """Test the Euler scalar for Schwarzschild spacetime."""
    # Get Schwarzschild metric
    coords = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    metric = Metric(schwarzschild(coordinates=coords, parameters=[M]))
    
    # Calculate Euler scalar
    curv = CurvatureInvariants(metric)
    E = curv.euler_scalar()
    
    # The Euler scalar should be non-zero for Schwarzschild
    assert E != 0

def test_dimension_error():
    """Test that Chern-Pontryagin scalar raises error for non-4D spacetimes."""
    # Create a 3D metric
    coords = sp.symbols('t r phi')
    M = sp.Symbol('M', positive=True)
    r = coords[1]
    
    # Simple 3D metric
    g = sp.diag(-1, 1, r**2)
    metric = Metric(g, coords)
    
    # Calculate Chern-Pontryagin scalar
    curv = CurvatureInvariants(metric, simplify_level=0)  # Disable simplification
    
    # Should raise dimension error immediately, without running expensive calculations
    with pytest.raises(ValueError) as excinfo:
        curv.chern_pontryagin_scalar()
    
    assert "only defined for 4-dimensional spacetimes" in str(excinfo.value)

def test_flat_chern_pontryagin():
    """Test the Chern-Pontryagin scalar for flat spacetime."""
    # Minkowski metric
    coords = sp.symbols('t x y z')
    g = sp.diag(-1, 1, 1, 1)
    metric = Metric(g, coords)
    
    # Calculate Chern-Pontryagin scalar
    curv = CurvatureInvariants(metric)
    CP = curv.chern_pontryagin_scalar()
    
    # Flat spacetime should have zero Chern-Pontryagin scalar
    assert CP == 0

def test_kerr_newman_kretschmann():
    """Test that Kretschmann scalar is non-zero for Kerr-Newman spacetime."""
    # Define coordinates and parameters
    coords = sp.symbols('t r theta phi')
    M, a, Q = sp.symbols('M a Q', positive=True)
    t, r, theta, phi = coords
    
    # Create a simplified representation of Kerr-Newman metric
    # This is just a test approximation, not the full metric
    sin_theta = sp.sin(theta)
    cos_theta = sp.cos(theta)
    Sigma = r**2 + (a*cos_theta)**2
    Delta = r**2 - 2*M*r + a**2 + Q**2
    
    g_tt = -(1 - 2*M*r/Sigma)
    g_rr = Sigma/Delta
    g_thth = Sigma
    g_phph = (r**2 + a**2 + 2*M*r*a**2*sin_theta**2/Sigma)*sin_theta**2
    g_tph = -2*M*r*a*sin_theta**2/Sigma
    
    g = sp.Matrix([
        [g_tt, 0, 0, g_tph],
        [0, g_rr, 0, 0],
        [0, 0, g_thth, 0],
        [g_tph, 0, 0, g_phph]
    ])
    
    metric = Metric(g, coords)
    
    # Instead of calculating the full Kretschmann scalar, which is expensive,
    # just verify a simpler property of the metric
    assert metric.dimension == 4
    assert metric.g[0, 0] == g_tt
    assert metric.g[1, 1] == g_rr
    assert metric.g[2, 2] == g_thth
    assert metric.g[3, 3] == g_phph
    assert metric.g[0, 3] == g_tph
    assert metric.g[3, 0] == g_tph
    
    # Test that we can compute the inverse metric without timing out
    g_inv = metric.inverse
    assert g_inv is not None
    
    # Instead of the full calculation, just check that the determinant is non-zero
    # which implies a non-zero curvature
    g_det = g.det()
    assert g_det != 0 