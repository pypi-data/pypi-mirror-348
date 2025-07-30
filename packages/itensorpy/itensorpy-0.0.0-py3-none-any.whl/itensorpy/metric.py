"""
Metric tensor module for general relativity calculations.
"""

import sympy as sp
from sympy import symbols, Symbol, Matrix
import functools
from typing import Dict, List, Tuple, Union, Optional

from .utils import custom_simplify


class Metric:
    """
    A class representing a metric tensor in general relativity.

    The metric tensor defines the geometry of spacetime and is fundamental
    for computing other tensors like Christoffel symbols, Riemann tensor, etc.
    """

    def __init__(self,
                 components: Union[Dict[Tuple[int, int], sp.Expr], Matrix, 'Metric'] = None,
                 coordinates: List[Symbol] = None,
                 params: List[Symbol] = None,
                 simplify_level: int = 2):
        """
        Initialize a metric tensor.

        Args:
            components: Dictionary mapping (i,j) tuples to symbolic expressions,
                       or a SymPy Matrix containing the metric components,
                       or another Metric object
            coordinates: List of symbolic coordinates (e.g., t, x, y, z)
            params: List of symbolic parameters used in the metric
            simplify_level: Level of simplification to apply (0 - 3)
        """
        # Initialize properties that will be cached
        self._g_inv = None
        self._determinant = None

        # Handle case where another Metric is passed
        if isinstance(components, Metric):
            self.coordinates = components.coordinates
            self.params = components.params
            self.g = components.g
            self.dimension = len(self.coordinates)
            self.simplify_level = components.simplify_level
            return

        self.coordinates = coordinates or []
        self.params = params or []
        
        # Validate coordinates
        if not self.coordinates:
            raise ValueError("Coordinates list cannot be empty")
            
        self.dimension = len(self.coordinates)
        self.simplify_level = simplify_level

        # Initialize the metric components
        if isinstance(components, Matrix):
            self.g = components
        elif isinstance(components, dict):
            self.g = self._dict_to_matrix(components)
        else:
            self.g = None

    def _dict_to_matrix(self, components_dict: Dict[Tuple[int, int], sp.Expr]) -> Matrix:
        """
        Convert a dictionary of components to a SymPy matrix.

        Args:
            components_dict: Dictionary mapping (i,j) tuples to symbolic expressions

        Returns:
            SymPy Matrix representing the metric
        """
        n = self.dimension
        matrix = sp.zeros(n, n)

        for (i, j), value in components_dict.items():
            matrix[i, j] = value
            # Metric is symmetric
            if i != j:
                matrix[j, i] = value

        return matrix

    @classmethod
    def from_file(cls, filename: str) -> 'Metric':
        """
        Load a metric from a text file.

        Format:
        - First line: coordinate symbols separated by commas, then semicolon, then parameters
        - Subsequent lines: i j expression (where i,j are indices and expression is the component)

        Args:
            filename: Path to the metric file

        Returns:
            Metric instance
        """
        symbol_assumptions = {
            'a': dict(real=True, positive=True),
            'tau': dict(real=True),
            'psi': dict(real=True),
            'theta': dict(real=True),
            'phi': dict(real=True),
        }

        def create_symbol(sym_name):
            if sym_name in symbol_assumptions:
                return sp.Symbol(sym_name, **symbol_assumptions[sym_name])
            else:
                return sp.Symbol(sym_name)

        coordinates = []
        params = []
        metric_components = {}

        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.split('#')[0].strip()
                    if not line:
                        continue

                    if ';' in line:
                        wsp_, prm_ = line.split(';')
                        wsp_strs = [sym.strip() for sym in wsp_.split(',') if sym.strip()]
                        coordinates = [create_symbol(s) for s in wsp_strs]

                        prm_ = prm_.strip()
                        if prm_:
                            par_strs = [sym.strip() for sym in prm_.split(',') if sym.strip()]
                            params = [create_symbol(s) for s in par_strs]
                    else:
                        dat = line.split(maxsplit=2)
                        if len(dat) == 3:
                            try:
                                i, j, expr = int(dat[0]), int(dat[1]), dat[2]
                                symbols_dict = {str(sym): sym for sym in coordinates + params}
                                metric_components[(i, j)] = sp.sympify(expr, locals=symbols_dict)
                            except ValueError:
                                print(f"Error: Incorrect data in line: {line}")
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return cls(components=metric_components, coordinates=coordinates, params=params)

    @functools.cached_property
    def inverse(self) -> Matrix:
        """
        Get the inverse of the metric tensor.

        Returns:
            SymPy Matrix representing the inverse metric
        """
        if self._g_inv is not None:
            return self._g_inv

        if self.g is not None:
            # For 2D metrics, we can compute inverse more efficiently
            if self.dimension == 2:
                return self._compute_2d_inverse()

            self._g_inv = self.g.inv()
            return self._g_inv

        raise ValueError("Metric components not defined")

    def _compute_2d_inverse(self) -> Matrix:
        """
        Compute inverse for 2D metric more efficiently.

        Returns:
            SymPy Matrix representing the inverse metric for 2D case
        """
        # For a 2x2 matrix, inverse is more efficiently computed as:
        # [a b]^-1 = 1/(ad - bc) * [d -b; -c a]
        g = self.g
        det = g[0, 0] * g[1, 1] - g[0, 1] * g[1, 0]
        inv = sp.Matrix([
            [g[1, 1]/det, -g[0, 1]/det],
            [-g[1, 0]/det, g[0, 0]/det]
        ])
        return inv

    def component(self, i: int, j: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the metric tensor.

        Args:
            i: First index
            j: Second index
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for the g_ij component
        """
        if self.g is None:
            raise ValueError("Metric components not defined")

        result = self.g[i, j]
        if simplify:
            return custom_simplify(result, self.simplify_level)
        return result

    def inverse_component(self, i: int, j: int, simplify: bool = True) -> sp.Expr:
        """
        Get a specific component of the inverse metric tensor.

        Args:
            i: First index
            j: Second index
            simplify: Whether to simplify the expression

        Returns:
            The symbolic expression for the g^ij component
        """
        result = self.inverse[i, j]
        if simplify:
            return custom_simplify(result, self.simplify_level)
        return result

    @functools.cached_property
    def determinant(self) -> sp.Expr:
        """
        Calculate the determinant of the metric.

        Returns:
            sympy.Expr: The determinant of the metric tensor
        """
        if self._determinant is not None:
            return self._determinant

        if self.g is None:
            raise ValueError("Metric components not defined")

        self._determinant = self.g.det()
        return self._determinant

    def det(self) -> sp.Expr:
        """
        Calculate the determinant of the metric (legacy method).

        Returns:
            sympy.Expr: The determinant of the metric tensor
        """
        return self.determinant

    def __str__(self) -> str:
        """
        Return a string representation of the metric.

        Returns:
            String showing the non - zero components of the metric
        """
        if self.g is None:
            return "Metric not defined"

        result = "Metric tensor g_{ij}:\n"

        # Display only non - zero components
        for i in range(self.dimension):
            for j in range(i, self.dimension):  # Use symmetry
                value = self.component(i, j, simplify=True)
                if value != 0:
                    result += f"g_{{{i}{j}}} = {value}\n"

        return result
