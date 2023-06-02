import numpy as np
from scipy.stats import pearsonr, spearmanr
import src.data_preprocessing.utils as utils
import pandas as pd
import numpy.testing as nptest

def test_assign_continents():
    continents = utils.assign_continents()
    assert continents.loc['Russia', 'continent'] == 'Europe'
    assert continents.loc['Kazakhstan', 'continent'] == 'Asia'
    assert continents.loc['Czechia', 'continent'] == 'Europe'

def test_get_continents():
    print(utils.get_continents())

class TestComputeDependencyMatrix:

    def test_compute_pearson_dependency(self):
        X = np.arange(0, 10)
        Y = X * 2 + 1
        metrics = pd.DataFrame(data=np.c_[X, Y])
        nptest.assert_almost_equal(np.array([[1.0, 1], [0, 1]]),
                                   utils.compute_dependency_matrix(metrics, pearsonr), decimal=1)

    def test_compute_spearmanr_dependency(self):
        X = np.arange(0, 10)
        Y = X * 2 + 1
        metrics = pd.DataFrame(data=np.c_[X, Y])
        nptest.assert_almost_equal(np.array([[1.0, 1], [0, 1]]),
                                   utils.compute_dependency_matrix(metrics, spearmanr), decimal=1)