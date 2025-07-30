import pytest
from sympy import symbols, Matrix, Function, diff, simplify
from itensorpy.differential_ops.core import Field

class TestField:
    
    def setup_method(self):
        self.x, self.y, self.z = symbols('x y z')
        self.coords = [self.x, self.y, self.z]
        
        # Scalar field
        self.scalar_function = self.x**2 + self.y**2 + self.z**2
        self.scalar_field = Field(self.scalar_function, self.coords)
        
        # Vector field
        self.vector_function = Matrix([self.x*self.y, self.y*self.z, self.z*self.x])
        self.vector_field = Field(self.vector_function, self.coords)
    
    def test_field_initialization(self):
        assert self.scalar_field.f == self.scalar_function
        assert self.scalar_field.coords == self.coords
        
        assert self.vector_field.f == self.vector_function
        assert self.vector_field.coords == self.coords
    
    def test_scalar_field_gradient(self):
        grad = self.scalar_field.gradient()
        expected = Matrix([2*self.x, 2*self.y, 2*self.z])
        
        assert isinstance(grad, Matrix)
        assert grad.shape == (3, 1)
        for i in range(3):
            assert simplify(grad[i] - expected[i]) == 0
    
    def test_vector_field_divergence(self):
        div = self.vector_field.divergence()
        # Expected: d/dx(x*y) + d/dy(y*z) + d/dz(z*x) = y + z + x
        expected = self.y + self.z + self.x
        
        assert simplify(div - expected) == 0
    
    def test_scalar_field_laplacian(self):
        lap = self.scalar_field.laplacian()
        # Expected: ∇²(x² + y² + z²) = 2 + 2 + 2 = 6
        expected = 6
        
        assert simplify(lap - expected) == 0
    
    def test_vector_field_curl(self):
        curl = self.vector_field.curl()
        # Expected curl of [xy, yz, zx] is:
        # [d/dy(zx) - d/dz(yz), d/dz(xy) - d/dx(zx), d/dx(yz) - d/dy(xy)]
        # = [x - y, 0, 0]
        expected = Matrix([self.x - self.y, 0, 0])
        
        assert isinstance(curl, Matrix)
        assert curl.shape == (3, 1)
        for i in range(3):
            assert simplify(curl[i] - expected[i]) == 0
    
    def test_scalar_field_hessian(self):
        hess = self.scalar_field.hessian()
        # Expected Hessian of x² + y² + z² is a diagonal matrix with 2's
        expected = Matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
        
        assert isinstance(hess, Matrix)
        assert hess.shape == (3, 3)
        for i in range(3):
            for j in range(3):
                assert simplify(hess[i, j] - expected[i, j]) == 0
    
    def test_vector_field_jacobian(self):
        jac = self.vector_field.jacobian()
        # Jacobian of [xy, yz, zx]
        expected = Matrix([
            [self.y, self.x, 0],
            [0, self.z, self.y],
            [self.z, 0, self.x]
        ])
        
        assert isinstance(jac, Matrix)
        assert jac.shape == (3, 3)
        for i in range(3):
            for j in range(3):
                assert simplify(jac[i, j] - expected[i, j]) == 0 