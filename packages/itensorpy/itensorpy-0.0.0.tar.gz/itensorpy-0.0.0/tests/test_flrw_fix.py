"""
Tests for diagnosing FLRW metric issues.
"""

import sympy as sp
from sympy import symbols, sin, exp, Function

from itensorpy.metric import Metric
from itensorpy.spacetimes import friedmann_lemaitre_robertson_walker
from itensorpy.einstein import EinsteinTensor


def test_flrw_einstein_simple():
    """A simplified test for Einstein tensor in FLRW spacetime."""
    # Create FLRW metric with flat spatial sections (k=0)
    t, r, theta, phi = symbols('t r theta phi')
    
    # Use a simple explicit scale factor instead of a symbolic function
    # a(t) = exp(H*t) where H is the Hubble parameter
    H = symbols('H', positive=True)
    a_explicit = exp(H*t)
    
    # Create the metric components directly - a diagonal matrix with:
    # g_00 = -1
    # g_11 = a(t)^2
    # g_22 = a(t)^2 * r^2
    # g_33 = a(t)^2 * r^2 * sin(theta)^2
    g_components = {
        (0, 0): -1,
        (1, 1): a_explicit**2,
        (2, 2): a_explicit**2 * r**2,
        (3, 3): a_explicit**2 * r**2 * sin(theta)**2,
    }
    
    # Create the metric using the explicit components
    metric = Metric(components=g_components, coordinates=[t, r, theta, phi], params=[H])
    
    # Compute the Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # For this specific scale factor a(t) = exp(H*t), we can compute:
    # a'(t) = H * exp(H*t) = H * a(t)
    # a''(t) = H^2 * exp(H*t) = H^2 * a(t)
    
    # Print the components to inspect
    print("G_00:", einstein.get_component_lower(0, 0))
    print("Expected G_00:", 3 * H**2)
    
    print("G_11:", einstein.get_component_lower(1, 1))
    print("Expected G_11:", -a_explicit**2 * 3 * H**2)
    
    # Test at specific numeric values
    H_val = 0.1
    t_val = 2.0
    r_val = 1.0
    theta_val = 1.0
    
    G_00 = einstein.get_component_lower(0, 0)
    expected_G00 = 3 * H**2
    
    # Substitute numeric values
    numeric_G00 = float(G_00.subs({H: H_val, t: t_val, r: r_val, theta: theta_val}))
    numeric_expected_G00 = float(expected_G00.subs(H, H_val))
    
    # Print numeric results
    print(f"Numeric G_00: {numeric_G00}")
    print(f"Expected numeric G_00: {numeric_expected_G00}")
    print(f"Is G_00 correct? {abs(numeric_G00 - numeric_expected_G00) < 1e-5}")


if __name__ == "__main__":
    test_flrw_einstein_simple() 