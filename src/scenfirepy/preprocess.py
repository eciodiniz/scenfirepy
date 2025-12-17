import numpy as np


def check_fire_data(x):
    """
    Literal implementation of SCENFIRE R::check_fire_data (from Rd).

    Validates fire size data:
    - numeric
    - finite
    - positive
    - non-empty

    Returns cleaned numeric array.
    """

    if x is None:
        raise ValueError("Input fire data is None")

    x = np.asarray(x, dtype=float)

    if x.size == 0:
        raise ValueError("Input fire data is empty")

    if not np.all(np.isfinite(x)):
        raise ValueError("Input fire data contains non-finite values")

    if not np.all(x > 0):
        raise ValueError("Input fire data must contain only positive values")

    return x
