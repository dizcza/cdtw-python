import itertools
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import squareform

import cdtw

__all__ = [
    "distmat_from_timeseries",
    "dtw_warped_mean",
    "dtw_plot_clustering"
]


def distmat_from_timeseries(data, dist_func=cdtw.dtw_dist):
    """
    Compute a square distance matrix given samples.

    Parameters
    ----------
    data: (N, M) np.ndarray
        `N` samples of `M`-dimensional vectors.
    dist_func: callable
        A function to compute pairwise distance.
        Default: `dtw_dist`.

    Returns
    -------
    np.ndarray
        `(N, N)` square pairwise distance matrix.
    """
    with Pool(processes=None) as pool:
        dist = pool.starmap(dist_func, itertools.combinations(data, 2))
    return squareform(dist)


def dtw_warped_mean(data, dist_func=cdtw.dtw_dist):
    """
    Compute the `data` samples mean warped with DTW.

    Parameters
    ----------
    data: (N, M) np.ndarray
        `N` samples of `M`-dimensional vectors to compute the mean from.
    dist_func: callable
        A function to compute pairwise distance.
        Default: `dtw_dist`.

    Returns
    -------
    np.ndarray
        Mean sample array of shape `M`.
    """
    dist_mat = distmat_from_timeseries(data, dist_func=dist_func)
    dist_mat = np.sort(dist_mat, axis=1)
    winner = dist_mat.mean(axis=1).argmin()
    segment_best = data[winner]
    segment_aver = np.zeros_like(segment_best)

    for i in range(len(data)):
        dp_seg = data[i]
        mat = cdtw.dtw_mat(dp_seg, segment_best)
        path = cdtw.dtw_path(mat)
        ii, jj = path.T
        segment_aver[jj] += dp_seg[ii]
    segment_aver /= len(data)

    return segment_aver


def dtw_plot_clustering(data, dist_mat=None, plot_best=True, plot_aver=True):
    """
    Plot the result of DTW clustering.

    Parameters
    ----------
    data: (N, M) np.ndarray
        `N` samples of `M`-dimensional vectors.
        It's assumed that all samples in the `data` belong to the same category / class.
    dist_mat: (N, N) np.ndarray or None
        Precomputed square dist matrix.
    plot_best: bool
        Plot the best single match.
    plot_aver: bool
        Plot the warped mean.

    Returns
    -------
    ax
        Matplotlib axis.
    """
    fig, ax = plt.subplots()
    if data.shape[0] == 1:
        ax.plot(data[0])
        return ax

    if dist_mat is None:
        dist_mat = distmat_from_timeseries(data)
    dist_mat = np.sort(dist_mat, axis=1)
    winner = dist_mat.mean(axis=1).argmin()
    segment_best = data[winner]
    segment_aver = np.zeros_like(segment_best)

    for i, dp_seg in enumerate(data):
        mat = cdtw.dtw_mat(dp_seg, segment_best)
        path = cdtw.dtw_path(mat)
        ii, jj = path.T
        segment_aver[jj] += dp_seg[ii]
        ax.plot(jj, dp_seg[ii], lw=0.75, color='gray', alpha=0.6)
    segment_aver /= len(data)
    if plot_best:
        ax.plot(segment_best, label='best')
    if plot_aver:
        ax.plot(segment_aver, label='aver')
    ax.legend()
    return ax
