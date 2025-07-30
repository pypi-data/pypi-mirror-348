"""
Tests for the Riemann tensor module.
"""

from sympy import symbols, simplify, Matrix, zeros, sin, cos, pi
import sympy as sp
import pytest

from itensorpy.metric import Metric
from itensorpy.riemann import RiemannTensor
from itensorpy.christoffel import ChristoffelSymbols
from itensorpy.spacetimes import schwarzschild, minkowski

def test_flat_spacetime_riemann():
    """Test that Riemann tensor is zero for flat spacetime."""
    # Set up flat spacetime metric
    coordinates = [symbols('t'), symbols('x'), symbols('y'), symbols('z')]
    flat_spacetime = Metric(minkowski(coordinates=coordinates))
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(flat_spacetime)
    
    # Check that all components are zero
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    assert riemann.get_component_up(i, j, k, l) == 0
                    
    # Also check components_down are all zero
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    assert riemann.get_component_down(i, j, k, l) == 0

def test_sphere_riemann():
    """Test the Riemann tensor for a 2D sphere."""
    # Set up 2D sphere metric
    r, theta, phi = symbols('r theta phi')
    coordinates = [theta, phi]  # Angular coordinates on the sphere
    
    # Metric for a 2D sphere of radius r
    R = 1  # Radius of the sphere
    components = {
        (0, 0): R**2,
        (1, 1): R**2 * sin(theta)**2
    }
    sphere_metric = Metric(components=components, coordinates=coordinates)
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(sphere_metric)
    
    # For a sphere, R_1212 = g_11 * g_22 * sin^2(theta)
    expected = R**2 * sin(theta)**2
    actual = riemann.get_component_down(0, 1, 0, 1)
    
    assert simplify(actual - expected) == 0

def test_schwarzschild_riemann():
    """Test the Riemann tensor for Schwarzschild spacetime."""
    # Set up Schwarzschild metric
    t, r, theta, phi = symbols('t r theta phi')
    M = symbols('M', positive=True)
    
    schw_metric = Metric(schwarzschild(
        coordinates=[t, r, theta, phi],
        parameters=[M]
    ))
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(schw_metric)
    
    # Get components and check their general structure
    
    # Check that R_trtr is proportional to M/r^3
    R_trtr = riemann.get_component_down(0, 1, 0, 1)
    R_trtr_normalized = simplify(R_trtr * r**3)
    
    # Check that it depends on M
    assert M in R_trtr_normalized.free_symbols
    
    # Check that it doesn't depend on theta or phi
    assert theta not in R_trtr_normalized.free_symbols
    assert phi not in R_trtr_normalized.free_symbols
    
    # Check symmetry relations
    # R_trtr = -R_rttr
    assert simplify(R_trtr + riemann.get_component_down(1, 0, 0, 1)) == 0
    
    # Check that R_tθtθ is proportional to M*r
    R_tthth = riemann.get_component_down(0, 2, 0, 2)
    
    # Check it contains M and r
    assert M in R_tthth.free_symbols
    assert r in R_tthth.free_symbols
    
    # Check it doesn't depend on phi
    assert phi not in R_tthth.free_symbols

def test_riemann_identities():
    """Test that the Riemann tensor satisfies its basic symmetry identities."""
    # Set up a non-trivial spacetime
    t, r, theta, phi = symbols('t r theta phi')
    M = symbols('M', positive=True)
    
    schw_metric = Metric(schwarzschild(
        coordinates=[t, r, theta, phi],
        parameters=[M]
    ))
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(schw_metric)
    
    # Test antisymmetry in first pair of indices
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if a != b:  # Skip when a = b since it's trivially satisfied
                        # R_abcd = -R_bacd
                        assert simplify(
                            riemann.get_component_down(a, b, c, d) + 
                            riemann.get_component_down(b, a, c, d)
                        ) == 0
    
    # Test antisymmetry in second pair of indices
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if c != d:  # Skip when c = d since it's trivially satisfied
                        # R_abcd = -R_abdc
                        assert simplify(
                            riemann.get_component_down(a, b, c, d) + 
                            riemann.get_component_down(a, b, d, c)
                        ) == 0

def test_nonzero_components():
    """Test the get_nonzero_components_down method."""
    # Set up a simple metric
    t, r = symbols('t r')
    components = {
        (0, 0): -1,
        (1, 1): 1/(1-2/r)
    }
    metric = Metric(components=components, coordinates=[t, r])
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(metric)
    
    # Get non-zero components
    nonzero = riemann.get_nonzero_components_down()
    
    # Verify that non-zero components are correct
    for indices, value in nonzero.items():
        a, b, c, d = indices
        assert riemann.get_component_down(a, b, c, d) != 0
        assert simplify(riemann.get_component_down(a, b, c, d) - value) == 0 