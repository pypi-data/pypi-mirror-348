"""
Utility functions for tensor operations and index management.
"""

import sympy as sp
import functools


@functools.lru_cache(maxsize=64)
def generate_index_riemann(n):
    """
    Generate all unique indices for Riemann tensor components.

    Args:
        n (int): Dimension of the space

    Returns:
        list: List of tuples (a,b,c,d) representing unique Riemann components
        
    Raises:
        ValueError: If n <= 0
    """
    if n <= 0:
        raise ValueError("Dimension must be a positive integer")
    
    index = []
    for a in range(n):
        for b in range(a, n):
            for c in range(n):
                for d in range(c, n):
                    if (a * n + b) <= (c * n + d):
                        index.append((a, b, c, d))
    return index


@functools.lru_cache(maxsize=32)
def generate_index_ricci(n):
    """
    Generate all unique indices for Ricci tensor components.

    Args:
        n (int): Dimension of the space

    Returns:
        list: List of tuples (i,j) representing unique Ricci components
        
    Raises:
        ValueError: If n <= 0
    """
    if n <= 0:
        raise ValueError("Dimension must be a positive integer")
    
    index = []
    for i in range(n):
        for j in range(i, n):
            index.append((i, j))
    return index


@functools.lru_cache(maxsize=32)
def generate_index_christoffel(n):
    """
    Generate all unique indices for Christoffel symbols.

    Args:
        n (int): Dimension of the space

    Returns:
        list: List of tuples (a,b,c) representing unique Christoffel components
        
    Raises:
        ValueError: If n <= 0
    """
    if n <= 0:
        raise ValueError("Dimension must be a positive integer")
    
    index = []
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                index.append((a, b, c))
    return index


def lower_indices(tensor, metric, n):
    """
    Lower the first index of a tensor (supports both rank-2 matrices and rank-4 Riemann tensors).

    Args:
        tensor: Either a 2D Matrix or a 4D nested list representing the tensor with first index up
        metric (Matrix): Metric tensor (g_μν)
        n (list or int): Dimensions or dimension of the space

    Returns:
        The tensor with first index lowered, in the same format as the input tensor

    Raises:
        ValueError: If dimensions don't match or inputs are invalid
        TypeError: If tensor type is not supported
    """
    # If n is a list, use the length as the dimension
    if isinstance(n, list):
        dimension = len(n)
    else:
        dimension = n
    
    # Check if tensor is a matrix (rank-2)
    if hasattr(tensor, 'shape'):
        if tensor.shape[0] != dimension or tensor.shape[1] != dimension:
            raise ValueError("Tensor dimensions don't match specified dimension")
            
        if metric.shape[0] != dimension or metric.shape[1] != dimension:
            raise ValueError("Metric dimensions don't match specified dimension")
        
        # Create result matrix of the same shape
        result = sp.zeros(dimension, dimension)
        
        # Lower the indices for rank-2 tensor
        for a in range(dimension):
            for b in range(dimension):
                result[a, b] = sum(metric[a, i] * tensor[i, b] for i in range(dimension))
        
        return result
    
    # Check if tensor is a 4D nested list (rank-4, like Riemann tensor)
    elif isinstance(tensor, list) and all(isinstance(inner, list) for inner in tensor):
        # Create a 4D result array
        result = [[[[0 for _ in range(dimension)] for _ in range(dimension)] 
                   for _ in range(dimension)] for _ in range(dimension)]
        
        # Lower the first index
        for a in range(dimension):
            for b in range(dimension):
                for c in range(dimension):
                    for d in range(dimension):
                        result[a][b][c][d] = sum(metric[a, i] * tensor[i][b][c][d] for i in range(dimension))
        
        return result
    
    else:
        raise TypeError("Unsupported tensor type. Must be either a Matrix or a nested list.")


def custom_simplify(expr, level=2):
    """
    Apply simplification with controllable intensity levels.

    Args:
        expr: SymPy expression to simplify
        level (int): Simplification level
            0: No simplification (return as is)
            1: Basic (expand only)
            2: Medium (expand, trigsimp, cancel) - DEFAULT
            3: Full (all operations, expensive but thorough)

    Returns:
        Simplified SymPy expression
    """
    if level == 0:
        return expr

    if level >= 1:
        expr = sp.expand(expr)

    if level >= 2:
        expr = sp.trigsimp(expr)
        expr = sp.cancel(expr)

    if level >= 3:
        expr = sp.factor(expr)
        expr = sp.simplify(expr)
        expr = sp.ratsimp(expr)

    return expr


