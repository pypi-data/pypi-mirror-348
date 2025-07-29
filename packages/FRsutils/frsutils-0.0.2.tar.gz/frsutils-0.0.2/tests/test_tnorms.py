import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core')))

import tnorms
import syntetic_data_for_tests as sds
# Data used for running tests

data = np.array([0.5, 0.7, 0.34, 0.98, 1.2])

def test_tn_minimum():
    assert tnorms.tn_minimum(data) == 0.34

def test_tn_product():
    assert np.isclose(tnorms.tn_product(np.array([0.5, 0.5])), 0.25)
    assert np.isclose(tnorms.tn_product(data), 0.139944)
    
# def test_tn_lukasiewicz():
#     assert np.isclose(tnorms.tn_lukasiewicz(np.array([0.9, 0.3])), 0.2)

def test_tn_minimum_scalar_values():
    data_dict = sds.syntetic_dataset_factory().tnorm_scalar_testing_data()
    a_b = data_dict["a_b"]
    expected = data_dict["minimum_outputs"]
    temp_tnorm = tnorms.tn_minimum

    result = []

    l = len(a_b)
    for i in range(l):
        result.append(temp_tnorm(a_b[i]))
    
    closeness = np.isclose(result, expected)
    assert np.all(closeness), "outputs are not the expected values"

def test_tn_product_scalar_values():
    data_dict = sds.syntetic_dataset_factory().tnorm_scalar_testing_data()
    a_b = data_dict["a_b"]
    expected = data_dict["product_outputs"]
    temp_tnorm = tnorms.tn_product

    result = []

    l = len(a_b)
    for i in range(l):
        result.append(temp_tnorm(a_b[i]))
    
    closeness = np.isclose(result, expected)
    assert np.all(closeness), "outputs are not the expected values"

# def test_tn_luk_scalar_values():
#     data_dict = sds.syntetic_dataset_factory().tnorm_scalar_testing_data()
#     a_b = data_dict["a_b"]
#     expected = data_dict["luk_outputs"]
#     temp_tnorm = tnorms.tn_luk

#     result = []

#     l = len(a_b)
#     for i in range(l):
#         result.append(temp_tnorm(a_b[i]))
    
#     closeness = np.isclose(result, expected)
#     assert np.all(closeness), "outputs are not the expected values"

def test_tn_minimum_nxnx2_map_values():
    data_dict = sds.syntetic_dataset_factory().tnorm_nxnx2_testing_dataset()
    nxnx2_map = data_dict["nxnx2_map"]
    expected = data_dict["minimum_outputs"]
    temp_tnorm = tnorms.tn_minimum

    result = temp_tnorm(nxnx2_map)
    
    closeness = np.isclose(result, expected)
    assert np.all(closeness), "outputs are not the expected values"

def test_tn_product_nxnx2_map_values():
    data_dict = sds.syntetic_dataset_factory().tnorm_nxnx2_testing_dataset()
    nxnx2_map = data_dict["nxnx2_map"]
    expected = data_dict["product_outputs"]
    temp_tnorm = tnorms.tn_product

    result = temp_tnorm(nxnx2_map)
    
    closeness = np.isclose(result, expected)
    assert np.all(closeness), "outputs are not the expected values"