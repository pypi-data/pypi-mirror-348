"""
Examples demonstrating the calculation of curvature invariants.

This script shows how to compute and analyze various curvature scalars for different
spacetimes using the iTensorPy package.
"""

import sympy as sp
from itensorpy import Metric, CurvatureInvariants
from itensorpy.spacetimes import (
    schwarzschild, 
    friedmann_lemaitre_robertson_walker, 
    kerr, 
    reissner_nordstrom
)

def print_divider():
    """Print a divider line for cleaner output."""
    print("\n" + "="*60 + "\n")

def analyze_schwarzschild():
    """Calculate curvature invariants for Schwarzschild spacetime."""
    print("Analyzing Schwarzschild spacetime:")
    
    # Define coordinates and parameters
    coords = sp.symbols('t r theta phi')
    M = sp.Symbol('M', positive=True)
    r = coords[1]
    
    # Create metric
    metric = Metric(schwarzschild(coordinates=coords, parameters=[M]))
    print(f"Coordinates: {coords}")
    print(f"Parameters: M = mass")
    
    # Calculate invariants
    curv = CurvatureInvariants(metric)
    
    # Kretschmann scalar
    K = curv.kretschmann_scalar()
    print("\nKretschmann scalar:")
    print(f"K = {sp.simplify(K)}")
    
    # Euler scalar
    E = curv.euler_scalar()
    print("\nEuler scalar:")
    print(f"E = {sp.simplify(E)}")
    
    # Chern-Pontryagin scalar
    CP = curv.chern_pontryagin_scalar()
    print("\nChern-Pontryagin scalar:")
    print(f"CP = {sp.simplify(CP)}")
    
    # Analysis of singularities
    print("\nAnalysis:")
    print(f"The Kretschmann scalar K = {sp.simplify(K)} diverges at r = 0,")
    print("confirming a curvature singularity at the center of the black hole.")
    print(f"The Chern-Pontryagin scalar is {CP}, indicating the spacetime is not chiral.")

def analyze_flrw():
    """Calculate curvature invariants for FLRW spacetime."""
    print("Analyzing FLRW (cosmological) spacetime:")
    
    # Define coordinates and parameters
    coords = sp.symbols('t r theta phi')
    a, k = sp.symbols('a k')
    t = coords[0]
    
    # Create the metric - note: 'a' can be a function of time a(t)
    a_func = sp.Function('a')(t)
    metric = Metric(friedmann_lemaitre_robertson_walker(coordinates=coords, parameters=[a_func], k=0))
    print(f"Coordinates: {coords}")
    print(f"Parameters: a(t) = scale factor, k = curvature parameter")
    
    # Calculate Kretschmann scalar
    curv = CurvatureInvariants(metric)
    K = curv.kretschmann_scalar()
    print("\nKretschmann scalar:")
    print(f"K = {K}")
    
    # For a simpler expression, we can substitute a constant a
    K_const = K.subs(a_func, a)
    K_const = K_const.subs(sp.Derivative(a_func, t), 0)
    K_const = K_const.subs(sp.Derivative(a_func, t, t), 0)
    print("\nKretschmann scalar with constant a:")
    print(f"K = {sp.simplify(K_const)}")
    
    # Analysis
    print("\nAnalysis:")
    print("The Kretschmann scalar depends on the scale factor a(t) and its derivatives,")
    print("reflecting the dynamic nature of the expanding universe.")
    print("For a constant scale factor, it depends only on k, the spatial curvature parameter.")

def analyze_kerr():
    """Calculate the Kretschmann scalar for Kerr spacetime."""
    print("Analyzing Kerr spacetime:")
    
    # Define coordinates and parameters
    coords = sp.symbols('t r theta phi')
    M, a = sp.symbols('M a', positive=True)
    r = coords[1]
    
    # Create the metric
    metric = Metric(kerr(coordinates=coords, parameters=[M, a]))
    print(f"Coordinates: {coords}")
    print(f"Parameters: M = mass, a = angular momentum per unit mass")
    
    # Calculate Kretschmann scalar
    curv = CurvatureInvariants(metric)
    
    # The full expression is quite complicated, so we'll evaluate it
    # at the equatorial plane (theta = pi/2) for simplicity
    theta = coords[2]
    K = curv.kretschmann_scalar()
    K_eq = K.subs(theta, sp.pi/2)
    
    print("\nKretschmann scalar (simplified at equatorial plane):")
    print(f"K = {sp.simplify(K_eq)}")
    
    # Analysis
    print("\nAnalysis:")
    print("The Kretschmann scalar for Kerr spacetime is more complicated than for Schwarzschild")
    print("due to the rotational effects. It still diverges at r = 0,")
    print("but the singularity structure is different (ring-like rather than point-like).")

def analyze_reissner_nordstrom():
    """Calculate curvature invariants for Reissner-Nordström spacetime."""
    print("Analyzing Reissner-Nordström spacetime:")
    
    # Define coordinates and parameters
    coords = sp.symbols('t r theta phi')
    M, Q = sp.symbols('M Q', positive=True)
    r = coords[1]
    
    # Create the metric
    metric = Metric(reissner_nordstrom(coordinates=coords, parameters=[M, Q]))
    print(f"Coordinates: {coords}")
    print(f"Parameters: M = mass, Q = charge")
    
    # Calculate invariants
    curv = CurvatureInvariants(metric)
    K = curv.kretschmann_scalar()
    
    print("\nKretschmann scalar:")
    print(f"K = {sp.simplify(K)}")
    
    # Analysis
    print("\nAnalysis:")
    print("The Reissner-Nordström Kretschmann scalar depends on both mass M and charge Q.")
    print("The presence of charge modifies the singularity structure compared to Schwarzschild.")
    print("As r approaches 0, the scalar diverges, confirming the central singularity.")

def main():
    """Run all example analyses."""
    analyze_schwarzschild()
    print_divider()
    analyze_flrw()
    print_divider()
    analyze_kerr()
    print_divider()
    analyze_reissner_nordstrom()

if __name__ == "__main__":
    main() 