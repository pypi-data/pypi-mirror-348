import pytest
from sympy import symbols, Matrix, sin, cos, exp, simplify
from itensorpy.utils import (
    generate_index_riemann,
    generate_index_ricci,
    generate_index_christoffel,
    lower_indices,
    custom_simplify
)

def test_generate_index_riemann():
    # Test dla funkcji generate_index_riemann
    indices_2d = generate_index_riemann(2)
    indices_4d = generate_index_riemann(4)
    
    # Sprawdzenie czy generowane są wszystkie indeksy
    assert len(indices_2d) > 0
    assert len(indices_4d) > 0
    
    # Sprawdzenie czy indeksy są unikalne
    assert len(indices_2d) == len(set(map(str, indices_2d)))
    assert len(indices_4d) == len(set(map(str, indices_4d)))
    
    # Sprawdzenie ograniczenia dla nieprawidłowego wymiaru
    with pytest.raises(ValueError):
        generate_index_riemann(0)

def test_generate_index_ricci():
    # Test dla funkcji generate_index_ricci
    indices_2d = generate_index_ricci(2)
    indices_4d = generate_index_ricci(4)
    
    # Sprawdzenie czy generowane są wszystkie indeksy
    assert len(indices_2d) > 0
    assert len(indices_4d) > 0
    
    # Sprawdzenie czy indeksy są unikalne
    assert len(indices_2d) == len(set(map(str, indices_2d)))
    assert len(indices_4d) == len(set(map(str, indices_4d)))
    
    # Sprawdzenie ograniczenia dla nieprawidłowego wymiaru
    with pytest.raises(ValueError):
        generate_index_ricci(0)

def test_generate_index_christoffel():
    # Test dla funkcji generate_index_christoffel
    indices_2d = generate_index_christoffel(2)
    indices_4d = generate_index_christoffel(4)
    
    # Sprawdzenie czy generowane są wszystkie indeksy
    assert len(indices_2d) > 0
    assert len(indices_4d) > 0
    
    # Sprawdzenie czy indeksy są unikalne
    assert len(indices_2d) == len(set(map(str, indices_2d)))
    assert len(indices_4d) == len(set(map(str, indices_4d)))
    
    # Sprawdzenie ograniczenia dla nieprawidłowego wymiaru
    with pytest.raises(ValueError):
        generate_index_christoffel(0)

def test_lower_indices():
    # Test dla funkcji lower_indices
    x, y = symbols('x y')
    metric = Matrix([[1, 0], [0, x**2]])
    tensor = Matrix([[y, 0], [0, sin(y)]])
    
    # Obniżanie indeksów
    lowered = lower_indices(tensor, metric, [0, 1])
    
    # Sprawdzenie czy wymiary są zachowane
    assert lowered.shape == tensor.shape
    
    # Sprawdzenie wartości
    assert lowered[0, 0] == y
    assert lowered[1, 1] == x**2 * sin(y)
    
    # Test dla niepoprawnych danych wejściowych
    with pytest.raises(ValueError):
        lower_indices(tensor, metric, [0, 1, 2])  # Zbyt dużo indeksów
        
    with pytest.raises(ValueError):
        lower_indices(tensor, Matrix([[1]]), [0, 1])  # Niewłaściwy wymiar metryki

def test_custom_simplify():
    # Test dla funkcji custom_simplify
    x, y = symbols('x y')
    
    # Proste wyrażenie
    expr1 = x + x
    assert custom_simplify(expr1) == 2*x
    
    # Bardziej złożone wyrażenie
    expr2 = sin(x)**2 + cos(x)**2
    simplified = custom_simplify(expr2)
    assert simplify(simplified - 1) == 0
    
    # Wyrażenie wykładnicze
    expr3 = exp(x + y) / exp(x)
    simplified = custom_simplify(expr3)
    assert simplified == exp(y)
    
    # Sprawdzenie dla macierzy
    mat = Matrix([[x + x, y], [0, sin(x)**2 + cos(x)**2]])
    simplified_mat = custom_simplify(mat)
    assert simplified_mat[0, 0] == 2*x
    assert simplify(simplified_mat[1, 1] - 1) == 0 