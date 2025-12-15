import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin


def rasterize_geometries(gdf, value=1, resolution=30, nodata=0):
    """
    Rasterize geometries from a GeoDataFrame.
    """
    if gdf.crs is None:
        raise ValueError("GeoDataFrame must have a CRS defined")

    bounds = gdf.total_bounds
    minx, miny, maxx, maxy = bounds

    width = int(np.ceil((maxx - minx) / resolution))
    height = int(np.ceil((maxy - miny) / resolution))

    if width <= 0 or height <= 0:
        raise ValueError("Invalid raster dimensions")

    transform = from_origin(minx, maxy, resolution, resolution)

    shapes = ((geom, value) for geom in gdf.geometry)

    raster = rasterize(
        shapes=shapes,
        out_shape=(height, width),
        fill=nodata,
        transform=transform,
        dtype="float32"
    )

    return raster, transform, gdf.crs
