import numpy as np

def select_events(
    event_sizes,
    event_probabilities,
    target_hist,
    bins,
    reference_surface,
    surface_threshold,
    tolerance,
    iter_limit,
    max_it,
    seed=None
):
    """
    Python mirror of R scenfire::select_events

    Returns:
        dict with keys:
        - surface_index
        - discrepancy
        - total_surface
    """

    rng = np.random.default_rng(seed)

    event_sizes = np.asarray(event_sizes, dtype=float)
    event_probabilities = np.asarray(event_probabilities, dtype=float)

    best_idx = None
    best_disc = np.inf
    best_surface = 0.0

    n_events = event_sizes.size

    for _ in range(max_it):
        # sample candidate indices weighted by ignition probability
        idx = rng.choice(
            n_events,
            size=n_events,
            replace=False,
            p=event_probabilities / event_probabilities.sum()
        )

        cum_surface = np.cumsum(event_sizes[idx])
        valid = cum_surface <= surface_threshold

        if not np.any(valid):
            continue

        sel_idx = idx[valid]
        sel_sizes = event_sizes[sel_idx]

        hist, _ = np.histogram(sel_sizes, bins=bins, density=True)
        disc = np.sum(np.abs(hist - target_hist))

        if disc < best_disc and disc <= tolerance:
            best_disc = disc
            best_idx = sel_idx
            best_surface = sel_sizes.sum()

        if best_disc <= tolerance:
            break

    if best_idx is None:
        raise RuntimeError("No valid event selection found")

    return {
        "surface_index": best_idx,
        "discrepancy": best_disc,
        "total_surface": best_surface
    }
