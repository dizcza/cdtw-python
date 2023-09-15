Dynamic Time Warping in C
=========================

The simplest Dynamic Time Warping C implementation with Python bindings.

The behavior is equivalent to the `dtaidistance <https://github.com/wannesm/dtaidistance>`_ package but with much simpler (basic) API and **X2 faster**.


Installation
------------

``pip install -e git+https://github.com/dizcza/cdtw-python.git#egg=cdtw``


.. automodule:: cdtw.dtw


.. code-block:: python

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


Tutorial
--------

.. nbgallery::
   Tutorial
