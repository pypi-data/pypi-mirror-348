from sympy import tensorcontraction


class ContractionMixin:

    def contract_indices(self, i, j):
        """Contract the tensor along the specified indices"""
        # MutableDenseNDimArray doesn't have trace, so we use tensorcontraction
        # which takes a list of pairs of indices to contract
        return self.__class__(tensorcontraction(self.data, [(i, j)]))
