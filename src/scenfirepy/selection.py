import numpy as np

from .distribution import (
    build_target_hist,
    calculate_discrepancy,
    fit_powerlaw,
)


def select_events(
    sizes,
    event_surfaces,
    xmin,
    alpha,
    num_bins=20,
    logaritmic=True,
    max_iter=1000,
    tol=1e-6,
    seed=None,
):
    """
    Literal implementation of SCENFIRE R::select_events (from Rd).

    Iteratively generates candidate event surfaces from a power-law,
    compares their histogram to the target histogram, and keeps the
    best (lowest discrepancy).
    """

    rng = np.random.default_rng(seed)

    sizes = np.asarray(sizes, dtype=float)
    event_surfaces = np.asarray(event_surfaces, dtype=float)

    sizes = sizes[sizes > 0]
    event_surfaces = event_surfaces[event_surfaces > 0]

    if sizes.size == 0 or event_surfaces.size == 0:
        raise ValueError("sizes and event_surfaces must contain positive values")

    # Target histogram (fixed)
    target = build_target_hist(
        sizes=sizes,
        event_surfaces=event_surfaces,
        num_bins=num_bins,
        logaritmic=logaritmic,
    )

    best_disc = np.inf
    best_events = None

    for _ in range(max_iter):
        # Generate candidate events from power-law
        candidate = fit_powerlaw(
            xmin=xmin,
            alpha=alpha,
            n=event_surfaces.size,
            seed=rng.integers(0, 2**32 - 1),
        )

        # Histogram of candidate using SAME bins
        if logaritmic:
            eps = 1e-6
            candidate_tr = np.log(candidate + eps)
        else:
            candidate_tr = candidate

        sim_hist, _ = np.histogram(
            candidate_tr,
            bins=target["bins"],
            density=True,
        )

        disc = calculate_discrepancy(
            target_hist=target["target_hist"],
            simulated_hist=sim_hist,
        )

        if disc < best_disc:
            best_disc = disc
            best_events = candidate

        if best_disc <= tol:
            break

    if best_events is None:
        raise RuntimeError("No valid event set found")

    return {
        "events": best_events,
        "discrepancy": best_disc,
    }
