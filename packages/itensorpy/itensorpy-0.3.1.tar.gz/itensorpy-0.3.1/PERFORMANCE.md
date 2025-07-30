# iTensorPy Performance Guide

This guide documents the performance optimizations incorporated into the iTensorPy package for symbolic tensor calculations in general relativity.

## Performance Optimizations

### 1. Tiered Simplification

The package now supports different levels of simplification to help balance performance and readability:

- **Level 0**: No simplification (fastest)
- **Level 1**: Basic simplification (expand only)
- **Level 2**: Medium simplification (expand, trigsimp, cancel)
- **Level 3**: Full simplification (all operations, slowest but most thorough)

Example usage:
```python
from itensorpy import Metric, RiemannTensor, CurvatureInvariants
from itensorpy.spacetimes import schwarzschild

# Create metric with custom simplification level
metric = Metric(schwarzschild(), simplify_level=1)

# Create tensors with custom simplification levels
riemann = RiemannTensor.from_metric(metric, simplify_level=1)
curv = CurvatureInvariants(metric=metric, simplify_level=0)

# Get result with custom simplification
K = curv.kretschmann_scalar(simplify_level=2)
```

### 2. Caching with `functools.cached_property`

Expensive computations are now cached:

- `Metric.inverse`: Cached inverse metric tensor
- `Metric.determinant`: Cached determinant
- `RiemannTensor.components_down`: Cached lowered indices components
- `CurvatureInvariants`: Cached invariants (Kretschmann, Euler, Chern-Pontryagin)

This means repeated access to these properties will be virtually instantaneous.

### 3. Optimized Index Generation

Tensor index permutations are now cached with `functools.lru_cache`:

```python
@functools.lru_cache(maxsize=64)
def generate_index_riemann(n):
    # Implementation here
```

### 4. Special Case Optimizations

The package now has special optimizations for well-known metrics:

- For flat (Minkowski) spacetime, curvature invariants return `0` directly
- For Schwarzschild metrics, the Kretschmann scalar is computed as `48 * M**2 / r**6`
- For Kerr metrics, analytic formulas are used instead of full tensor contractions

### 5. Optimized Matrix Operations

- 2D metrics get special treatment for faster inverse computation
- Symbolic operations are sequenced for better performance

## Performance Benchmarks

The `examples/` directory contains several benchmarking scripts:

- `performance_test.py`: General performance tests with caching
- `kerr_performance.py`: Tests specific to Kerr metric optimizations
- `metric_size_test.py`: Performance tests for different metric dimensions

### Sample Results (simplified)

Tested on a typical laptop:

| Operation | Before | After | Speedup |
|-----------|--------|-------|---------|
| Cached Component Access | 250ms | <1ms | >250x |
| Schwarzschild Kretschmann | 650ms | 2ms | 325x |
| Kerr Riemann Tensor (level 1) | 3.5s | 0.8s | 4.4x |

## Best Practices

1. **Choose the right simplification level**:
   - During development or for chained calculations, use level 0 or 1
   - For final results or visualization, use level 2 or 3

2. **Use pre-calculated metrics**:
   - The `spacetimes` module contains optimized implementations of common metrics

3. **Reuse tensor objects**:
   - Create the tensors once and reuse them to take advantage of caching

4. **Limit component iteration**:
   - When computing contractions, use `get_nonzero_components_down()` to avoid iterating over zero components
   
5. **Consider exact arithmetic**:
   - Use symbolic parameters (like `Symbol('M')`) rather than floating-point when possible

## Future Optimizations

- Further parallelization of tensor contractions
- Just-in-time compilation for numerical evaluations
- More special case implementations for common metrics
- Improved memory management for very large tensor calculations 