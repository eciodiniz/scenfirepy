import numpy as np

def build_target_hist(x, breaks):
    """
    Literal port of R build_target_hist():
    hist(x, breaks=breaks, plot=FALSE, density=TRUE)
    """

    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    x = x[x > 0]

    if x.size == 0:
        raise ValueError("Input vector 'x' must contain positive values")

    density, breaks = np.histogram(x, bins=breaks, density=True)

    mids = (breaks[:-1] + breaks[1:]) / 2.0

    return {
        "density": density,
        "breaks": breaks,
        "mids": mids
    }
