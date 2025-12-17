import numpy as np


def calc_burn_probability(selected_events, event_surfaces):
    """
    Literal port of SCENFIRE R::calc_burn_probability()

    Parameters
    ----------
    selected_events : array-like (int/bool)
        Indicator vector of selected fire events (1 = selected, 0 = not).
    event_surfaces : array-like (float)
        Burned surface/area associated with each event.

    Returns
    -------
    np.ndarray
        Burn probability per event surface unit.
    """

    selected_events = np.asarray(selected_events, dtype=float)
    event_surfaces = np.asarray(event_surfaces, dtype=float)

    if selected_events.shape != event_surfaces.shape:
        raise ValueError("selected_events and event_surfaces must have same length")

    if selected_events.size == 0:
        raise ValueError("Input vectors must be non-empty")

    if np.any(event_surfaces < 0):
        raise ValueError("event_surfaces must be non-negative")

    total_selected = np.sum(selected_events)

    if total_selected <= 0:
        raise ValueError("No selected events to compute burn probability")

    burn_probability = (selected_events * event_surfaces) / total_selected

    return burn_probability
