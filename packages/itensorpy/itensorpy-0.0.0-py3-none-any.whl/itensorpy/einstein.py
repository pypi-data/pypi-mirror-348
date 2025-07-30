"""
Module for computing and manipulating the Einstein tensor.
"""

import sympy as sp
from sympy import Matrix, Symbol, Expr, Rational
from typing import List, Dict, Tuple, Union, Optional

from .metric import Metric
from .ricci import RicciTensor, RicciScalar
from .utils import custom_simplify, generate_index_ricci


class EinsteinTensor:
    """
    A class for computing and storing the Einstein tensor.

    The Einstein tensor is related to the energy - momentum distribution in spacetime
    and appears on the left side of Einstein's field equations.
    """

    def __init__(self,
                 components_lower=None,
                 components_upper=None,
                 ricci_tensor: Optional[RicciTensor] = None,
                 ricci_scalar: Optional[RicciScalar] = None,
                 metric: Optional[Metric] = None):
        """
        Initialize the Einstein tensor.

        Args:
            components_lower: Optional pre - computed Einstein tensor with lower indices
            components_upper: Optional pre - computed Einstein tensor with upper indices
            ricci_tensor: Ricci tensor used to compute the Einstein tensor
            ricci_scalar: Ricci scalar used to compute the Einstein tensor
            metric: Metric tensor, needed for computing and raising / lowering indices
        """
        self.components_lower = components_lower
        self.components_upper = components_upper
        self.ricci_tensor = ricci_tensor
        self.ricci_scalar = ricci_scalar
        self.metric = metric or (ricci_tensor.metric if ricci_tensor else None)

        # Compute Einstein tensor if necessary components are available
        if components_lower is None and ricci_tensor is not None and ricci_scalar is not None:
            self.components_lower = self._compute_einstein_tensor_lower()

        if components_upper is None and self.components_lower is not None and self.metric is not None:
            self.components_upper = self._compute_einstein_tensor_upper()

    @classmethod
    def from_ricci(cls, ricci_tensor: RicciTensor, ricci_scalar: RicciScalar) -> 'EinsteinTensor':
        """
        Create an Einstein tensor from Ricci tensor and scalar.

        Args:
            ricci_tensor: Ricci tensor instance
            ricci_scalar: Ricci scalar instance

        Returns:
            EinsteinTensor instance
        """
        # Ensure they share the same metric
        if ricci_tensor.metric != ricci_scalar.metric:
            raise ValueError("Ricci tensor and scalar must share the same metric")

        return cls(ricci_tensor=ricci_tensor, ricci_scalar=ricci_scalar, metric=ricci_tensor.metric)

    @classmethod
    def from_metric(cls, metric: Metric) -> 'EinsteinTensor':
        """
        Create an Einstein tensor directly from a metric tensor.

        Args:
            metric: Metric tensor instance

        Returns:
            EinsteinTensor instance
        """
        ricci_tensor = RicciTensor.from_metric(metric)
        ricci_scalar = RicciScalar.from_ricci(ricci_tensor)
        return cls.from_ricci(ricci_tensor, ricci_scalar)

    def _compute_einstein_tensor_lower(self) -> Matrix:
        """
        Compute the Einstein tensor with lower indices.

        Returns:
            SymPy Matrix representing the Einstein tensor with lower indices
        """
        if self.ricci_tensor is None or self.ricci_tensor.components is None:
            raise ValueError("Valid Ricci tensor required to compute the Einstein tensor")

        if self.ricci_scalar is None or self.ricci_scalar.value is None:
            raise ValueError("Valid Ricci scalar required to compute the Einstein tensor")

        if self.metric is None or self.metric.g is None:
            raise ValueError("Valid metric tensor required to compute the Einstein tensor")

        n = self.metric.dimension
        R = self.ricci_scalar.value
        Ricci = self.ricci_tensor.components
        g = self.metric.g

        # Create a matrix to store Einstein tensor components
        G_lower = sp.zeros(n, n)

        # G_μν = R_μν - (1 / 2)Rg_μν
        for mu in range(n):
            for nu in range(n):
                G_lower[mu, nu] = Ricci[mu, nu] - Rational(1, 2) * g[mu, nu] * R
                G_lower[mu, nu] = custom_simplify(G_lower[mu, nu])

        return G_lower

    def _compute_einstein_tensor_upper(self) -> Matrix:
        """
        Compute the Einstein tensor with upper indices.

        Returns:
            SymPy Matrix representing the Einstein tensor with upper indices
        """
        if self.components_lower is None:
            raise ValueError("Einstein tensor with lower indices required")

        if self.metric is None:
            raise ValueError("Metric tensor required to raise indices")

        n = self.metric.dimension
        g_inv = self.metric.inverse
        G_lower = self.components_lower

        # Create a matrix to store Einstein tensor components with upper indices
        G_upper = sp.zeros(n, n)

        # G^μν = g^μα g^νβ G_αβ
        for mu in range(n):
            for nu in range(n):
                sum_term = 0
                for alpha in range(n):
                    for beta in range(n):
                        sum_term += g_inv[mu, alpha] * g_inv[nu, beta] * G_lower[alpha, beta]
                G_upper[mu, nu] = custom_simplify(sum_term)

        return G_upper

    def get_component_lower(self, i: int, j: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the Einstein tensor with lower indices.

        Args:
            i: First index
            j: Second index
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for G_ij
        """
        if self.components_lower is None:
            raise ValueError("Einstein tensor with lower indices not computed")

        result = self.components_lower[i, j]
        if simplify:
            return custom_simplify(result)
        return result

    def get_component_upper(self, i: int, j: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the Einstein tensor with upper indices.

        Args:
            i: First index
            j: Second index
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for G^ij
        """
        if self.components_upper is None:
            raise ValueError("Einstein tensor with upper indices not computed")

        result = self.components_upper[i, j]
        if simplify:
            return custom_simplify(result)
        return result

    def get_nonzero_components_lower(self) -> Dict[Tuple[int, int], sp.Expr]:
        """
        Get all non - zero components of the Einstein tensor with lower indices.

        Returns:
            Dictionary mapping (i,j) indices to non - zero symbolic expressions
        """
        if self.components_lower is None:
            raise ValueError("Einstein tensor with lower indices not computed")

        n = self.metric.dimension
        result = {}

        for indices in generate_index_ricci(n):
            i, j = indices
            val = self.get_component_lower(i, j)
            if val != 0:
                result[indices] = val

        return result

    def get_nonzero_components_upper(self) -> Dict[Tuple[int, int], sp.Expr]:
        """
        Get all non - zero components of the Einstein tensor with upper indices.

        Returns:
            Dictionary mapping (i,j) indices to non - zero symbolic expressions
        """
        if self.components_upper is None:
            raise ValueError("Einstein tensor with upper indices not computed")

        n = self.metric.dimension
        result = {}

        for i in range(n):
            for j in range(n):
                val = self.get_component_upper(i, j)
                if val != 0:
                    result[(i, j)] = val

        return result

    def __str__(self) -> str:
        """
        String representation showing non - zero components of the Einstein tensor.

        Returns:
            String showing all non - zero Einstein tensor components
        """
        result = ""

        if self.components_upper is not None:
            result += "Non - zero Einstein tensor components (G^i_j):\n"
            for i in range(self.metric.dimension):
                for j in range(self.metric.dimension):
                    val = custom_simplify(self.components_upper[i, j])
                    if val != 0:
                        result += f"G^{{{i}}}_{{{j}}} = {val}\n"
            result += "\n"

        if self.components_lower is not None:
            result += "Non - zero Einstein tensor components (G_ij):\n"
            for i in range(self.metric.dimension):
                for j in range(i, self.metric.dimension):
                    val = custom_simplify(self.components_lower[i, j])
                    if val != 0:
                        result += f"G_{{{i}{j}}} = {val}\n"

        if not result:
            return "Einstein tensor not computed"

        return result