# Additional utility functions from code.mdc

def write_scalar_curvatre(scalar_curvature, n):
    """Write the scalar curvature to the console."""
    print("Curvature scalar R:")
    sp.pprint(scalar_curvature)
    print("")


def write_einstein_components(G_upper, G_lower, n):
    """Write the Einstein tensor components to the console."""
    print("Non zero Einstein tensor (G^i_j):")
    for i in range(n):
        for j in range(n):
            val = custom_simplify(G_upper[i, j])
            if val != 0:
                print(f"G^{{{i}}}_{{{j}}} = {val}")
    print("")

    print("Non zero Einstein tensor (G_ij):")
    for i in range(n):
        for j in range(n):
            val = custom_simplify(G_lower[i, j])
            if val != 0:
                print(f"G_{{{i}{j}}} = {val}")
    print("")


def write_metric_components(g, n):
    """Write the metric tensor components to the console."""
    print("Metric tensor (g_{ij}):")
    for i in range(n):
        for j in range(i, n):
            val = custom_simplify(g[i, j])
            if val != 0:
                print(f"g_{i}{j} = {val}")
    print("")


def write_christoffel_symbols(Gamma, n):
    """Write the Christoffel symbols to the console."""
    print("Non zero Christoffel symbols (Γ^a_{bc}):")
    ch_index = generate_index_christoffel(n)
    for (a, b, c) in ch_index:
        val = Gamma[a][b][c]
        if custom_simplify(val) != 0:
            print(f"\\Gamma^{{{a}}}_{{{b}{c}}} = {val}")
    print("")


def write_full_riemann_components(R_abcd, n):
    """Write the Riemann tensor components to the console."""
    print("Non zero components Riemann tensor (R_{abcd}):")
    riemann_index = generate_index_riemann(n)
    for (a, b, c, d) in riemann_index:
        val = R_abcd[a][b][c][d]
        if val != 0:
            print(f"R_{{{a}{b}{c}{d}}} = {val}")
    print("")


def write_ricci_components(Ricci, n):
    """Write the Ricci tensor components to the console."""
    print("Non zero components Ricci tensor (R_{ij}):")
    ricci_index = generate_index_ricci(n)
    for (i, j) in ricci_index:
        val = Ricci[i, j]
        if val != 0:
            print(f"R_{{{i}{j}}} = {val}")
    print("")


def wczytaj_metryke(filename):
    """Load a metric from a text file."""
    symbol_assumptions = {
        'a':    dict(real=True, positive=True),
        'tau':  dict(real=True),
        'psi':  dict(real=True),
        'theta':dict(real=True),
        'phi':  dict(real=True),
    }

    def create_symbol(sym_name):
        if sym_name in symbol_assumptions:
            return sp.Symbol(sym_name, **symbol_assumptions[sym_name])
        else:
            return sp.Symbol(sym_name)

    wspolrzedne = []
    parametry = []
    metryka = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.split('#')[0].strip()
                if not line:
                    continue

                if ';' in line:
                    wsp_, prm_ = line.split(';')
                    wsp_strs = [sym.strip() for sym in wsp_.split(',') if sym.strip()]
                    wspolrzedne = [create_symbol(s) for s in wsp_strs]

                    prm_ = prm_.strip()
                    if prm_:
                        par_strs = [sym.strip() for sym in prm_.split(',') if sym.strip()]
                        parametry = [create_symbol(s) for s in par_strs]
                else:
                    dat = line.split(maxsplit=2)
                    if len(dat) == 3:
                        try:
                            i, j, expr = int(dat[0]), int(dat[1]), dat[2]

                            symbols_dict = {str(sym): sym for sym in wspolrzedne + parametry}
                            metryka[(i, j)] = sp.sympify(expr, locals=symbols_dict)
                        except ValueError:
                            print(f"Error: Incorrect data in line: {line}")
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return wspolrzedne, parametry, metryka
