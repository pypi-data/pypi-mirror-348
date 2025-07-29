# frutil/models/vqrs.py
"""
VQRS implementation.
"""
import numpy as np

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

from approximations import FuzzyRoughModel
import numpy as np

class VQRS(FuzzyRoughModel):
    def __init__(self, similarity_matrix: np.ndarray, labels: np.ndarray, alpha: float = 0.5, beta: float = 0.5):
        super().__init__(similarity_matrix, labels)
        if not (0.0 <= alpha <= 1.0 and 0.0 <= beta <= 1.0):
            raise ValueError("Alpha and beta must be in range [0.0, 1.0].")
        self.alpha = alpha
        self.beta = beta

    def lower_approximation(self):
        raise NotImplementedError
        return (self.similarity_matrix >= self.alpha).astype(float).min(axis=1)

    def upper_approximation(self):
        raise NotImplementedError
        return (self.similarity_matrix >= self.beta).astype(float).max(axis=1)