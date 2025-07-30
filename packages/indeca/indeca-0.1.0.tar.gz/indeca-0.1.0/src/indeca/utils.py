import itertools as itt

import numpy as np


def norm(a):
    amin, amax = np.nanmin(a), np.nanmax(a)
    diff = amax - amin
    if diff > 0:
        return (a - amin) / diff
    else:
        return a - amin


def scal_lstsq(a, b, fit_intercept=False):
    if a.ndim == 1:
        a = a.reshape((-1, 1))
    if fit_intercept:
        a = np.concatenate([a, np.ones_like(a)], axis=1)
    return np.linalg.lstsq(a, b.squeeze(), rcond=None)[0]


def scal_like(src: np.ndarray, tgt: np.ndarray, zero_center=True):
    smin, smax = np.nanmin(src), np.nanmax(src)
    tmin, tmax = np.nanmin(tgt), np.nanmax(tgt)
    if zero_center:
        return src / (smax - smin) * (tmax - tmin)
    else:
        return (src - smin) / (smax - smin) * (tmax - tmin) + tmin


def enumerated_product(*args):
    yield from zip(itt.product(*(range(len(x)) for x in args)), itt.product(*args))
