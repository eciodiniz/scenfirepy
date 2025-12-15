import numpy as np
import pandas as pd
import powerlaw


def fit_powerlaw_distribution(sizes, xmin=None):
    """
    Fit a truncated power-law distribution to fire sizes.
    """
    sizes = np.asarray(sizes)
    sizes = sizes[sizes > 0]

    if sizes.size == 0:
        raise ValueError("No positive fire sizes provided")

    fit = powerlaw.Fit(sizes, xmin=xmin, verbose=False)

    return {
        "alpha": fit.alpha,
        "xmin": fit.xmin,
        "sigma": fit.sigma,
        "fit": fit
    }


def build_target_histogram(sizes, bins):
    """
    Build target fire-size histogram.
    """
    sizes = np.asarray(sizes)

    if sizes.size == 0:
        raise ValueError("No fire sizes provided")

    if not isinstance(bins, (int, list, tuple, np.ndarray)):
        raise TypeError("bins must be an integer or a sequence of bin edges")

    hist, bin_edges = np.histogram(sizes, bins=bins)

    return pd.DataFrame({
        "bin_min": bin_edges[:-1],
        "bin_max": bin_edges[1:],
        "count": hist
    })
