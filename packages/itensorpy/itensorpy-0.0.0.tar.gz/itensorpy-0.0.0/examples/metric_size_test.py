"""
Performance test comparing metrics of different dimensions.

This script demonstrates the performance improvements for:
1. Metrics of different dimensions (2D, 3D, 4D)
2. Special optimizations for 2D inverse calculation
"""

import time
import sympy as sp
from itensorpy import Metric, ChristoffelSymbols, RiemannTensor

def create_test_metric(dimension):
    """Create a simple diagonal metric of the given dimension."""
    coords = [sp.Symbol(f'x{i}') for i in range(dimension)]
    components = {}
    
    # Create a simple diagonal metric with varying components
    for i in range(dimension):
        components[(i, i)] = sp.exp(coords[0]) if i == 0 else 1.0
    
    return Metric(components=components, coordinates=coords)

def test_metric_inverse_performance():
    """Test inverse computation performance for metrics of different dimensions."""
    print("\n=== Metric Inverse Performance Test ===")
    
    for dim in [2, 3, 4, 5]:
        print(f"\nTesting {dim}D metric:")
        
        # Create metric
        metric = create_test_metric(dim)
        
        # Time the inverse calculation
        start_time = time.time()
        _ = metric.inverse
        end_time = time.time()
        first_time = end_time - start_time
        print(f"  First inverse calculation: {first_time:.6f} seconds")
        
        # Time the cached access
        start_time = time.time()
        _ = metric.inverse
        end_time = time.time()
        cached_time = end_time - start_time
        print(f"  Cached access: {cached_time:.6f} seconds")
        
        # Calculate speedup ratio, handle division by zero
        if cached_time > 0:
            speedup = first_time / cached_time
            print(f"  Speedup from caching: {speedup:.1f}x")
        else:
            print("  Speedup from caching: ∞ (cached time too small to measure)")

def test_christoffel_performance():
    """Test Christoffel symbols computation for metrics of different dimensions."""
    print("\n=== Christoffel Symbols Performance Test ===")
    
    for dim in [2, 3, 4]:
        print(f"\nTesting {dim}D metric:")
        
        # Create metric
        metric = create_test_metric(dim)
        
        # Time Christoffel symbols calculation
        start_time = time.time()
        christoffel = ChristoffelSymbols.from_metric(metric)
        end_time = time.time()
        print(f"  Christoffel symbols calculation: {end_time - start_time:.4f} seconds")
        
        # Count non-zero Christoffel symbols
        non_zero = sum(1 for a in range(dim) for b in range(dim) for c in range(dim) 
                     if christoffel.components[a][b][c] != 0)
        print(f"  Number of non-zero components: {non_zero} out of {dim*dim*dim}")

def main():
    """Run all performance tests."""
    print("Metric Dimension Performance Tests")
    print("---------------------------------")
    
    test_metric_inverse_performance()
    test_christoffel_performance()

if __name__ == "__main__":
    main() 