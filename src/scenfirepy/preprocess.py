import pandas as pd


def validate_fire_dataframe(df):
    """
    Validate basic structure of a fire-event DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        raise ValueError("DataFrame is empty")

    return df


def compute_fire_size(df, area_column):
    """
    Ensure a fire-size column exists and is numeric.
    """
    if area_column not in df.columns:
        raise KeyError(f"Missing required column: {area_column}")

    df = df.copy()

    df[area_column] = pd.to_numeric(df[area_column], errors="coerce")

    if df[area_column].isna().all():
        raise ValueError("Fire size column contains no valid numeric values")

    return df
