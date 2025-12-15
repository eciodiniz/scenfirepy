import numpy as np
import pandas as pd


def calculate_discrepancy(target_hist, selected_hist):
    """
    Calculate discrepancy between target and selected histograms.
    """
    required = ["bin_min", "bin_max", "count"]

    for col in required:
        if col not in target_hist.columns or col not in selected_hist.columns:
            raise KeyError("Histograms must contain bin_min, bin_max, and count columns")

    if len(target_hist) != len(selected_hist):
        raise ValueError("Target and selected histograms must have the same number of bins")

    return np.sum(
        np.abs(
            target_hist["count"].to_numpy() -
            selected_hist["count"].to_numpy()
        )
    )


def select_events(df, size_column, target_hist, random_state=None):
    """
    Select events to match target fire-size histogram.
    """
    if size_column not in df.columns:
        raise KeyError(f"Missing size column: {size_column}")

    required = ["bin_min", "bin_max", "count"]
    for col in required:
        if col not in target_hist.columns:
            raise KeyError(f"target_hist missing column: {col}")

    rng = np.random.default_rng(random_state)
    df = df.copy()

    selected_indices = set()

    for _, row in target_hist.iterrows():
        bin_min = row["bin_min"]
        bin_max = row["bin_max"]
        n_select = int(row["count"])

        if n_select <= 0:
            continue

        candidates = df[
            (df[size_column] >= bin_min) &
            (df[size_column] < bin_max) &
            (~df.index.isin(selected_indices))
        ]

        if candidates.empty:
            continue

        chosen = rng.choice(
            candidates.index,
            size=min(n_select, len(candidates)),
            replace=False
        )

        selected_indices.update(chosen)

    if not selected_indices:
        raise ValueError("No events were selected; check target histogram and data")

    return df.loc[list(selected_indices)].reset_index(drop=True)
