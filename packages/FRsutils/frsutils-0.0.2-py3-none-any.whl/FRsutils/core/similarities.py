"""
frutil.similarities
====================

This module provides functions for computing similarities between normalized feature vectors and generating
similarity matrices. It is useful in fuzzy-rough set-based machine learning, clustering, and other
similarity-based computations.

All similarity functions assume values are in the normalized range [0.0, 1.0].

Functions
---------
- linear_similarity: Basic similarity measure based on inverse distance.
- compute_feature_similarities: Applies a similarity function elementwise on two vectors.
- aggregate_similarities: Aggregates an array of similarity scores into a single scalar.
- compute_similarity_matrix: Computes a full NxN similarity matrix from a dataset.
- compute_instance_similarities: Computes similarity scores between a single instance and a dataset.
"""

import numpy as np


def _linear_similarity_scalar(v1: float, v2: float) -> float:
    """
    Compute linear similarity between two scalar values using the formula:
    `max(0, 1 - |v1 - v2|)`

    Parameters
    ----------
    v1 : float
        First input value in the range [0.0, 1.0].
    v2 : float
        Second input value in the range [0.0, 1.0].

    Returns
    -------
    float
        Similarity score in the range [0.0, 1.0].

    Raises
    ------
    ValueError
        If either input or the output is outside the [0.0, 1.0] range.
    """
    sim = max(0.0, 1.0 - abs(v1 - v2))
    if not ((0.0 <= v1 <= 1.0) and (0.0 <= v2 <= 1.0) and (0.0 <= sim <= 1.0)):
        raise ValueError("inputs/outputs must be in [0.0, 1.0].")
    return sim

def _compute_feature_similarities(x1: np.ndarray, x2: np.ndarray, sim_func) -> np.ndarray:
    """
    Compute the similarity between two feature vectors using the provided similarity function.

    Parameters
    ----------
    x1 : np.ndarray
        First feature vector (1D array).
    x2 : np.ndarray
        Second feature vector (1D array), must be same length as x1.
    sim_func : Callable[[float, float], float]
        Similarity function to apply to each pair of feature values.

    Returns
    -------
    np.ndarray
        1D array of similarity scores between each pair of corresponding features.
    """
    fs = np.vectorize(sim_func)(x1, x2)
    return fs

def _aggregate_similarities(similarities: np.ndarray, agg_tnorm) -> float:
    """
    Aggregate a set of similarity scores into a single value using the provided aggregation tnorm.

    Parameters
    ----------
    similarities : np.ndarray
        Array of similarity scores in the range [0.0, 1.0].
    agg_tnorm : Callable[[np.ndarray], float]
        Aggregation tnorm.

    Returns
    -------
    float
        Aggregated similarity score.

    Raises
    ------
    ValueError
        If any similarity value is outside the range [0.0, 1.0].
    """
    if not ((0.0 <= similarities).all() and (similarities <= 1.0).all()):
        raise ValueError("All similarities must be in the range [0.0, 1.0].")
    agg = agg_tnorm(similarities)
    return agg

def compute_similarity_matrix(X: np.ndarray, sim_func, agg_func) -> np.ndarray:
    """
    Compute a pairwise similarity matrix for all instances in a dataset.

    Parameters
    ----------
    X : np.ndarray
        A 2D array of shape (n_samples, n_features).
    sim_func : Callable[[float, float], float]
        Similarity function to apply to feature pairs.
    agg_func : Callable[[np.ndarray], float]
        Aggregation function for reducing feature similarities to instance similarity.

    Returns
    -------
    np.ndarray
        A 2D similarity matrix of shape (n_samples, n_samples).
    """
    n = X.shape[0]
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        sims = np.array([
            _aggregate_similarities(
                _compute_feature_similarities(X[i], X[j], sim_func),
                agg_func
            ) for j in range(n)
        ])
        sim_matrix[i, :] = sims
    return sim_matrix

# def compute_instance_similarities(instance: np.ndarray, X: np.ndarray, sim_func, agg_func) -> np.ndarray:
#     """
#     Compute similarity scores between a single instance and all instances in a dataset.

#     Parameters
#     ----------
#     instance : np.ndarray
#         A 1D array representing a single instance (feature vector).
#     X : np.ndarray
#         A 2D array of shape (n_samples, n_features) representing the dataset.
#     sim_func : Callable[[float, float], float]
#         Similarity function for individual features.
#     agg_func : Callable[[np.ndarray], float]
#         Aggregation function for reducing feature-level similarities.

#     Returns
#     -------
#     np.ndarray
#         1D array of similarity scores between the instance and each sample in X.
#     """
#     return np.array([
#         aggregate_similarities(compute_feature_similarities(instance, other, sim_func), agg_func)
#         for other in X
#     ])