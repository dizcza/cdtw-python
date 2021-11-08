import numpy as np

from cdtw.utils import cdtwlib


__all__ = [
    "dtw_dist",
    "dtw_mat",
    "dtw_path"
]


def dtw_mat(x, y):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    nx, ny = len(x), len(y)
    cost_mat = np.zeros((nx + 1) * (ny + 1), dtype=np.float32)
    cdtwlib.dtw_mat(cost_mat, x, y, nx, ny)
    cost_mat = cost_mat.reshape((nx + 1, ny + 1))
    cost_mat = np.sqrt(cost_mat)
    # the first row & col are inf
    return cost_mat[1:, 1:]


def dtw_dist(x, y):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    nx, ny = len(x), len(y)
    dist = cdtwlib.dtw_dist(x, y, nx, ny)
    return dist


def dtw_path(cost_mat):
    nx, ny = cost_mat.shape
    cost_mat = np.ascontiguousarray(cost_mat.reshape(-1), dtype=np.float32)
    path_alloc = np.empty((nx + ny) * 2, dtype=np.int32)
    path_len = cdtwlib.dtw_path(path_alloc, cost_mat, nx, ny)
    path_alloc = path_alloc.reshape((-1, 2))[:path_len][::-1]
    return path_alloc


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4]
    print(dtw_dist(x, y))
    cost = dtw_mat(x, y)
    print(dtw_path(cost).tolist())
