import unittest
import math

import numpy as np
from cdtw import *
from numpy.testing import assert_array_equal, assert_array_almost_equal

try:
    import dtaidistance
    DTAIDISTANCE_INSTALLED = True
except ImportError:
    DTAIDISTANCE_INSTALLED = False


class TestCDTW(unittest.TestCase):

    def test_simple(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 4]

        cost_mat_expected = np.sqrt([
            [1, 5, 14],
            [1, 2, 6],
            [2, 1, 2],
            [6, 2, 1],
            [15, 6, 2]
        ])
        path_expected = [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)]

        cost_mat = dtw_mat(x, y)
        self.assertAlmostEqual(dtw_dist(x, y), math.sqrt(2.0), places=6)
        assert_array_almost_equal(cost_mat, cost_mat_expected)
        assert_array_equal(dtw_path(cost_mat), path_expected)

    def test_order_does_not_matter(self):
        np.random.seed(0)
        x = np.random.randn(100)
        y = np.random.randn(300)
        assert_array_almost_equal(dtw_mat(x, y), dtw_mat(y, x).T)
        self.assertAlmostEqual(dtw_dist(x, y), dtw_dist(y, x))

    def test_dtw_distance_path(self):
        np.random.seed(0)
        x = np.random.randn(10)
        y = np.random.randn(30)
        cost_mat = dtw_mat(x, y)
        self.assertAlmostEqual(cost_mat[-1, -1], dtw_dist(x, y), places=6)
        path = dtw_path(cost_mat)
        assert_array_equal(path[0], (0, 0))
        assert_array_equal(path[-1], (len(x) - 1, len(y) - 1))

    @unittest.skipUnless(DTAIDISTANCE_INSTALLED, "dtaidistance not installed")
    def test_dtaidistance(self):
        np.random.seed(0)
        x = np.random.randn(100).astype(np.float32)
        y = np.random.randn(30).astype(np.float32)
        self.assertAlmostEqual(dtw_dist(x, y),
                               dtaidistance.dtw.distance(x, y),
                               places=6)
        _, cost_mat_expected = dtaidistance.dtw.warping_paths(x, y)
        cost_mat = dtw_mat(x, y)
        assert_array_almost_equal(cost_mat, cost_mat_expected[1:, 1:],
                                  decimal=5)
        path_expected = dtaidistance.dtw.best_path(cost_mat_expected)
        assert_array_equal(dtw_path(cost_mat), path_expected)


if __name__ == '__main__':
    unittest.main()
