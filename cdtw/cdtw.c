#include <stdint.h>
#include <math.h>


inline float min3(float a, float b, float c) {
    float m = a;
    if (m > b) m = b;
    if (m > c) m = c;
    return m;
}


inline int32_t int32_mod(int32_t a, int32_t b) {
	int32_t mod = a % b;
	if (mod < 0) {
		mod += b;
	}
	return mod;
}


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


float dtw_dist(const float *x, const float *y, int32_t nx, int32_t ny) {
    int32_t i, j, k;
    const int32_t ncol = ny + 2;
    float cost;

    float *cost_mat = malloc(ncol * sizeof(float));
    for (j = 0; j < ncol; j++) {
        cost_mat[j] = INFINITY;
    }
    cost_mat[1] = 0;
    for (i = 1; i <= nx; i++) {
        for (j = 1; j <= ny; j++) {
            k = int32_mod(j - i + 1, ncol);
            cost = pow(x[i - 1] - y[j - 1], 2);
            cost_mat[k] = cost + min3(cost_mat[int32_mod(k + 1, ncol)],   // insertion
                                      cost_mat[int32_mod(k - 1, ncol)],   // deletion
                                      cost_mat[k]);                       // match
        }
        cost_mat[int32_mod(k + 1, ncol)] = INFINITY;
    }

    float dist = sqrt(cost_mat[k]);

    free(cost_mat);

    return dist;
}


int32_t dtw_path(int32_t *path, const float *cost_mat, int32_t nx, int32_t ny) {
    // adapted from https://www.audiolabs-erlangen.de/resources/MIR/FMP/C3/C3S2_DTWbasic.html
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

    // the resulting path must be reversed
    return path_len;
}
