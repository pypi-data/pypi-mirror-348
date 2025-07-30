# jacobian_hessian.py
from sympy import Matrix, diff

class JacobianHessianMixin:
    def jacobian(self):
        
        F = self.f if hasattr(self.f, '__iter__') else [self.f]
        J = []
        for fi in F:
            J.append([diff(fi, var) for var in self.coords])
        return Matrix(J)

    def hessian(self):
        
        f = self.f
        H = []
        for xi in self.coords:
            H.append([diff(f, xj, xi==xj and 2 or 1) for xj in self.coords])
        # Uwaga: symetria H, ale diff wymaga zamiany argumentów, więc lepiej:
        H = [[diff(f, xi, xj) for xj in self.coords] for xi in self.coords]
        return Matrix(H)
