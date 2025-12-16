import numpy as np


def build_target_hist(
    sizes,
    event_surfaces,
    num_bins=20,
    logaritmic=True
):
    """
    Literal port of SCENFIRE R::build_target_hist()
    """

    sizes = np.asarray(sizes, dtype=float)
    event_surfaces = np.asarray(event_surfaces, dtype=float)

    if sizes.size == 0 or event_surfaces.size == 0:
        raise ValueError("sizes and event_surfaces must not be empty")

    eps = 1e-6

    if logaritmic:
        sizes_tr = np.log(sizes + eps)
        events_tr = np.log(event_surfaces + eps)
    else:
        sizes_tr = sizes
        events_tr = event_surfaces

    all_vals = np.concatenate([sizes_tr, events_tr])

    bins = np.linspace(
        np.min(all_vals),
        np.max(all_vals),
        num_bins + 1
    )

    target_hist, _ = np.histogram(
        sizes_tr,
        bins=bins,
        density=True
    )

    return {
        "target_hist": target_hist,
        "bins": bins
    }


def calculate_discrepancy(target_hist, simulated_hist):
    """
    Literal port of SCENFIRE R::calculate_discrepancy()
    """

    target_hist = np.asarray(target_hist, dtype=float)
    simulated_hist = np.asarray(simulated_hist, dtype=float)

    if target_hist.shape != simulated_hist.shape:
        raise ValueError("target_hist and simulated_hist must have same length")

    mask = target_hist > 0

    if not np.any(mask):
        raise ValueError("target_hist contains no positive values")

    discrepancy = np.sum(
        np.abs(simulated_hist[mask] - target_hist[mask]) / target_hist[mask]
    )

    return discrepancy
