import pytest
import numpy as np
from sympy import symbols
from itensorpy.tensor_ops.core import TensorND
from itensorpy.tensor_ops.einsum import parse_einsum_pairs

class TestEinsumExtended:
    
    def test_parse_einsum_pairs_matrix_mult(self):
        # Test dla mnożenia macierzy "ij,jk->ik"
        input_notations = ['ij', 'jk']
        output_notation = 'ik'
        
        pairs = parse_einsum_pairs(input_notations, output_notation)
        
        # Powinien zwrócić parę (1, 2) dla kontraktowania j z j
        assert len(pairs) == 1
        assert (1, 2) in pairs
    
    def test_parse_einsum_pairs_trace(self):
        # Test dla śladu macierzy "ii->"
        input_notations = ['ii']
        output_notation = ''
        
        pairs = parse_einsum_pairs(input_notations, output_notation)
        
        # Powinien zwrócić parę (0, 1) dla kontraktowania i z i
        assert len(pairs) == 1
        assert (0, 1) in pairs
    
    def test_parse_einsum_pairs_tensor_contraction(self):
        # Test dla kontrakcji tensora "ijk,klm->ijlm"
        input_notations = ['ijk', 'klm']
        output_notation = 'ijlm'
        
        pairs = parse_einsum_pairs(input_notations, output_notation)
        
        # Powinien zwrócić parę dla kontraktowania k z k
        assert len(pairs) == 1
        # Indeks k jest na pozycji 2 w pierwszym tensorze i 0 w drugim
        expected_pair = (2, 3)  # Uwzględniając offset
        assert expected_pair in pairs
    
    def test_parse_einsum_pairs_multiple_contractions(self):
        # Test dla wielu kontrakcji "ijk,jli->kl"
        input_notations = ['ijk', 'jli']
        output_notation = 'kl'
        
        pairs = parse_einsum_pairs(input_notations, output_notation)
        
        # Powinny być 2 pary do kontraktowania: i oraz j
        assert len(pairs) == 2
        
        # Sprawdzamy, czy kontraktowane są właściwe indeksy
        # Pierwsze 'j' jest na pozycji 1 w pierwszym tensorze, 
        # drugie 'j' jest na pozycji 0 w drugim tensorze (offset 3)
        assert (1, 3) in pairs
        
        # Pierwsze 'i' jest na pozycji 0 w pierwszym tensorze,
        # drugie 'i' jest na pozycji 2 w drugim tensorze (offset 3)
        assert (0, 5) in pairs
    
    def test_einsum_product_with_complex_notation(self):
        # Test bardziej złożonej operacji einsum
        A = TensorND(np.random.rand(2, 3, 2))
        B = TensorND(np.random.rand(2, 3, 4))
        
        # Operacja: A_ijk * B_ilm -> A_jklm
        result = A.einsum_product("ijk,ilm->jklm", B)
        
        # Sprawdzenie kształtu wyniku
        expected_shape = (3, 2, 3, 4)
        assert result.shape == expected_shape
        
        # Porównanie z numpy.einsum
        np_A = A.to_numpy()
        np_B = B.to_numpy()
        expected = np.einsum("ijk,ilm->jklm", np_A, np_B)
        
        np.testing.assert_allclose(result.to_numpy(), expected)
    
    def test_einsum_product_symbolic(self):
        # Test z symbolicznymi wartościami
        a, b = symbols('a b')
        A = TensorND([[a, b], [b, a]])
        B = TensorND([[1, 0], [0, 1]])
        
        # Operacja: A_ij * B_jk -> A_ik (mnożenie macierzy)
        result = A.einsum_product("ij,jk->ik", B)
        
        # Sprawdzamy czy wymiar jest poprawny
        assert result.shape == (2, 2)
        
        # Sprawdzamy wartości
        assert result.data[0, 0] == a
        assert result.data[0, 1] == b
        assert result.data[1, 0] == b
        assert result.data[1, 1] == a
    
    def test_einsum_reduce_diagonal(self):
        # Test operacji redukcji dla przekątnej
        A = TensorND([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        # Operacja: A_ii -> suma przekątnej (ślad)
        result = A.einsum_reduce("ii->")
        
        # Sprawdzenie wyniku
        expected = 1 + 5 + 9  # Suma elementów na przekątnej
        assert result == expected
    
    def test_einsum_reduce_sum_over_indices(self):
        # Test sumowania po indeksach
        A = TensorND([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        
        # Operacja: A_ijk -> A_i (suma po j,k)
        result = A.einsum_reduce("ijk->i")
        
        # Sprawdzenie kształtu
        assert result.shape == (2,)
        
        # Sprawdzenie wyniku
        expected = np.array([10, 26])  # Suma po j,k dla każdego i
        np.testing.assert_allclose(result.to_numpy(), expected) 