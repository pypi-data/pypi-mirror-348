"""
Module for computing and manipulating the Riemann curvature tensor.
"""

import sympy as sp
from sympy import diff, Matrix, Symbol
import functools
from typing import List, Dict, Tuple, Union, Optional

from .metric import Metric
from .christoffel import ChristoffelSymbols
from .utils import custom_simplify, generate_index_riemann, lower_indices


class RiemannTensor:
    """
    A class for computing and storing the Riemann curvature tensor.

    The Riemann tensor describes the curvature of spacetime and measures how
    parallel transport around an infinitesimal loop changes a vector.
    """

    def __init__(self,
                 components_up=None,
                 components_down=None,
                 christoffel: Optional[ChristoffelSymbols] = None,
                 metric: Optional[Metric] = None,
                 simplify_level: int = 2):
        """
        Initialize the Riemann tensor.

        Args:
            components_up: Optional pre - computed Riemann tensor with first index up
            components_down: Optional pre - computed Riemann tensor with all indices down
            christoffel: Christoffel symbols used to compute the Riemann tensor
            metric: Metric tensor used to lower indices
            simplify_level: Level of simplification to apply (0 - 3)
        """
        self.components_up = components_up
        self._components_down = components_down
        self.christoffel = christoffel
        self.metric = metric or (christoffel.metric if christoffel else None)
        self.simplify_level = simplify_level

        if self.components_up is None and christoffel is not None:
            self.components_up = self._compute_riemann_tensor()

        # No longer directly compute components_down in __init__
        # It will be computed on - demand via the cached_property

    @classmethod
    def from_christoffel(cls, christoffel: ChristoffelSymbols, simplify_level: int = 2) -> 'RiemannTensor':
        """
        Create a Riemann tensor from Christoffel symbols.

        Args:
            christoffel: Christoffel symbols instance
            simplify_level: Level of simplification to apply (0 - 3)

        Returns:
            RiemannTensor instance
        """
        return cls(christoffel=christoffel, simplify_level=simplify_level)

    @classmethod
    def from_metric(cls, metric: Metric, simplify_level: int = 2) -> 'RiemannTensor':
        """
        Create a Riemann tensor directly from a metric tensor.

        Args:
            metric: Metric tensor instance
            simplify_level: Level of simplification to apply (0 - 3)

        Returns:
            RiemannTensor instance
        """
        christoffel = ChristoffelSymbols.from_metric(metric)
        return cls.from_christoffel(christoffel, simplify_level=simplify_level)

    def _compute_riemann_tensor(self) -> List[List[List[List[sp.Expr]]]]:
        """
        Compute the Riemann curvature tensor from Christoffel symbols.

        Returns:
            A 4D array representing the Riemann tensor with first index contravariant
        """
        if self.christoffel is None or self.christoffel.components is None:
            raise ValueError("Valid Christoffel symbols required to compute the Riemann tensor")

        if self.metric is None:
            raise ValueError("Valid metric tensor required to compute the Riemann tensor")

        n = self.metric.dimension
        Gamma = self.christoffel.components
        coordinates = self.metric.coordinates

        Riemann = [[[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]

        for rho in range(n):
            for sigma in range(n):
                for mu in range(n):
                    for nu in range(n):
                        # Partial derivative terms
                        term1 = diff(Gamma[rho][nu][sigma], coordinates[mu])
                        term2 = diff(Gamma[rho][mu][sigma], coordinates[nu])

                        # Christoffel product terms
                        sum_term = 0
                        for lam in range(n):
                            sum_term += (Gamma[rho][mu][lam] * Gamma[lam][nu][sigma] -
                                        Gamma[rho][nu][lam] * Gamma[lam][mu][sigma])

                        Riemann[rho][sigma][mu][nu] = custom_simplify(term1 - term2 + sum_term, self.simplify_level)

        return Riemann

    @functools.cached_property
    def components_down(self) -> List[List[List[List[sp.Expr]]]]:
        """
        Get the Riemann tensor with all indices lowered.

        Returns:
            A 4D array representing the Riemann tensor with all indices covariant
        """
        if self._components_down is not None:
            return self._components_down

        if self.components_up is None:
            raise ValueError("Riemann tensor components with first index up not computed")

        if self.metric is None:
            raise ValueError("Valid metric tensor required to lower indices")

        self._components_down = lower_indices(self.components_up, self.metric.g, self.metric.dimension)
        return self._components_down

    def get_component_up(self, a: int, b: int, c: int, d: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the Riemann tensor with first index up.

        Args:
            a: First index (contravariant)
            b, c, d: Remaining indices (covariant)
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for R^a_bcd
        """
        if self.components_up is None:
            raise ValueError("Riemann tensor components with first index up not computed")

        result = self.components_up[a][b][c][d]
        if simplify:
            return custom_simplify(result, self.simplify_level)
        return result

    def get_component_down(self, a: int, b: int, c: int, d: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the Riemann tensor with all indices down.

        Args:
            a, b, c, d: Indices (all covariant)
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for R_abcd
        """
        result = self.components_down[a][b][c][d]
        if simplify:
            return custom_simplify(result, self.simplify_level)
        return result

    @functools.lru_cache(maxsize=16)
    def get_nonzero_components_down(self) -> Dict[Tuple[int, int, int, int], sp.Expr]:
        """
        Get all non - zero components of the Riemann tensor with all indices down.

        Returns:
            Dictionary mapping (a,b,c,d) indices to non - zero symbolic expressions
        """
        if self.metric is None:
            raise ValueError("Valid metric tensor required to get nonzero components")
            
        n = self.metric.dimension
        result = {}

        for indices in generate_index_riemann(n):
            a, b, c, d = indices
            val = self.get_component_down(a, b, c, d)
            if val != 0:
                result[indices] = val

        return result

    def __str__(self) -> str:
        """
        String representation showing non - zero components of the Riemann tensor.

        Returns:
            String showing all non - zero Riemann tensor components with all indices down
        """
        n = self.metric.dimension
        result = "Non - zero components of Riemann tensor (R_abcd):\n"

        for indices in generate_index_riemann(n):
            a, b, c, d = indices
            val = custom_simplify(self.components_down[a][b][c][d], self.simplify_level)
            if val != 0:
                result += f"R_{{{a}{b}{c}{d}}} = {val}\n"

        return result
