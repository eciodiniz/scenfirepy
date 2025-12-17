from .preprocess import check_fire_data
from .params import get_select_params
from .selection import select_events


def create_distribution(
    sizes,
    event_surfaces,
    xmin,
    alpha,
    num_bins=20,
    logaritmic=True,
    max_iter=1000,
    tol=1e-6,
    seed=None,
):
    """
    Literal port of SCENFIRE R::create_distribution()

    Orchestrates validation, parameter setup, and event selection.
    """

    # Validate inputs (R::check_fire_data)
    sizes = check_fire_data(sizes)
    event_surfaces = check_fire_data(event_surfaces)

    # Collect and validate parameters (R::get_select_params)
    params = get_select_params(
        xmin=xmin,
        alpha=alpha,
        num_bins=num_bins,
        logaritmic=logaritmic,
        max_iter=max_iter,
        tol=tol,
        seed=seed,
    )

    # Select events (R::select_events)
    result = select_events(
        sizes=sizes,
        event_surfaces=event_surfaces,
        xmin=params["xmin"],
        alpha=params["alpha"],
        num_bins=params["num_bins"],
        logaritmic=params["logaritmic"],
        max_iter=params["max_iter"],
        tol=params["tol"],
        seed=params["seed"],
    )

    return result
