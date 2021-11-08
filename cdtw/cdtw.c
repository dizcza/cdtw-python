#include <stdint.h>
#include <math.h>


inline float min3(float a, float b, float c) {
    float m = a;
    if (m < b) m = b;
    if (m < c) m = c;
    return m;
}


void dtw(float *res, float *x, float *y, int32_t nx, int32_t ny) {
    int32_t i, j;
    float cost;

    for (i = 0; i < nx; i++) {
        for (j = 0; j < ny; j++) {
            res[i * ny + j] = 0;
        }
    }
    
    for (i = 1; i < nx; i++) {
        for (j = 1; j < ny; j++) {
            cost = pow(x[i] - y[i], 2);
            res[i * ny + j] = cost + min3(res[(i - 1) * ny + j], res[i * ny + j - 1], res[(i - 1) * ny + j - 1]);
        }
    }
}

