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
