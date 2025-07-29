"""
Collection of fuzzy implicator functions.

This module provides a set of standard fuzzy logic implicators.
Each function takes two fuzzy truth values (floats in the range [0.0, 1.0])
and returns the result of the corresponding implicator.
"""

import numpy as np

def imp_gaines(a: float, b: float) -> float:
    """
    Gaines fuzzy implicator.

    Returns 1.0 if a <= b.
    Returns b / a if a > b and a > 0.
    Returns 0.0 if a == 0 and b < a.

    @param a: Antecedent value in the range [0.0, 1.0].
    @param b: Consequent value in the range [0.0, 1.0].
    @return: Result of Gaines' implicator.
    @throws ValueError: If either input is outside the range [0.0, 1.0].
    """
    if not (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("Inputs must be in range [0.0, 1.0].")
    if a <= b:
        return 1.0
    elif a > 0:
        return b / a
    else:
        return 0.0

def imp_goedel(a: float, b: float) -> float:
    """
    Gödel fuzzy implicator.

    Returns 1.0 if a <= b, otherwise returns b.

    @param a: Antecedent value in the range [0.0, 1.0].
    @param b: Consequent value in the range [0.0, 1.0].
    @return: Result of Gödel's implicator.
    @throws ValueError: If either input is outside the range [0.0, 1.0].
    """
    if not (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("Inputs must be in range [0.0, 1.0].")
    return 1.0 if a <= b else b

def imp_kleene_dienes(a: float, b: float) -> float:
    """
    Kleene-Dienes fuzzy implicator.

    Computes max(1 - a, b).

    @param a: Antecedent value in the range [0.0, 1.0].
    @param b: Consequent value in the range [0.0, 1.0].
    @return: Result of Kleene-Dienes implicator.
    @throws ValueError: If either input is outside the range [0.0, 1.0].
    """
    if not (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("Inputs must be in range [0.0, 1.0].")
    return max(1.0 - a, b)

def imp_reichenbach(a: float, b: float) -> float:
    """
    Reichenbach fuzzy implicator.

    Computes 1 - a + a * b.

    @param a: Antecedent value in the range [0.0, 1.0].
    @param b: Consequent value in the range [0.0, 1.0].
    @return: Result of Reichenbach implicator.
    @throws ValueError: If either input is outside the range [0.0, 1.0].
    """
    if not (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("Inputs must be in range [0.0, 1.0].")
    return 1.0 - a + a * b

def imp_lukasiewicz(a: float, b: float) -> float:
    """
    Łukasiewicz fuzzy implicator.

    Computes min(1, 1 - a + b).

    @param a: Antecedent value in the range [0.0, 1.0].
    @param b: Consequent value in the range [0.0, 1.0].
    @return: Result of Łukasiewicz implicator.
    @throws ValueError: If either input is outside the range [0.0, 1.0].
    """
    if not (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("Inputs must be in range [0.0, 1.0].")
    return min(1.0, 1.0 - a + b)
