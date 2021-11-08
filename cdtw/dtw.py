import numpy as np

from cdtw.utils import cdtwlib


def dtw(x, y):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    nx, ny = len(x), len(y)
    res = np.empty(nx * ny, dtype=np.float32)
    cdtwlib.dtw(res, x, y, nx, ny)
    res = res.reshape((nx, ny))
    return res


if __name__ == '__main__':
    x = [1, 2, 3, 4]
    y = [1, 2, 5]
    print(dtw(x, y))
