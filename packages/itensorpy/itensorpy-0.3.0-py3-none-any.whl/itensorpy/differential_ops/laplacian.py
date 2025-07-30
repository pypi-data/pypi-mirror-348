from sympy import diff


class LaplacianMixin:
    def laplacian(self):
        f = self.f
        return sum(diff(f, coord, 2) for coord in self.coords)
