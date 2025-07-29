import numpy as np


def int16_to_float(x: np.ndarray) -> np.ndarray:
    """Convert an int16 array to a floating point array with range +/- 1"""
    return x.astype(np.float32) / 32768


def float_to_int16(x: np.ndarray) -> np.ndarray:
    """Convert a floating point array with range +/- 1 to an int16 array"""
    return (x * 32768).astype(np.int16)
