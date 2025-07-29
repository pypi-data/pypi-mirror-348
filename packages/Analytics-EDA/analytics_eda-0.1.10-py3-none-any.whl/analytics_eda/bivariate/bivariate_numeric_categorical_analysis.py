# Copyright 2025 ArchiStrata, LLC and Andrew Dabrowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path

import pandas as pd
from scipy.stats import f_oneway, kruskal
from pandas.api.types import is_numeric_dtype, is_categorical_dtype, is_object_dtype

from ..univariate import univariate_numeric_analysis
from ..core import write_json_report

def run_statistical_tests(
        df: pd.DataFrame,
        numeric_col: str,
        categorical_col: str,
        alpha: float = 0.05) -> dict:
    """
    Perform ANOVA and Kruskal-Wallis tests to evaluate whether the distribution
    of a numeric variable differs across categories of a categorical variable.

    Args:
        df (pd.DataFrame): The input DataFrame.
        numeric_col (str): The name of the numeric column.
        categorical_col (str): The name of the categorical column.
        alpha (float): Significance level for hypothesis testing (default: 0.05).

    Returns:
        dict: A dictionary containing:
            - 'anova': {'statistic', 'p_value', 'reject'} or {'error'}
            - 'kruskal': {'statistic', 'p_value', 'reject'} or {'error'}
            Returns {'error': ...} if < 2 groups are found.
    """
    if numeric_col not in df.columns:
        raise KeyError(f"Numeric column '{numeric_col}' not found.")
    if categorical_col not in df.columns:
        raise KeyError(f"Categorical column '{categorical_col}' not found.")

    grouped_data = [
        group[numeric_col].dropna().values
        for _, group in df.groupby(categorical_col, observed=True)
    ]
    results = {}

    if len(grouped_data) < 2:
        return {"error": "Not enough groups to perform statistical tests."}

    try:
        anova_stat, anova_p = f_oneway(*grouped_data)
        results['anova'] = {
            'statistic': float(anova_stat),
            'p_value': float(anova_p),
            'reject': anova_p < alpha
        }
    except Exception as e:
        results['anova'] = {'error': str(e)}

    try:
        kruskal_stat, kruskal_p = kruskal(*grouped_data)
        results['kruskal'] = {
            'statistic': float(kruskal_stat),
            'p_value': float(kruskal_p),
            'reject': kruskal_p < alpha
        }
    except Exception as e:
        results['kruskal'] = {'error': str(e)}
    
    group_sizes = [len(g) for g in grouped_data]
    results['meta'] = {
        'n_groups': len(grouped_data),
        'group_sizes': group_sizes
    }

    return results

def bivariate_numeric_categorical_analysis(
    df: pd.DataFrame,
    numeric_col: str,
    categorical_col: str,
    report_root: str = 'reports/eda/bivariate/numeric_categorical',
    **kwargs
) -> dict:
    """
    Run univariate numeric analysis on segments defined by a categorical column.

    Args:
        df (pd.DataFrame): The dataset.
        numeric_col (str): Numeric column to analyze.
        categorical_col (str): Column to segment by.
        report_root (str): Root directory for saving reports.
        **kwargs: Additional arguments passed to univariate_numeric_analysis (e.g., alpha, iqr_multiplier).

    Returns:
        dict: Dictionary with statistical test results and per-segment univariate reports.
    """
    # 1. Validation
    if categorical_col not in df.columns:
        raise KeyError(f"Categorical column '{categorical_col}' not found.")
    if numeric_col not in df.columns:
        raise KeyError(f"Numeric column '{numeric_col}' not found.")
    if not (is_categorical_dtype(df[categorical_col]) or is_object_dtype(df[categorical_col])):
        raise TypeError(f"Column '{categorical_col}' must be categorical or object.")
    if not is_numeric_dtype(df[numeric_col]):
        raise TypeError(f"Column '{numeric_col}' must be numeric.")

    report_dir = Path(report_root) / numeric_col
    report_dir.mkdir(parents=True, exist_ok=True)

    statistical_tests = run_statistical_tests(df, numeric_col, categorical_col)

    segment_reports = {}
    for segment_value, group_df in df.groupby(categorical_col, observed=True):
        segment_name = str(segment_value).replace(" ", "_")
        segment_report_root = report_dir / f"{categorical_col}_{segment_name}"
        print(f"Running univariate analysis for segment '{segment_value}'...")

        try:
            report = univariate_numeric_analysis(
                group_df[numeric_col],
                report_root=segment_report_root,
                **kwargs
            )
            segment_reports[segment_value] = report
        except Exception as e:
            segment_reports[segment_value] = {'error': str(e)}

    full_report = {
        'statistical_tests': statistical_tests,
        'segments': segment_reports
    }

    report_path = report_dir / f"{numeric_col}_by_{categorical_col}_bivariate_analysis_report.json"
    full_report = write_json_report(full_report, report_path)

    return full_report
