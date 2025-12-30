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
    seed=None,
):
    """
    Faithful mirror of R scenfire::select_events

    - selects REAL simulated events (indices)
    - weighted by event_probabilities
    - enforces surface_threshold
    - minimizes histogram discrepancy vs target_hist
    """

    rng = np.random.default_rng(seed)

    event_sizes = np.asarray(event_sizes, dtype=float)
    event_probabilities = np.asarray(event_probabilities, dtype=float)

    # safety
    event_probabilities = np.nan_to_num(event_probabilities, nan=0.0)
    if event_probabilities.sum() == 0:
        raise ValueError("All event probabilities are zero")

    # normalize probabilities (R does this implicitly)
    probs = event_probabilities / event_probabilities.sum()

    best_disc = np.inf
    best_idx = None
    best_surface = None

    n_events = event_sizes.size

    for _ in range(max_it):

        selected_idx = []
        total_surface = 0.0

        # sample events WITHOUT replacement, weighted by probabilities
        order = rng.choice(
            np.arange(n_events),
            size=n_events,
            replace=False,
            p=probs,
        )

        for i in order:
            s = event_sizes[i]

            if total_surface + s > surface_threshold:
                break

            selected_idx.append(i)
            total_surface += s

            # R: stop early if we are close enough
            if abs(total_surface - reference_surface) / reference_surface <= tolerance:
                break

        if len(selected_idx) == 0:
            continue

        selected_sizes = event_sizes[selected_idx]

        # histogram of selected events using SAME bins
        sel_hist, _ = np.histogram(
            selected_sizes,
            bins=bins,
            density=True
        )

        # discrepancy = L1 distance (same spirit as R)
        disc = np.sum(np.abs(sel_hist - target_hist))

        if disc < best_disc:
            best_disc = disc
            best_idx = np.array(selected_idx, dtype=int)
            best_surface = total_surface

        # R: stop if good enough
        if best_disc <= tolerance:
            break

    if best_idx is None:
        raise RuntimeError("No valid selection found")

    return {
        "surface_index": best_idx,
        "total_surface": best_surface,
        "discrepancy": best_disc,
    }
