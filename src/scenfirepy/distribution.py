# src/scenfirepy/distribution.py
import numpy as np

def build_target_hist(sizes, event_surfaces=None, num_bins=10, logaritmic=False):
    """
    Build a target histogram from historical sizes and (optional) event_surfaces.
    Robustly coerce num_bins to int and handle edge cases.
    """
    # coerce and sanitise num_bins
    try:
        num_bins = int(num_bins)
    except Exception:
        num_bins = 10
    if num_bins < 2:
        num_bins = 10

    # ensure arrays
    sizes = np.asarray(sizes, dtype=float)
    if event_surfaces is None:
        events_tr = sizes
    else:
        events_tr = np.asarray(event_surfaces, dtype=float)

    # check there's data
    if sizes.size == 0 and events_tr.size == 0:
        raise ValueError("No input values to build target histogram.")

    # combine to get bin edges (use all_vals so bins cover both)
    all_vals = np.concatenate([sizes, events_tr])
    if all_vals.size == 0:
        raise ValueError("No valid numeric values to compute bins.")

    # if all values are identical, create a small range
    vmin = np.nanmin(all_vals)
    vmax = np.nanmax(all_vals)
    if np.isclose(vmin, vmax):
        # create a tiny range around the value
        vmin = vmin * 0.999 if vmin != 0 else -0.0005
        vmax = vmax * 1.001 if vmax != 0 else 0.0005

    bins = np.linspace(vmin, vmax, num_bins + 1)

    # target histogram from sizes only (density)
    target_hist, _ = np.histogram(sizes, bins=bins, density=True)

    return {"target_hist": target_hist, "bins": bins}
