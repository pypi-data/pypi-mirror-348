# eigen.py

class EigenMixin:
   
    def eigenvalues(self):
        """Return the eigenvalues of this matrix"""
        return self.mat.eigenvals()
    
    def eigenvectors(self):
        """Return the eigenvectors of this matrix"""
        return self.mat.eigenvects()
