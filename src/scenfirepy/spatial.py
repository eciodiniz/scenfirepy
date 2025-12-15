import geopandas as gpd


def validate_geodataframe(gdf, drop_invalid=False):
    """
    Validate a GeoDataFrame and its geometry.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
    drop_invalid : bool
        If True, invalid geometries are dropped.
        If False, an error is raised if invalid geometries exist.
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame")

    if gdf.empty:
        raise ValueError("GeoDataFrame is empty")

    if gdf.geometry.isna().any():
        raise ValueError("Geometry column contains missing values")

    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS defined")

    if not gdf.is_valid.all():
        if drop_invalid:
            gdf = gdf[gdf.is_valid]
            if gdf.empty:
                raise ValueError("All geometries are invalid")
        else:
            raise ValueError("Invalid geometries found; fix or set drop_invalid=True")

    return gdf.reset_index(drop=True)
