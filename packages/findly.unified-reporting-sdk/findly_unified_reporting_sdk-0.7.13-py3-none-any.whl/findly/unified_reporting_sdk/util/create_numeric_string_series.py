import pandas as pd

DEFAULT_FLOAT_PRECISION = 2


def create_numeric_string_series(
    col: pd.Series, precision: int = DEFAULT_FLOAT_PRECISION
) -> pd.Series:
    try:
        numeric_col: pd.Series = pd.to_numeric(col)
        if (numeric_col.dropna() % 1 == 0).all():
            return numeric_col.astype(int).astype(str)
        else:
            return numeric_col.astype(float).round(precision).astype(str)
    except Exception:
        return col
