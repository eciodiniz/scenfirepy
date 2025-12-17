import numpy as np
import pandas as pd


def flp20_to_bp_df(flp20_df, burn_probability):
    """
    Literal port of SCENFIRE R::flp20_to_bp_df()

    Parameters
    ----------
    flp20_df : pandas.DataFrame
        Output of flp20_to_df(), containing at least a 'fire_id' column.
    burn_probability : array-like
        Burn probability values corresponding to each fire_id.

    Returns
    -------
    pandas.DataFrame
        Input DataFrame with an added 'burn_probability' column.
    """

    if not isinstance(flp20_df, pd.DataFrame):
        raise TypeError("flp20_df must be a pandas DataFrame")

    if "fire_id" not in flp20_df.columns:
        raise ValueError("flp20_df must contain a 'fire_id' column")

    burn_probability = np.asarray(burn_probability, dtype=float)

    if burn_probability.ndim != 1:
        raise ValueError("burn_probability must be a 1D array")

    if burn_probability.size != flp20_df.shape[0]:
        raise ValueError(
            "burn_probability length must match number of rows in flp20_df"
        )

    df = flp20_df.copy()
    df["burn_probability"] = burn_probability

    return df
