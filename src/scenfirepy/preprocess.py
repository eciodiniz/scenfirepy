# put this in src/scenfirepy/preprocess.py, replacing the old check_fire_data
import numpy as np

def check_fire_data(fires_hist_size, sim_perimeters_size, n_years):
    """
    R-like check_fire_data(fires_hist_size, sim_perimeters_size, n_years)
    - Fires_hist_size : 1D array-like of historical fire sizes (same units as sim)
    - sim_perimeters_size : 1D array-like of simulated fire sizes
    - n_years : integer number of years represented in the historical sample

    Behavior:
      - Prints diagnostic messages if simulated data seem insufficient.
      - If sufficient, computes and returns a recommended surface threshold (int).
      - If insufficient, prints guidance and returns None.
    """
    fires = np.asarray(fires_hist_size, dtype=float)
    sims = np.asarray(sim_perimeters_size, dtype=float)

    if fires.size == 0:
        raise ValueError("fires_hist_size is empty")
    if sims.size == 0:
        raise ValueError("sim_perimeters_size is empty")
    if not (isinstance(n_years, (int, np.integer)) and n_years > 0):
        raise ValueError("n_years must be a positive integer")

    max_hist = np.nanmax(fires)
    total_hist = np.nansum(fires)

    max_sim = np.nanmax(sims)
    total_sim = np.nansum(sims)

    # Diagnostics (mirrors R logic sensibly)
    sufficient_max = (max_sim >= 0.9 * max_hist)
    simulated_avg_area_per_year = total_sim / float(n_years)
    sufficient_area = (simulated_avg_area_per_year >= total_hist * 0.9)

    if not sufficient_max:
        print("Insufficient simulated maximum fire size:")
        print(f"  max_hist = {max_hist:.3f}, max_sim = {max_sim:.3f}")
    if not sufficient_area:
        print("Insufficient simulated total burned area (per year):")
        print(f"  total_hist = {total_hist:.3f}, simulated_avg_area_per_year = {simulated_avg_area_per_year:.3f}")

    if not (sufficient_max and sufficient_area):
        print("Simulated data appear insufficient. Consider more/larger simulations.")
        return None

    # If sufficient: compute recommended threshold
    # Heuristic: maximum useful threshold is min(max_sim, simulated_avg_area_per_year)
    max_possible_threshold = min(max_sim, simulated_avg_area_per_year)
    recommended = int(max(1, round(0.10 * max_possible_threshold)))  # 10% rule like R doc
    print("Sufficient simulated perimeters and burned area.")
    print("Maximum surface threshold:", int(max_possible_threshold))
    print("Recommended surface threshold:", recommended)

    return recommended
