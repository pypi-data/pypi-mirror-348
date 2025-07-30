import pandas as pd
from .univariate_numeric_analysis import univariate_numeric_analysis

def batch_univariate_numeric_analysis(
    df: pd.DataFrame,
    columns: list[str],
    report_root: str = 'reports/eda/univariate/numeric',
    **analysis_kwargs
) -> dict[str, dict]:
    """
    Runs univariate_numeric_analysis on each column in `columns`.

    Returns:
        dict mapping column name → analysis results dict.
    """
    summary = {}
    for col in columns:
        print(f"\n\n==== Univariate Numeric Analysis for '{col}' ====")
        summary[col] = univariate_numeric_analysis(df[col], report_root, **analysis_kwargs)
    return summary
