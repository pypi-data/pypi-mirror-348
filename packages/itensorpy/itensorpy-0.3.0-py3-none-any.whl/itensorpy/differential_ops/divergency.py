# divergence.py

from sympy import diff
from sympy.core.expr import Expr

class DivergenceMixin:
    """
    Mix-in providing divergence calculation for vector fields.
    """

    def divergence(self):
        """
        Calculate the divergence ∇·F for a vector field F.
        Returns a sympy expression: sum_i ∂F_i/∂x_i.
        """
        coords = self.coords
        F = self.f

        # spróbujmy zamienić na listę wyrażeń
        try:
            components = list(F)
        except TypeError:
            raise TypeError("divergence: f must be an iterable of sympy Expr")

        if len(components) != len(coords):
            raise ValueError(
                f"divergence: number of field components ({len(components)}) "
                f"!= number of coordinates ({len(coords)})"
            )

        # sumujemy pochodne ∂Fi/∂xi
        return sum(diff(comp, var) for comp, var in zip(components, coords))
