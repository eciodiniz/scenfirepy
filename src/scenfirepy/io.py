from pathlib import Path
import pandas as pd


def read_flp20_csv(csv_path):
    """
    Read FLP20 (FConstMTT) CSV output and return a pandas DataFrame.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise RuntimeError(f"Failed to read FLP20 CSV: {e}")

    if df.empty:
        raise ValueError("FLP20 CSV is empty")

    return df
