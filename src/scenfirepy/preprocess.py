import numpy as np

def check_fire_data(fires_hist_size, sim_perimeters_size, n_years):
    fires_hist_size = np.asarray(fires_hist_size, dtype=float)
    sim_perimeters_size = np.asarray(sim_perimeters_size, dtype=float)

    if fires_hist_size.size == 0 or sim_perimeters_size.size == 0:
        raise ValueError("Empty fire size vectors.")

    max_hist = fires_hist_size.max()
    max_sim = sim_perimeters_size.max()

    total_hist = fires_hist_size.sum()
    total_sim = sim_perimeters_size.sum()

    if max_sim < max_hist:
        print("Simulated fires too small.")
        return None

    if total_sim < total_hist:
        print("Insufficient total burned area.")
        return None

    max_surface_threshold = int(max_sim)
    recommended_surface_threshold = int(max_surface_threshold * 0.1)

    print("Sufficient simulated perimeters and burned area.")
    print("Maximum surface threshold:", max_surface_threshold)
    print("Recommended surface threshold:", recommended_surface_threshold)

    return recommended_surface_threshold
