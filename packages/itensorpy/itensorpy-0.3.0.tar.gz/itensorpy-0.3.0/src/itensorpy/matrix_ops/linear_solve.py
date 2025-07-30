# linear_solve.py

import sympy as _sympy
from sympy import Matrix as _M

class LinearSolveMixin:
    
    def solve(self, b):
        """
        Solves the linear system Ax = b, where A is this matrix.
        
        Args:
            b: The right-hand side of the equation, should be a MatrixOps instance
            
        Returns:
            MatrixOps: solution to the system
        """
        if not hasattr(b, 'mat'):
            raise TypeError("b must be a MatrixOps instance")
            
        # Get the raw sympy Matrix from b
        b_mat = b.mat
        
        # Solve the system using sympy's solve_linear_system
        x = self.mat.solve(b_mat)
        
        # Return the solution as a MatrixOps instance
        return self.__class__(x)

    def _symbols_for_vars(self):
        
        from sympy import symbols
        n = self.mat.cols
        return symbols(f'x0:{n}')
