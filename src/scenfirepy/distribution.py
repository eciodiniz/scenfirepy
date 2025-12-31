import numpy as np

def build_target_hist(sizes, event_surfaces, num_bins=10):
    sizes = np.asarray(sizes, dtype=float)
    event_surfaces = np.asarray(event_surfaces, dtype=float)

    all_vals = np.concatenate([sizes, event_surfaces])
    vmin = all_vals[all_vals > 0].min()
    vmax = all_vals.max()

    bins = np.exp(
        np.linspace(np.log(vmin), np.log(vmax), int(num_bins) + 1)
    )

    target_hist, _ = np.histogram(
        sizes,
        bins=bins,
        density=True
    )

    return {
        "target_hist": target_hist,
        "bins": bins
    }

def calculate_discrepancy(hist, target_hist):
    return float(np.sum(np.abs(hist - target_hist)))
