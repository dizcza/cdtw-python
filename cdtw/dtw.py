"""
Dynamic Time Warping Python API
-------------------------------

.. autosummary::
    :toctree: toctree

    dtw_dist
    dtw_mat
    dtw_path
"""

import numpy as np

from cdtw.utils import cdtwlib


__all__ = [
    "dtw_dist",
    "dtw_mat",
    "dtw_path"
]


def dtw_mat(x, y):
    r"""
    Computes the full cost (distance) matrix ``D`` between all elements of
    ``x`` and ``y`` according to

    .. math::
        \boldsymbol{D}_{ij} = d(x_i, y_j) +
        \min{\lbrace \boldsymbol{D}_{i-1,j-1}, \boldsymbol{D}_{i-1, j},
                     \boldsymbol{D}_{i, j-1} \rbrace}

    where :math:`d(x_i, y_j)` is the Euclidean squared metric. A squared root
    of the output matrix ``D`` is returned.

    Parameters
    ----------
    x, y : np.ndarray
        Input time series, 1-d arrays of arbitrary size.

    Returns
    -------
    cost_mat : np.ndarray
        A squared root of the distance matrix ``D``.
    """
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    nx, ny = len(x), len(y)
    cost_mat = np.zeros((nx + 1) * (ny + 1), dtype=np.float32)
    cdtwlib.dtw_mat(cost_mat, x, y, nx, ny)
    cost_mat = cost_mat.reshape((nx + 1, ny + 1))
    cost_mat = np.sqrt(cost_mat, out=cost_mat)
    # the first row & col are inf
    return cost_mat[1:, 1:]


def dtw_dist(x, y):
    """
    Computes the DTW distance between ``x`` and ``y`` aligned in time, using
    dynamic programming. It's equivalent but more efficient to calling
    ``dtw_mat(x, y)[-1, -1]``.

    Parameters
    ----------
    x, y : np.ndarray
        Input time series, 1-d arrays of arbitrary size.

    Returns
    -------
    dist : float
        The distance between ``x`` and ``y``.
    """
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    if len(x) < len(y):
        # swap the order to allocate less memory
        x, y = y, x
    nx, ny = len(x), len(y)
    dist = cdtwlib.dtw_dist(x, y, nx, ny)
    return dist


def dtw_path(cost_mat):
    """
    Finds the best path (an array of x- and y-coordinates) to align ``x`` to
    ``y``, given the cost matrix ``cost_mat = dtw_mat(x, y)``.

    Parameters
    ----------
    cost_mat : (N, M) np.ndarray
        The output of the :func:`dtw_mat` function.

    Returns
    -------
    path : (L, 2) np.ndarray
        The path that aligns ``x`` to ``y`` in time.

    """
    nx, ny = cost_mat.shape
    cost_mat = np.ascontiguousarray(cost_mat.reshape(-1), dtype=np.float32)
    # the path length is at most 2(n + m)
    path = np.empty(2 * (nx + ny), dtype=np.int32)
    path_len = cdtwlib.dtw_path(path, cost_mat, nx, ny)
    path = path.reshape((-1, 2))[:path_len][::-1]
    return path


if __name__ == '__main__':
    from cdtw import dtw_mat, dtw_dist, dtw_path
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4]
    print(dtw_dist(x, y))
    cost = dtw_mat(x, y)
    print(dtw_path(cost).tolist())
