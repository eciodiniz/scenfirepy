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
):
    """
    Python mirror of scenfire::select_events
    """

    rng = np.random.default_rng()

    event_sizes = np.asarray(event_sizes, dtype=float)
    event_probabilities = np.asarray(event_probabilities, dtype=float)

    best_disc = np.inf
    best_idx = None

    for _ in range(max_it):
        selected = []
        acc_surface = 0.0

        for _ in range(iter_limit):
            i = rng.choice(len(event_sizes), p=event_probabilities / event_probabilities.sum())
            selected.append(i)
            acc_surface += event_sizes[i]

            if acc_surface >= surface_threshold:
                break

        sel_sizes = event_sizes[selected]
        hist, _ = np.histogram(sel_sizes, bins=bins, density=True)

        disc = np.sum(np.abs(hist - target_hist))

        if disc < best_disc:
            best_disc = disc
            best_idx = selected

        if best_disc <= tolerance:
            break

    return {
        "surface_index": np.array(best_idx, dtype=int),
        "events": event_sizes[best_idx],
        "discrepancy": float(best_disc),
    }
