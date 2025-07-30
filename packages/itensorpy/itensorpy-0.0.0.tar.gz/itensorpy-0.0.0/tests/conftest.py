"""
Pytest configuration and fixtures for the iTensorPy test suite.
"""

import pytest
import sympy as sp
from sympy import symbols, diag, sin

@pytest.fixture
def basic_coordinates():
    """Return a set of standard 4D coordinates."""
    t, x, y, z = symbols('t x y z')
    return [t, x, y, z]

@pytest.fixture
def spherical_coordinates():
    """Return a set of spherical coordinates."""
    t, r, theta, phi = symbols('t r theta phi')
    return [t, r, theta, phi]

@pytest.fixture
def minkowski_components():
    """Return the components for a Minkowski metric."""
    return diag(-1, 1, 1, 1)

@pytest.fixture
def schwarzschild_components(spherical_coordinates):
    """Return the components for a Schwarzschild metric with M=1."""
    t, r, theta, phi = spherical_coordinates
    g_tt = -(1 - 2/r)
    g_rr = 1/(1 - 2/r)
    g_theta_theta = r**2
    g_phi_phi = r**2 * sin(theta)**2
    
    return {
        (0, 0): g_tt,
        (1, 1): g_rr,
        (2, 2): g_theta_theta,
        (3, 3): g_phi_phi
    } 