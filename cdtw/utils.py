import ctypes
import re
import warnings
from pathlib import Path

import numpy as np


def load_cdll():
    libdir = Path(__file__).parent.parent / 'lib'
    libpath = None
    for fpath in libdir.iterdir():
        if re.match("cdtw\.cpython.*\.so", fpath.name):
            libpath = fpath
            break
    if libpath is None:
        # to be run on readthedocs
        warnings.warn("Could not find the compiled library")
        return None
    cdll = ctypes.CDLL(str(libpath))

    # dtw_dist function
    cdll.dtw_dist.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        ctypes.c_int32, ctypes.c_int32
    ]
    cdll.dtw_dist.restype = ctypes.c_float

    # dtw_mat function
    cdll.dtw_mat.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        ctypes.c_int32, ctypes.c_int32
    ]
    cdll.dtw_mat.restype = ctypes.c_void_p

    # dtw_path function
    cdll.dtw_path.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.int32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        ctypes.c_int32, ctypes.c_int32
    ]
    cdll.dtw_path.restype = ctypes.c_int32
    return cdll


cdtwlib = load_cdll()
