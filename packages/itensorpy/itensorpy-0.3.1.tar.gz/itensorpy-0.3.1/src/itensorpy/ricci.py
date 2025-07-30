"""
Module for computing and manipulating Ricci tensor and scalar curvature.
"""

import sympy as sp
from sympy import Matrix, Symbol, Expr
from typing import List, Dict, Tuple, Union, Optional

from .metric import Metric
from .riemann import RiemannTensor
from .utils import custom_simplify, generate_index_ricci


class RicciTensor:
    """
    A class for computing and storing the Ricci tensor.

    The Ricci tensor is a contraction of the Riemann tensor and describes
    the volume deformation of a small region of spacetime.
    """

    def __init__(self,
                 components=None,
                 riemann: Optional[RiemannTensor] = None,
                 metric: Optional[Metric] = None):
        """
        Initialize the Ricci tensor.

        Args:
            components: Optional pre - computed Ricci tensor components
            riemann: Riemann tensor used to compute the Ricci tensor
            metric: Metric tensor, needed if computing from Riemann tensor
        """
        self.components = components
        self.riemann = riemann
        self.metric = metric or (riemann.metric if riemann else None)

        if components is None and riemann is not None:
            self.components = self._compute_ricci_tensor()

    @classmethod
    def from_riemann(cls, riemann: RiemannTensor) -> 'RicciTensor':
        """
        Create a Ricci tensor from a Riemann tensor.

        Args:
            riemann: Riemann tensor instance

        Returns:
            RicciTensor instance
        """
        return cls(riemann=riemann)

    @classmethod
    def from_metric(cls, metric: Metric) -> 'RicciTensor':
        """
        Create a Ricci tensor directly from a metric tensor.

        Args:
            metric: Metric tensor instance

        Returns:
            RicciTensor instance
        """
        riemann = RiemannTensor.from_metric(metric)
        return cls.from_riemann(riemann)

    def _compute_ricci_tensor(self) -> Matrix:
        """
        Compute the Ricci tensor from the Riemann tensor.

        Returns:
            SymPy Matrix representing the Ricci tensor
        """
        if self.riemann is None or self.riemann.components_up is None:
            raise ValueError("Valid Riemann tensor required to compute the Ricci tensor")

        if self.metric is None:
            raise ValueError("Valid metric tensor required to compute the Ricci tensor")

        n = self.metric.dimension
        Riemann = self.riemann.components_up

        # Create a matrix to store Ricci tensor components
        Ricci = sp.zeros(n, n)

        # Compute Ricci tensor by contracting Riemann tensor
        for mu in range(n):
            for nu in range(n):
                Ricci[mu, nu] = sum(Riemann[rho][mu][rho][nu] for rho in range(n))
                Ricci[mu, nu] = custom_simplify(Ricci[mu, nu])

        return Ricci

    def get_component(self, i: int, j: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the Ricci tensor.

        Args:
            i: First index
            j: Second index
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for R_ij
        """
        if self.components is None:
            raise ValueError("Ricci tensor not computed")

        result = self.components[i, j]
        if simplify:
            return custom_simplify(result)
        return result

    def get_nonzero_components(self) -> Dict[Tuple[int, int], sp.Expr]:
        """
        Get all non - zero components of the Ricci tensor.

        Returns:
            Dictionary mapping (i,j) indices to non - zero symbolic expressions
        """
        if self.components is None:
            raise ValueError("Ricci tensor not computed")

        n = self.metric.dimension
        result = {}

        for indices in generate_index_ricci(n):
            i, j = indices
            val = self.get_component(i, j)
            if val != 0:
                result[indices] = val

        return result

    def __str__(self) -> str:
        """
        String representation showing non - zero components of the Ricci tensor.

        Returns:
            String showing all non - zero Ricci tensor components
        """
        if self.components is None:
            return "Ricci tensor not computed"

        n = self.metric.dimension
        result = "Non - zero components of Ricci tensor (R_ij):\n"

        for indices in generate_index_ricci(n):
            i, j = indices
            val = custom_simplify(self.components[i, j])
            if val != 0:
                result += f"R_{{{i}{j}}} = {val}\n"

        return result


class RicciScalar:
    """
    A class for computing and storing the Ricci scalar (scalar curvature).

    The Ricci scalar is a contraction of the Ricci tensor and provides a single
    measure of curvature at each point in spacetime.
    """

    def __init__(self,
                 value=None,
                 ricci: Optional[RicciTensor] = None,
                 metric: Optional[Metric] = None):
        """
        Initialize the Ricci scalar.

        Args:
            value: Optional pre - computed Ricci scalar value
            ricci: Ricci tensor used to compute the Ricci scalar
            metric: Metric tensor, needed if computing from Ricci tensor
        """
        self.value = value
        self.ricci = ricci
        self.metric = metric or (ricci.metric if ricci else None)

        if value is None and ricci is not None and metric is not None:
            self.value = self._compute_ricci_scalar()

    @classmethod
    def from_ricci(cls, ricci: RicciTensor) -> 'RicciScalar':
        """
        Create a Ricci scalar from a Ricci tensor.

        Args:
            ricci: Ricci tensor instance

        Returns:
            RicciScalar instance
        """
        return cls(ricci=ricci, metric=ricci.metric)

    @classmethod
    def from_metric(cls, metric: Metric) -> 'RicciScalar':
        """
        Create a Ricci scalar directly from a metric tensor.

        Args:
            metric: Metric tensor instance

        Returns:
            RicciScalar instance
        """
        ricci = RicciTensor.from_metric(metric)
        return cls.from_ricci(ricci)

    def _compute_ricci_scalar(self) -> sp.Expr:
        """
        Compute the Ricci scalar from the Ricci tensor and metric.

        Returns:
            SymPy expression representing the Ricci scalar
        """
        if self.ricci is None or self.ricci.components is None:
            raise ValueError("Valid Ricci tensor required to compute the Ricci scalar")

        if self.metric is None:
            raise ValueError("Valid metric tensor required to compute the Ricci scalar")

        n = self.metric.dimension
        Ricci = self.ricci.components
        g_inv = self.metric.inverse

        # Compute Ricci scalar by contracting Ricci tensor with inverse metric
        scalar = sum(g_inv[mu, nu] * Ricci[mu, nu] for mu in range(n) for nu in range(n))
        scalar = custom_simplify(scalar)

        return scalar

    def get_value(self, simplify: bool = True) -> sp.Expr:
        """
        Get the value of the Ricci scalar.

        Args:
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for the Ricci scalar R
        """
        if self.value is None:
            raise ValueError("Ricci scalar not computed")

        if simplify:
            return custom_simplify(self.value)
        return self.value

    def __str__(self) -> str:
        """
        String representation of the Ricci scalar.

        Returns:
            String showing the Ricci scalar value
        """
        if self.value is None:
            return "Ricci scalar not computed"

        return f"Ricci scalar (R):\nR = {custom_simplify(self.value)}"
