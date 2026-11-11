"""Load a CSV and split it into numeric and categorical columns."""
import pandas as pd


def load_csv(path, columns=None):
    """Read a CSV file. Optionally keep only the given columns."""
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{path} has no rows")
    if columns:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValueError(f"Columns not found: {', '.join(missing)}")
        df = df[columns]
    return df


def split_columns(df):
    """Return (numeric_columns, categorical_columns)."""
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in df.columns if c not in numeric]
    return numeric, categorical
