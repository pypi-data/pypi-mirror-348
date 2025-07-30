"""
Performance test for iTensorPy with the new optimizations.

This script compares the performance of various metrics with different
simplification levels and demonstrates the caching improvements.
"""

import time
import sympy as sp
from itensorpy import Metric, ChristoffelSymbols, RiemannTensor, CurvatureInvariants
from itensorpy.spacetimes import schwarzschild, kerr, minkowski

def measure_time(func, *args, **kwargs):
    """Measure the execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def test_schwarzschild_performance():
    """Test the performance of Schwarzschild metric calculations."""
    print("\n=== Schwarzschild Performance Test ===")
    
    # Create Schwarzschild metric
    t, r, theta, phi = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    metric = Metric(schwarzschild(coordinates=[t, r, theta, phi], parameters=[M]))
    
    # Test with different simplification levels
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
        
        # Kretschmann scalar (first time - computation)
        start_time = time.time()
        curv = CurvatureInvariants(metric=metric, simplify_level=level)
        K = curv.kretschmann_scalar()
        end_time = time.time()
        print(f"  Kretschmann scalar (first call): {end_time - start_time:.4f} seconds")
        
        # Kretschmann scalar (second time - cached)
        start_time = time.time()
        K2 = curv.kretschmann_scalar()
        end_time = time.time()
        print(f"  Kretschmann scalar (cached): {end_time - start_time:.4f} seconds")
        
        # Verify we get the expected formula for Schwarzschild
        expected = 48 * M**2 / r**6
        is_same = sp.simplify(K - expected) == 0
        print(f"  Result is correctly optimized: {is_same}")

def test_kerr_components_down_caching():
    """Test the cached_property for Riemann components_down."""
    print("\n=== Riemann Caching Performance Test ===")
    
    # Create a simple metric
    t, r, theta, phi = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    metric = Metric(minkowski(coordinates=[t, r, theta, phi]))
    
    # Create Riemann tensor
    christoffel = ChristoffelSymbols.from_metric(metric)
    riemann = RiemannTensor.from_christoffel(christoffel)
    
    # First access to components_down (should compute)
    start_time = time.time()
    _ = riemann.components_down
    end_time = time.time()
    print(f"First access to components_down: {end_time - start_time:.4f} seconds")
    
    # Second access (should use cache)
    start_time = time.time()
    _ = riemann.components_down
    end_time = time.time()
    print(f"Second access to components_down (cached): {end_time - start_time:.4f} seconds")
    
    # Access to component (should use cached components_down)
    start_time = time.time()
    _ = riemann.get_component_down(0, 1, 2, 3)
    end_time = time.time()
    print(f"Component access (uses cache): {end_time - start_time:.4f} seconds")

def main():
    """Run all performance tests."""
    print("iTensorPy Performance Test")
    print("--------------------------")
    
    test_schwarzschild_performance()
    test_kerr_components_down_caching()
    
    print("\nPerformance testing complete.")

if __name__ == "__main__":
    main() 