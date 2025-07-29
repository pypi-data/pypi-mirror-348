# frutil/tnorms.py
"""
Collection of common T-norm functions.
"""
import numpy as np

def tn_minimum(values: np.ndarray):
    """
    Computes the minimum T-norm of the input array.

    If the input is a 1D array, returns the minimum value.
    If the input is a 3D array of shape (n, n, 2), computes the element-wise
    minimum along the last axis (between [:, :, 0] and [:, :, 1]), which is
    useful for vectorized similarity calculations.

    @param values: A scalar or a NumPy array that is either:
        - scalar
        - 3-dimensional numpy array: shape (n, n, 2)
    @return: The minimum value(s) computed as described above.
    @throws ValueError: If the input is not a 1D or 3D NumPy array.
    """
    if(values.ndim == 1):
        return np.min(values)
    elif(values.ndim == 3):
        return np.min(values, axis=-1)
    raise ValueError("Input must be a 1-dimensional or 3-dimensional numpy array.")
    
def tn_product(values: np.ndarray):
    """
    Computes the product T-norm of the input array.

    If the input is a 1D array, returns the product of all elements.
    If the input is a 3D array of shape (n, n, 2), computes the element-wise
    product along the last axis (between [:, :, 0] and [:, :, 1]), which is
    useful for vectorized similarity calculations.

    @param values: A scalar or a NumPy array that is either:
        - scalar
        - 3-dimensional numpy array: shape (n, n, 2)
    @return: The product value(s) computed as described above.
    @throws ValueError: If the input is not a 1D or 3D NumPy array.
    """
    if(values.ndim == 1):
        return np.prod(values)
    elif(values.ndim == 3):
        return np.prod(values, axis=-1)
    raise ValueError("Input must be a 1-dimensional or 3-dimensional numpy array.")

