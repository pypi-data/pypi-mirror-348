# gradient.py

from sympy import diff, Matrix, Expr

class GradientMixin:
    """
    Mix-in providing gradient calculation for scalar functions.
    """

    def gradient(self):
        """
        Calculate the gradient ∇f for a scalar field f.
        Returns a sympy Matrix (column vector) of partial derivatives.
        """
        f = self.f
        coords = self.coords

        if not isinstance(f, Expr):
            raise TypeError(f"gradient: f must be a sympy Expr, got {type(f).__name__}")

        # dla stałych diff zwróci 0, więc nie trzeba dodatkowej obsługi
        return Matrix([diff(f, var) for var in coords])
