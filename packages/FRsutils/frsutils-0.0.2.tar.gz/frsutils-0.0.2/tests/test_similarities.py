import numpy as np
import sys
import os
import syntetic_data_for_tests as sds

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core')))

import similarities
import tnorms as tn

def test_linear_similarity():
    assert similarities._linear_similarity_scalar(1.0, 1.0) == 1.0
    assert similarities._linear_similarity_scalar(0.0, 1.0) == 0.0
    assert similarities._linear_similarity_scalar(0.3, 0.5) == 0.8
    assert similarities._linear_similarity_scalar(0.73, 0.91) == 0.82

def test_compute_feature_similarities_linear():
    x1 = np.array([0.1, 0.2])
    x2 = np.array([0.3, 0.8])
    sim = similarities._compute_feature_similarities(x1, x2, sim_func=similarities._linear_similarity_scalar)
    assert np.allclose(sim, [0.8, 0.4])
    assert sim.shape == x1.shape
    assert (0.0 <= sim).all() and (sim <= 1.0).all()

def test_aggregate_similarities():
    sims = np.array([0.8, 0.9, 0.56])
    agg = similarities._aggregate_similarities(sims, agg_tnorm=tn.tn_minimum)
    assert agg == 0.56
    assert 0.0 <= agg <= 1.0
    
    agg = similarities._aggregate_similarities(sims, agg_tnorm=tn.tn_product)
    assert np.isclose(agg, 0.4032)
    assert 0.0 <= agg <= 1.0

def test_compute_similarity_matrix_with_linear_similarity_product_tnorm():
    dsm = sds.syntetic_dataset_factory()
    data_dict = dsm.similarity_testing_dataset()
    X = data_dict["X"]
    expected = data_dict["sim_matrix_with_linear_similarity_product_tnorm"]

    sim_matrix = similarities.compute_similarity_matrix(X, sim_func=similarities._linear_similarity_scalar, agg_func=tn.tn_product)
    assert sim_matrix.shape == (5, 5), "dimension mismatch"
    assert (0.0 <= sim_matrix).all() and (sim_matrix <= 1.0).all(), "similarity matrix values are not normalized"
    closeness = np.isclose(sim_matrix, expected)
    assert np.all(closeness), "outputs are not the expected values"


def test_compute_similarity_matrix_with_linear_similarity_minimum_tnorm():
    dsm = sds.syntetic_dataset_factory()
    data_dict = dsm.similarity_testing_dataset()
    X = data_dict["X"]
    expected = data_dict["sim_matrix_with_linear_similarity_minimum_tnorm"]

    sim_matrix = similarities.compute_similarity_matrix(X, sim_func=similarities._linear_similarity_scalar, agg_func=tn.tn_minimum)
    assert sim_matrix.shape == (5, 5), "dimension mismatch"
    assert (0.0 <= sim_matrix).all() and (sim_matrix <= 1.0).all(), "similarity matrix values are not normalized"
    closeness = np.isclose(sim_matrix, expected)
    assert np.all(closeness), "outputs are not the expected values"


# def test_compute_instance_similarities_basic():
#     X = np.array([
#         [0.0, 0.5],
#         [0.5, 0.5],
#         [1.0, 0.5]
#     ])
#     instance = np.array([0.25, 0.7])
#     sims = similarities.compute_instance_similarities(instance, X, sim_func=similarities._linear_similarity_scalar, agg_func=tn.tn_minimum)
#     expected = np.array([
#         min(similarities._linear_similarity_scalar(0.25, 0.0), similarities._linear_similarity_scalar(0.7, 0.5)),
#         min(similarities._linear_similarity_scalar(0.25, 0.5), similarities._linear_similarity_scalar(0.7, 0.5)),
#         min(similarities._linear_similarity_scalar(0.25, 1.0), similarities._linear_similarity_scalar(0.7, 0.5))
#     ])
#     np.testing.assert_allclose(sims, expected, rtol=1e-5)

# def test_compute_instance_similarities_output_range():
#     X = np.array([
#         [0.1, 0.9],
#         [0.4, 0.4],
#         [0.9, 0.1]
#     ])
#     instance = np.array([0.5, 0.5])
#     sims = similarities.compute_instance_similarities(instance, X, sim_func=similarities._linear_similarity_scalar, agg_func=tn.tn_minimum)
#     assert np.all((0.0 <= sims) & (sims <= 1.0)), "All similarity values should be in range [0.0, 1.0]"

# def test_compute_instance_similarities_shape():
#     X = np.random.rand(10, 5)
#     instance = X[0]
#     sims = similarities.compute_instance_similarities(instance, X, sim_func=similarities._linear_similarity_scalar, agg_func=tn.tn_minimum)
#     assert sims.shape == (10,), "Output should have shape (n_samples,)"
