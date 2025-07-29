import pandas as pd
from .univariate_categorical_analysis import univariate_categorical_analysis

def batch_univariate_categorical_analysis(
    df: pd.DataFrame,
    columns: list[str],
    top_n: int = 10,
    report_root: str = 'reports/eda/univariate/categorical'
) -> dict[str, dict]:
    """
    Runs univariate_categorical_analysis on each specified column.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        columns (list[str]): List of categorical column names to analyze.
        top_n (int, optional): Number of top categories to display in each bar plot.
        report_root (str, optional): Root directory for saving report.

    Returns:
        dict[str, dict]: Mapping from column name to the analysis results dict 
                         (missingness, frequency, cardinality, goodness_of_fit).
    """
    summary = {}
    for col in columns:
        print(f"\n\n==== Univariate Categorical Analysis for '{col}' ====")
        results = univariate_categorical_analysis(df[col], top_n=top_n, report_root=report_root)
        summary[col] = results
    return summary
