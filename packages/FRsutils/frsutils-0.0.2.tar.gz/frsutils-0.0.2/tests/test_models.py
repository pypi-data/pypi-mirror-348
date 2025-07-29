import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core/models')))

from models import OWAFRS, VQRS, ITFRS
from similarities import compute_similarity_matrix

def get_sample_data():
    X = np.array([[0.0], [1.0]])
    y = np.array([0, 1])
    sim_matrix = compute_similarity_matrix(X)
    return sim_matrix, y

def test_owafrs():
    sim, y = get_sample_data()
    model = OWAFRS(sim, y)
    assert (0.0 <= model.lower_approximation()).all()
    assert (0.0 <= model.upper_approximation()).all()

def test_vqrs():
    sim, y = get_sample_data()
    model = VQRS(sim, y, alpha=0.3, beta=0.7)
    assert (0.0 <= model.lower_approximation()).all()
    assert (0.0 <= model.upper_approximation()).all()

def test_itfrs():
    sim, y = get_sample_data()
    model = ITFRS(sim, y)
    assert (0.0 <= model.lower_approximation()).all()
    assert (0.0 <= model.upper_approximation()).all()
