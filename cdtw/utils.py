import ctypes
import re
from pathlib import Path
import numpy as np


def load_cdll():
    libdir = Path(__file__).parent.parent / 'lib'
    libpath = None
    for fpath in libdir.iterdir():
        if re.match("cdtw\.cpython.*\.so", fpath.name):
            libpath = fpath
            break
    cdll = ctypes.CDLL(str(libpath))
    cdll.dtw.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                               flags='C_CONTIGUOUS'),
    ]
    cdll.dtw.restype = ctypes.c_void_p
    return cdll


cdtwlib = load_cdll()
