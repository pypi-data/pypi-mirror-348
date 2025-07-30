"""
Performance test for Kerr metric calculations with different optimization levels.

This script demonstrates the performance improvements from:
1. Caching with functools.cached_property
2. Different simplification levels
3. Special case optimizations for known metrics
"""

import time
import sympy as sp
from itensorpy import Metric, ChristoffelSymbols, RiemannTensor, CurvatureInvariants
from itensorpy.spacetimes import kerr

def test_kerr_performance():
    """Test the performance of Kerr metric calculations with optimizations."""
    print("\n=== Kerr Metric Performance Test ===")
    
    # Create Kerr metric
    t, r, theta, phi = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    a = sp.Symbol('a', positive=True)
    
    print("Generating Kerr metric...")
    start_time = time.time()
    metric = Metric(kerr(coordinates=[t, r, theta, phi], parameters=[M, a]))
    end_time = time.time()
    print(f"Metric generation: {end_time - start_time:.4f} seconds")
    
    # Test with and without optimization for Kretschmann scalar
    print("\nTesting Kretschmann scalar calculation:")
    
    # First with special case optimization (should be fast)
    print("\n1. With Kerr-specific optimization:")
    start_time = time.time()
    curv = CurvatureInvariants(metric=metric, simplify_level=1)
    K = curv.kretschmann_scalar()
    end_time = time.time()
    print(f"  Calculation time: {end_time - start_time:.4f} seconds")
    
    # Now accessing the cached result
    start_time = time.time()
    K2 = curv.kretschmann_scalar()
    end_time = time.time()
    print(f"  Cached access: {end_time - start_time:.4f} seconds")
    
    # Create a dummy version of the optimization check to always return False
    real_is_kerr = CurvatureInvariants._is_kerr
    CurvatureInvariants._is_kerr = lambda self: False
    
    print("\n2. Without Kerr-specific optimization (general calculation):")
    start_time = time.time()
    curv_general = CurvatureInvariants(metric=metric, simplify_level=1)
    K_general = curv_general.kretschmann_scalar()
    end_time = time.time()
    print(f"  Calculation time: {end_time - start_time:.4f} seconds")
    
    # Restore the real optimization check
    CurvatureInvariants._is_kerr = real_is_kerr
    
    # Check if results are the same
    print("\nVerifying results:")
    try:
        diff = sp.simplify(K - K_general)
        is_same = diff == 0
        print(f"  Results match: {is_same}")
        if not is_same:
            print(f"  Difference: {diff}")
    except Exception as e:
        print(f"  Error comparing results: {e}")

def test_simplification_levels():
    """Test different simplification levels on Kerr metric computations."""
    print("\n=== Simplification Level Comparison for Kerr Metric ===")
    
    # Create Kerr metric
    t, r, theta, phi = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True) 
    a = sp.Symbol('a', positive=True)
    metric = Metric(kerr(coordinates=[t, r, theta, phi], parameters=[M, a]))
    
    for level in [0, 1, 2, 3]:
        print(f"\nSimplification Level {level}:")
        
        # Christoffel symbols
        start_time = time.time()
        christoffel = ChristoffelSymbols.from_metric(metric)
        end_time = time.time()
        print(f"  Christoffel symbols: {end_time - start_time:.4f} seconds")
        
        # Riemann tensor
        start_time = time.time()
        riemann = RiemannTensor.from_christoffel(christoffel, simplify_level=level)
        end_time = time.time()
        print(f"  Riemann tensor: {end_time - start_time:.4f} seconds")
        
        # Count non-zero components in the Riemann tensor
        nonzero = riemann.get_nonzero_components_down()
        print(f"  Non-zero Riemann components: {len(nonzero)}")

def main():
    """Run Kerr metric performance tests."""
    print("Kerr Metric Performance Tests")
    print("-----------------------------")
    
    test_kerr_performance()
    test_simplification_levels()

if __name__ == "__main__":
    main() 