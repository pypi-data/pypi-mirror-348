from sympy import symbols, Matrix
from .gradient import GradientMixin
from .divergency import DivergenceMixin
from .laplacian import LaplacianMixin
from .curl import CurlMixin
from .jacobian_hessian import JacobianHessianMixin


class Field(GradientMixin, 
            DivergenceMixin, 
            LaplacianMixin, 
            CurlMixin, 
            JacobianHessianMixin):
    
    def __init__(self, f, coords):
        self.f = f
        self.coords = coords
