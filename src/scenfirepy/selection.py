# src/scenfirepy/selection.py
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
    Mirror of scenfire::select_events (keyword-based call style).

    Parameters
    ----------
    event_sizes : array-like  (simulated event areas)
    event_probabilities : array-like (per-event sampling weights, >=0)
    target_hist : array-like (target histogram density)
    bins : array-like (bin edges for histogram, length = len(target_hist)+1)
    reference_surface : float (not used directly here but kept for API parity)
    surface_threshold : float (stop selection when accumulated surface >= this)
    tolerance : float (early stop when discrepancy <= tolerance)
    iter_limit : int (max number of picks per attempt to reach threshold)
    max_it : int (number of independent attempts / outer loops)
    seed : int | None (rng seed)

    Returns
    -------
    dict with keys:
      - "surface_index": numpy int array of selected event indices (best)
      - "events": numpy array of selected event sizes
      - "discrepancy": float (best discrepancy)
      - "total_surface": float (sum sizes of selected events)
    """
    rng = np.random.default_rng(seed)

    sizes = np.asarray(event_sizes, dtype=float)
    probs = np.asarray(event_probabilities, dtype=float)
    target_hist = np.asarray(target_hist, dtype=float)
    bins = np.asarray(bins, dtype=float)

    if sizes.size == 0:
        raise ValueError("No event_sizes provided.")
    n = sizes.size

    # sanitize probabilities
    probs = np.nan_to_num(probs, nan=0.0)
    if probs.sum() <= 0:
        probs = np.ones_like(probs, dtype=float)
    probs = probs.astype(float)
    probs = probs / probs.sum()

    # Ensure bins/target_hist compatibility
    if bins.size != target_hist.size + 1:
        raise ValueError("bins length must be len(target_hist) + 1")

    best_disc = np.inf
    best_idx = None
    best_total = 0.0

    # Precompute indices array for speed
    all_idx = np.arange(n, dtype=int)

    for attempt in range(int(max_it)):
        acc_surface = 0.0
        selected = []
        picks = 0

        # We will try to sample without replacement while possible
        available_mask = np.ones(n, dtype=bool)
        # local copy of probabilities (we will renormalize over available)
        local_probs = probs.copy()

        while acc_surface < surface_threshold and picks < iter_limit:
            # available indices
            available_idx = all_idx[available_mask]
            if available_idx.size == 0:
                # no more available events: break
                break

            # renormalize probabilities over available
            p_av = local_probs[available_idx]
            s = p_av.sum()
            if s <= 0:
                # fallback to uniform on available
                p_choice = None
            else:
                p_choice = p_av / s

            # choose one index (without replacement)
            # note: rng.choice with replace=False ensures unique picks in this attempt
            choice = rng.choice(available_idx, size=1, replace=False, p=p_choice)
            idx = int(choice[0])
            selected.append(idx)
            acc_surface += sizes[idx]
            picks += 1

            # mark as unavailable to avoid reselecting same perimeter in this attempt
            available_mask[idx] = False

        # compute histogram (density) with same bins
        if len(selected) == 0:
            hist = np.zeros_like(target_hist)
        else:
            sel_sizes = sizes[np.array(selected, dtype=int)]
            hist, _ = np.histogram(sel_sizes, bins=bins, density=True)

        # discrepancy (L1)
        disc = float(np.sum(np.abs(hist - target_hist)))

        # update best
        if disc < best_disc:
            best_disc = disc
            best_idx = np.array(selected, dtype=int)
            best_total = float(np.sum(sizes[best_idx]))

        # early exit
        if best_disc <= tolerance:
            break

    # final packaging
    if best_idx is None:
        best_idx = np.array([], dtype=int)
        best_events = np.array([], dtype=float)
    else:
        best_events = sizes[best_idx]

    return {
        "surface_index": best_idx,
        "events": best_events,
        "discrepancy": float(best_disc),
        "total_surface": float(best_total),
    }
