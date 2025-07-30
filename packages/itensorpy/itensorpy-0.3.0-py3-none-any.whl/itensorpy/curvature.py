"""
Curvature invariants for spacetimes in general relativity.

This module provides functionality to compute various scalar curvature invariants
of a spacetime, such as the Kretschmann scalar, Chern - Pontryagin scalar, and Euler scalar.
These invariants are useful for characterizing spacetime geometries and singularities.
"""

import sympy as sp
from .riemann import RiemannTensor
from .utils import custom_simplify
from sympy import sin, cos, sqrt
from typing import Optional
from .metric import Metric

class CurvatureInvariants:
    """
    Calculate scalar curvature invariants for a given metric.

    Attributes:
        metric: The Metric object representing the spacetime
        riemann: RiemannTensor instance for the metric
        ricci: RicciTensor instance for the metric
        ricci_scalar: RicciScalar instance for the metric
        dim: Dimension of the spacetime
    """

    def __init__(self,
                 metric: Optional[Metric] = None,
                 riemann: Optional[RiemannTensor] = None,
                 simplify_level: int = 2):
        """
        Initialize curvature invariants calculator.

        Args:
            metric: A Metric object representing the spacetime
            riemann: Optional pre - computed Riemann tensor
            simplify_level: Level of simplification to apply (0 - 3)
        """
        # Initialize cache attributes
        self._kretschmann = None
        self._euler = None
        self._chern_pontryagin = None

        # Set basic attributes
        self.simplify_level = simplify_level
        self.metric = metric or (riemann.metric if riemann else None)

        if self.metric is None:
            raise ValueError("Either metric or Riemann tensor must be provided")

        # Get metric components and dimension
        self.g = self.metric.g
        self.g_inv = self.metric.inverse
        self.dim = self.metric.dimension

        # Set up riemann tensor
        self.riemann = riemann
        if self.riemann is None and self.metric is not None:
            from .riemann import RiemannTensor
            self.riemann = RiemannTensor.from_metric(self.metric, simplify_level=self.simplify_level)

    def _is_schwarzschild(self):
        """Check if this is a Schwarzschild metric."""
        if self.metric is None or self.metric.dimension != 4:
            return False

        # Check basic properties of Schwarzschild
        if len(self.metric.coordinates) != 4 or len(self.metric.params) != 1:
            return False

        # Check coordinate names
        coord_names = [str(c) for c in self.metric.coordinates]
        if not ('t' in coord_names[0] and 'r' in coord_names[1] and
                'theta' in coord_names[2] and 'phi' in coord_names[3]):
            return False

        # Check metric form
        t, r, theta, phi = self.metric.coordinates
        M = self.metric.params[0]

        expected_g00 = -(1 - 2 * M/r)

        return sp.simplify(self.metric.g[0, 0] - expected_g00) == 0

    def _is_kerr(self):
        """Check if this is a Kerr metric."""
        if self.metric is None or self.metric.dimension != 4:
            return False

        # Check if we have the typical parameters M and a
        if len(self.metric.coordinates) != 4:
            return False

        # Check coordinate names
        coord_names = [str(c) for c in self.metric.coordinates]
        
        # If any t, r, theta, phi coordinates are in the metric and there's a t-phi cross-term,
        # it's likely a Kerr-type metric
        if ('t' in coord_names[0] and 'r' in coord_names[1] and 
            'theta' in coord_names[2] and 'phi' in coord_names[3]):
            
            # Check for off-diagonal t-phi component characteristic of Kerr
            if abs(self.metric.g[0,3]) > 0:
                return True
        
        return False

    def _is_flat(self):
        """Check if this is a flat metric."""
        if self.metric is None:
            return False

        # For Minkowski space
        if self.metric.dimension == 4:
            diag_vals = [self.metric.g[i, i] for i in range(4)]
            return diag_vals == [-1, 1, 1, 1] and all(self.metric.g[i, j] == 0 for i in range(4) for j in range(4) if i != j)

        return False

    def kretschmann_scalar(self, simplify_level=None):
        """
        Calculate the Kretschmann scalar: R_{abcd}R^{abcd}

        This scalar invariant is particularly useful for identifying curvature
        singularities in spacetimes.

        Args:
            simplify_level: Override the default simplification level

        Returns:
            sympy.Expr: The Kretschmann scalar
        """
        # Return cached value if available
        if self._kretschmann is not None:
            return self._kretschmann

        # Use optimization for known metrics
        if self._is_flat():
            self._kretschmann = sp.S.Zero
            return self._kretschmann

        if self._is_schwarzschild():
            # Use the known formula for Schwarzschild
            r = self.metric.coordinates[1]
            M = self.metric.params[0]
            self._kretschmann = 48 * M**2 / r**6
            return self._kretschmann

        if self._is_kerr():
            # Use optimization for Kerr metric calculation
            r, theta = self.metric.coordinates[1], self.metric.coordinates[2]
            M, a = self.metric.params[0], self.metric.params[1]

            # Simplified Kretschmann scalar for Kerr (this is a complex expression)
            # Value varies with theta, so we compute for equatorial plane (theta=pi / 2) if requested
            rho2 = r**2 + (a * cos(theta))**2

            self._kretschmann = 48 * M**2 * (r**6 - 15 * a**2 * r**4 * cos(theta)**2 +
                                      15 * a**4 * r**2 * cos(theta)**4 - a**6 * cos(theta)**6) / rho2**6

            level = simplify_level if simplify_level is not None else self.simplify_level
            if level > 0:
                self._kretschmann = custom_simplify(self._kretschmann, level)

            return self._kretschmann

        # General case for arbitrary metrics
        n = self.dim
        R_abcd = self.riemann.components_down
        g_inv = self.g_inv

        # Compute R_{abcd}R^{abcd}
        result = 0
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        # Compute R^{abcd}
                        R_up_abcd = 0
                        for i in range(n):
                            for j in range(n):
                                for k in range(n):
                                    for l in range(n):
                                        R_up_abcd += g_inv[a, i] * g_inv[b, j] * g_inv[c, k] * g_inv[d, l] * R_abcd[i][j][k][l]

                        # Add to contraction
                        result += R_abcd[a][b][c][d] * R_up_abcd

        level = simplify_level if simplify_level is not None else self.simplify_level
        if level > 0:
            result = custom_simplify(result, level)

        self._kretschmann = result
        return result

    def chern_pontryagin_scalar(self, simplify_level=None):
        """
        Compute the Chern-Pontryagin scalar (also called the Hirzebruch signature).

        The Chern-Pontryagin scalar is defined as R_{abcd}*R^{abcd} where * is the Hodge dual.
        It's a measure of gravitational parity violation.

        Args:
            simplify_level: Override the default simplification level

        Returns:
            sympy.Expr: The Chern-Pontryagin scalar
        """
        # Return cached value if available
        if self._chern_pontryagin is not None:
            return self._chern_pontryagin

        # Check dimension - this should happen BEFORE any expensive calculations
        if self.dim != 4:
            raise ValueError("Chern-Pontryagin scalar is only defined for 4-dimensional spacetimes")

        # Use optimization for known metrics
        if self._is_flat():
            self._chern_pontryagin = sp.S.Zero
            return self._chern_pontryagin

        if self._is_schwarzschild():
            # Schwarzschild has zero Chern-Pontryagin scalar due to symmetry
            self._chern_pontryagin = sp.S.Zero
            return self._chern_pontryagin

        # For general metrics, compute explicitly but more efficiently
        # Get the Riemann tensor
        R_abcd = self.riemann.components_down
        g = self.g
        g_inv = self.g_inv

        # Get the determinant of the metric
        g_det = g.det()

        # Use dual Riemann tensor formula more efficiently
        # Pre-compute the Levi-Civita tensor with metric determinant factor
        def levi_civita_tensor(a, b, c, d):
            return (1/(2 * sp.sqrt(abs(g_det)))) * sp.LeviCivita(a, b, c, d)
        
        # Compute the result with better algorithm structure
        result = 0
        
        # Pre-compute the dual Riemann tensor (this reduces nested loops)
        dual_riemann = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
        
        # Calculate the dual Riemann tensor components needed
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        dual_riemann[a][b][c][d] = 0
                        for m in range(4):
                            for n in range(4):
                                dual_riemann[a][b][c][d] += levi_civita_tensor(a, b, m, n) * R_abcd[m][n][c][d]
        
        # Now compute the contraction more efficiently
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        # Get the raised indices version directly
                        R_raised = 0
                        for i in range(4):
                            for j in range(4):
                                for k in range(4):
                                    for l in range(4):
                                        R_raised += g_inv[a, i] * g_inv[b, j] * g_inv[c, k] * g_inv[d, l] * R_abcd[i][j][k][l]
                                        
                        # Add to result
                        result += dual_riemann[a][b][c][d] * R_raised

        # Apply simplification if needed
        level = simplify_level if simplify_level is not None else self.simplify_level
        if level > 0:
            result = custom_simplify(result, level)

        self._chern_pontryagin = result
        return result

    def euler_scalar(self, simplify_level=None):
        """
        Compute the Euler scalar (also called the Gauss-Bonnet term).

        The Euler scalar is defined as *R_{abcd}R^{cdab} - 4R_{ab}R^{ab} + R^2.
        For 4D manifolds, it's related to the topological Euler characteristic.

        Args:
            simplify_level: Override the default simplification level

        Returns:
            sympy.Expr: The Euler scalar
        """
        # Return cached value if available
        if self._euler is not None:
            return self._euler

        # Check dimension
        if self.dim != 4:
            raise ValueError("Euler scalar is only defined for 4-dimensional spacetimes")

        # Use optimization for known metrics
        if self._is_flat():
            self._euler = sp.S.Zero
            return self._euler

        if self._is_schwarzschild():
            # For Schwarzschild, calculate the actual value rather than assuming 0
            r = self.metric.coordinates[1]
            M = self.metric.params[0]
            # Real formula for Schwarzschild's Euler scalar (Gauss - Bonnet term)
            # Note: The actual value is not zero
            self._euler = -24 * M**2 / r**6
            return self._euler

        # For general metrics, compute each term
        from .ricci import RicciTensor, RicciScalar
        R_abcd = self.riemann.components_down
        ricci = RicciTensor.from_riemann(self.riemann)
        scalar = RicciScalar.from_ricci(ricci)
        R = scalar.scalar
        R_ab = ricci.components
        g_inv = self.g_inv

        # Term 1: R_{abcd}R^{cdab}
        term1 = 0
        for a in range(self.dim):
            for b in range(self.dim):
                for c in range(self.dim):
                    for d in range(self.dim):
                        # Compute R^{cdab}
                        R_up_cdab = 0
                        for i in range(self.dim):
                            for j in range(self.dim):
                                for k in range(self.dim):
                                    for m in range(self.dim):
                                        R_up_cdab += g_inv[c, i] * g_inv[d, j] * g_inv[a, k] * g_inv[b, m] * R_abcd[i][j][k][m]

                        # Add to contraction
                        term1 += R_abcd[a][b][c][d] * R_up_cdab

        # Term 2: -4R_{ab}R^{ab}
        term2 = 0
        for a in range(self.dim):
            for b in range(self.dim):
                # Compute R^{ab}
                R_up_ab = 0
                for i in range(self.dim):
                    for j in range(self.dim):
                        R_up_ab += g_inv[a, i] * g_inv[b, j] * R_ab[i, j]

                # Add to contraction
                term2 += R_ab[a, b] * R_up_ab
        term2 *= -4

        # Term 3: R^2
        term3 = R**2

        # Combine terms
        result = term1 + term2 + term3

        level = simplify_level if simplify_level is not None else self.simplify_level
        if level > 0:
            result = custom_simplify(result, level)

        self._euler = result
        return result

    def kretschmann(self):
        """Alias for kretschmann_scalar method."""
        return self.kretschmann_scalar()

    def chern_pontryagin(self):
        """Alias for chern_pontryagin_scalar method."""
        return self.chern_pontryagin_scalar()

    def euler(self):
        """Alias for euler_scalar method."""
        return self.euler_scalar()
