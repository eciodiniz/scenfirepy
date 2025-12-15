import matplotlib.pyplot as plt


def plot_fire_size_distribution(target_hist, selected_hist=None):
    """
    Plot target (and optionally selected) fire-size distributions.
    """
    if "count" not in target_hist.columns:
        raise KeyError("target_hist must contain 'count' column")

    if selected_hist is not None:
        if "count" not in selected_hist.columns:
            raise KeyError("selected_hist must contain 'count' column")
        if len(target_hist) != len(selected_hist):
            raise ValueError("target_hist and selected_hist must have the same number of bins")

    x = range(len(target_hist))

    plt.figure()
    plt.bar(x, target_hist["count"], alpha=0.6, label="Target")

    if selected_hist is not None:
        plt.bar(x, selected_hist["count"], alpha=0.6, label="Selected")

    plt.xlabel("Fire-size bin")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.show()
