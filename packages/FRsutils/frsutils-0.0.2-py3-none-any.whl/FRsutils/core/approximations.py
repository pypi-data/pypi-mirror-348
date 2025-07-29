# frutil/approximations.py
"""
Module containing base classes for fuzzy-rough approximations.
"""
from abc import ABC, abstractmethod
import numpy as np

class FuzzyRoughModel(ABC):
    """Abstract base class for fuzzy-rough models."""
    def __init__(self, similarity_matrix: np.ndarray, labels: np.ndarray):
        if not ((0.0 <= similarity_matrix).all() and (similarity_matrix <= 1.0).all()):
            raise ValueError("All similarity values must be in the range [0.0, 1.0].")
        self.similarity_matrix = similarity_matrix
        self.labels = labels

    @abstractmethod
    def lower_approximation(self):
        pass

    @abstractmethod
    def upper_approximation(self):
        pass

    def boundary_region(self):
        return self.upper_approximation() - self.lower_approximation()

    def positive_region(self):
        return self.lower_approximation()