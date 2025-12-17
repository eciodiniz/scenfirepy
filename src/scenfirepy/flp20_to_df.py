import numpy as np
import pandas as pd
import rasterio


def flp20_to_df(raster):
    """
    Literal port of SCENFIRE R::flp20_to_df()

    Parameters
    ----------
    raster : str | rasterio.io.DatasetReader
        Path to an FLP20 raster or an already-open rasterio dataset.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - row
        - col
        - fire_id
        - value
    """

    # Open raster if a path is provided
    if isinstance(raster, str):
        with rasterio.open(raster) as src:
            data = src.read(1)
    else:
        data = raster.read(1)

    if data.ndim != 2:
        raise ValueError("FLP20 raster must be 2D")

    data = np.asarray(data)

    # Mask invalid / non-fire cells (R behavior: remove NA / zero)
    mask = np.isfinite(data) & (data > 0)

    if not np.any(mask):
        raise ValueError("No valid fire events found in FLP20 raster")

    rows, cols = np.where(mask)
    values = data[mask]

    df = pd.DataFrame(
        {
            "row": rows,
            "col": cols,
            "fire_id": np.arange(1, len(values) + 1),
            "value": values,
        }
    )

    return df
