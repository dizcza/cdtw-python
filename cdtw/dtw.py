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
    res = np.zeros((nx + 1) * (ny + 1), dtype=np.float32)
    cdtwlib.dtw_mat(res, x, y, nx, ny)
    res = res.reshape((nx + 1, ny + 1))
    return res


def dtw_dist(x, y):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    nx, ny = len(x), len(y)
    dist = cdtwlib.dtw_dist(x, y, nx, ny)
    return dist


def dtw_path(cost_mat):
    nx, ny = cost_mat.shape
    cost_mat = np.ascontiguousarray(cost_mat.reshape(-1), dtype=np.float32)
    path_alloc = np.empty(nx + ny, dtype=np.int32)
    path_len = cdtwlib.dtw_path(path_alloc, cost_mat, nx, ny)
    path_alloc = path_alloc[:path_len][::-1]
    return path_alloc


if __name__ == '__main__':
    import time
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4]
    # np.random.seed(0)
    # x = np.random.randn(10_000).astype(np.float32)
    # y = np.random.randn(20_000).astype(np.float32)
    start = time.time()
    cost = dtw_mat(x, y)
    duration = time.time() - start
    print(f"{duration=:.3f} s")
    print(cost)
