import numpy as np
import rasterio
from rasterio.enums import Resampling


def flp20_to_raster(
    reference_raster,
    burn_probability,
    output_path=None,
):
    """
    Literal port of SCENFIRE R::flp20_to_raster()

    Parameters
    ----------
    reference_raster : str | rasterio.io.DatasetReader
        FLP20 raster used as spatial reference (grid, transform, CRS).
    burn_probability : array-like
        Burn probability values aligned with FLP20 fire_id order.
    output_path : str | None
        If provided, writes GeoTIFF to this path. If None, returns array + profile.

    Returns
    -------
    If output_path is None:
        (np.ndarray, dict) -> (burn probability raster, raster profile)
    Else:
        str -> output_path
    """

    # Open raster
    if isinstance(reference_raster, str):
        src = rasterio.open(reference_raster)
        close_src = True
    else:
        src = reference_raster
        close_src = False

    try:
        data = src.read(1)
        profile = src.profile.copy()
    finally:
        if close_src:
            src.close()

    if data.ndim != 2:
        raise ValueError("reference_raster must be 2D")

    bp = np.asarray(burn_probability, dtype=float)

    # Mask fire cells (same rule used in flp20_to_df)
    mask = np.isfinite(data) & (data > 0)

    if bp.size != np.count_nonzero(mask):
        raise ValueError(
            "burn_probability length must match number of fire cells in raster"
        )

    # Create output raster
    out = np.zeros_like(data, dtype=float)
    out[mask] = bp

    profile.update(
        dtype="float32",
        count=1,
        nodata=0.0,
    )

    if output_path is not None:
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(out.astype("float32"), 1)
        return output_path

    return out, profile
