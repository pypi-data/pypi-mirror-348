class ShapeMixin:

    def reshape(self, new_shape):
        """Reshape the tensor to a new shape"""
        # Manual unpacking of the new_shape tuple if it's nested
        if len(new_shape) == 1 and isinstance(new_shape[0], tuple):
            new_shape = new_shape[0]
            
        return self.__class__(self.data.reshape(*new_shape))

    def transpose(self, axes=None):
        """Transpose the tensor along the specified axes"""
        # Default transpose without specifying axes
        if axes is None:
            axes = list(range(self.ndim))[::-1]  # Reverse the order of dimensions
            
        # In sympy, transpose takes a permutation list, not individual axes
        return self.__class__(self.data.transpose(axes))
