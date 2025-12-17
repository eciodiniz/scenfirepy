def get_select_params(
    xmin,
    alpha,
    num_bins=20,
    logaritmic=True,
    max_iter=1000,
    tol=1e-6,
    seed=None,
):
    """
    Literal implementation of SCENFIRE R::get_select_params (from Rd).

    Collects and validates parameters for select_events.
    Returns a dictionary of validated parameters.
    """

    if xmin is None or xmin <= 0:
        raise ValueError("xmin must be a positive number")

    if alpha is None or alpha <= 1:
        raise ValueError("alpha must be > 1")

    if num_bins <= 0:
        raise ValueError("num_bins must be positive")

    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    if tol <= 0:
        raise ValueError("tol must be positive")

    return {
        "xmin": xmin,
        "alpha": alpha,
        "num_bins": num_bins,
        "logaritmic": bool(logaritmic),
        "max_iter": max_iter,
        "tol": tol,
        "seed": seed,
    }
