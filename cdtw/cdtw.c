/**
 * Dynamic Time Warping in C.
 *
 * Only Euclidean distance metric is available.
 *
 * Author: Danylo Ulianych
 */

#include <stdint.h>
#include <math.h>
#include <stdlib.h>


/**
 * Returns the minimum of three values.
 */
inline float min3(float a, float b, float c) {
    float m = a;
    if (m > b) m = b;
    if (m > c) m = c;
    return m;
}


/**
 * Computes the full cost (distance) matrix `cost_mat` given 1-d time series `x` and `y`.
 */
void dtw_mat(float *cost_mat, const float *x, const float *y, int32_t nx, int32_t ny) {
    int32_t i, j;
    const int32_t ncol = ny + 1;
    float cost;

    for (j = 1; j <= ny; j++) {
        cost_mat[j] = INFINITY;
    }
    cost_mat[0] = 0;

    for (i = 1; i <= nx; i++) {
        cost_mat[i * ncol] = INFINITY;
        for (j = 1; j <= ny; j++) {
            cost = pow(x[i - 1] - y[j - 1], 2);
            cost_mat[i * ncol + j] = cost + min3(cost_mat[(i - 1) * ncol + j],        // insertion
                                                 cost_mat[i * ncol + j - 1],          // deletion
                                                 cost_mat[(i - 1) * ncol + j - 1]);   // match
        }
    }
}


/**
 * Computes the DTW distance between 1-d time series `x` and `y`
 *  using dynamic programming. It's equivalent but more efficient to
 *  calling `dtw_mat(x, y)` and retrieving the last row and column.
 */
float dtw_dist(const float *x, const float *y, int32_t nx, int32_t ny) {
    int32_t i, j, k;
    const int32_t ncol = ny + 2;
    float cost;

    float *cost_mat = malloc(ncol * sizeof(float));
    int32_t *next = malloc(ncol * sizeof(int32_t));
    int32_t *prev = malloc(ncol * sizeof(int32_t));
    for (j = 0; j < ncol; j++) {
        cost_mat[j] = INFINITY;
        next[j] = j + 1;
        prev[j] = j - 1;
    }
    cost_mat[1] = 0;
    next[ncol - 1] = 0;
    prev[0] = ncol - 1;
    k = 1;
    for (i = 1; i <= nx; i++) {
        k = (2 - i) % ncol;
        if (k < 0) k += ncol;
        for (j = 1; j <= ny; j++) {
            cost = pow(x[i - 1] - y[j - 1], 2);
            cost_mat[k] = cost + min3(cost_mat[next[k]],   // insertion
                                      cost_mat[prev[k]],   // deletion
                                      cost_mat[k]);        // match
            k = next[k];
        }
        cost_mat[k] = INFINITY;
    }

    k = prev[k];
    float dist = sqrt(cost_mat[k]);

    free(cost_mat);
    free(next);
    free(prev);

    return dist;
}


/**
 * Finds the best warping `path` (an array of x- and y-coordinates) to align input
 *  time series `x` to `y` given the cost matrix `cost_mat` obtained from the
 *  `dtw_mat` function.
 * The resulting warping path must be reversed.
 * Returns the path length.
 *
 * Adapted from https://www.audiolabs-erlangen.de/resources/MIR/FMP/C3/C3S2_DTWbasic.html
 */
int32_t dtw_path(int32_t *path, const float *cost_mat, int32_t nx, int32_t ny) {
    int32_t n, m;
    float diag, down, left;

    n = nx - 1;
    m = ny - 1;

    int32_t *p_path = path;

    while (n > 0 || m > 0) {
        *p_path++ = n;
        *p_path++ = m;
        if (n == 0) {
            m--;
        } else if (m == 0) {
            n--;
        } else {
            diag = cost_mat[(n - 1) * ny + m - 1];
            down = cost_mat[(n - 1) * ny + m];
            left = cost_mat[n * ny + m - 1];
            if (diag < down && diag < left) {
                n--;
                m--;
            } else if (down < diag && down < left) {
                n--;
            } else {
                m--;
            }
        }
    }
    *p_path++ = 0;
    *p_path++ = 0;

    int32_t path_len = (p_path - path) / 2;

    return path_len;
}
