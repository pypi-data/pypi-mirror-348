"""
Test file to isolate the slow-running test_dimension_error function.
"""

import pytest
import time
import sympy as sp
from itensorpy import Metric, CurvatureInvariants

def test_dimension_error_isolated():
    """Test that Chern-Pontryagin scalar raises error for non-4D spacetimes."""
    # Create a 3D metric
    coords = sp.symbols('t r phi')
    M = sp.Symbol('M', positive=True)
    r = coords[1]
    
    # Simple 3D metric
    g = sp.diag(-1, 1, r**2)
    metric = Metric(g, coords)
    
    # Calculate Chern-Pontryagin scalar
    curv = CurvatureInvariants(metric)
    
    # Should raise dimension error
    with pytest.raises(ValueError) as excinfo:
        curv.chern_pontryagin_scalar()
    
    assert "only defined for 4-dimensional spacetimes" in str(excinfo.value) 