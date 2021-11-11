[![CircleCI](https://circleci.com/gh/dizcza/cdtw-python.svg?style=svg)](https://app.circleci.com/pipelines/github/dizcza/cdtw-python)
![](https://coveralls.io/repos/dizcza/cdtw-python/badge.png "Unit Test Coverage")
[![Documentation Status](https://readthedocs.org/projects/cdtw-python/badge/?version=latest)](https://cdtw-python.readthedocs.io/en/latest/?badge=latest)


# Dynamic Time Warping in C with Python bindings

The simplest (and perhaps the fastest) Dynamic Time Warping C implementation with Python bindings.

The behavior is equivalent to the [dtaidistance](https://github.com/wannesm/dtaidistance) package but with much simpler (basic) API and **X2 faster**.

## Installation

```
pip install -e git+https://github.com/dizcza/cdtw-python.git#egg=cdtw
```

## Documentation

https://cdtw-python.readthedocs.io/en/latest/


## Quick start

```python
>>> from cdtw import dtw_mat, dtw_dist, dtw_path
>>> x = [1, 2, 3, 4, 5]
>>> y = [2, 3, 4]

# total distance
>>> dtw_dist(x, y)
1.4142135381698608

# full distance (cost) matrix
>>> cost = dtw_mat(x, y)
>>> cost
array([[1.       , 2.236068 , 3.7416575],
       [1.       , 1.4142135, 2.4494898],
       [1.4142135, 1.       , 1.4142135],
       [2.4494898, 1.4142135, 1.       ],
       [3.8729835, 2.4494898, 1.4142135]], dtype=float32)

# best warp path
>>> dtw_path(cost).tolist()
[[0, 0], [1, 0], [2, 1], [3, 2], [4, 2]]
```

## Benchmarking

```python
>>> import dtaidistance
>>> import numpy as np
>>> import cdtw
>>> np.random.seed(0)
>>> x = np.random.randn(5_000)
>>> y = np.random.randn(10_000)

>>> %timeit cdtw.dtw_dist(x, y)
157 ms ± 218 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

>>> %timeit dtaidistance.dtw.distance_fast(x, y)
296 ms ± 2.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit cdtw.dtw_mat(x, y)
404 ms ± 37 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit dtaidistance.dtw.warping_paths_fast(x, y)
991 ms ± 47.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

The *cdtw* package converts everything to the `float` data type (if needed) while *dtaidistance* requires `double`. The *cdtw* compiled with the `double` precision is X1.5 faster than *dtaidistance*.
