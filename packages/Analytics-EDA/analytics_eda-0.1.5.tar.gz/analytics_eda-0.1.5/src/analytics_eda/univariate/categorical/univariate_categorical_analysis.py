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
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_categorical_dtype, is_object_dtype
from scipy.stats import chisquare

from ...core import write_json_report, missing_data_analysis

def verify_categorical_column(df: pd.DataFrame, column: str) -> None:
    """
    Ensure the specified column exists in the DataFrame and is categorical or object dtype.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")
    if not (is_categorical_dtype(df[column]) or is_object_dtype(df[column])):
        raise TypeError(f"Column '{column}' must be categorical (or object) for categorical analysis.")

def univariate_categorical_analysis(
    df: pd.DataFrame,
    column: str,
    top_n: int = 10,
    report_root: str = 'reports/eda/univariate/categorical',
    rare_threshold: float = 0.01
) -> dict:
    """
    Conducts a full univariate analysis on a categorical column, saves plots and summary JSON:
      1. Validation
      2. Missing Data Analysis
      3. Frequency Distribution Analysis
      4. Cardinality and Imbalance Analysis
      5. Bar plot of top categories (others grouped as 'Other')
      6. Chi-square goodness-of-fit against uniform distribution

    Args:
        df (pd.DataFrame): Source DataFrame.
        column (str): Name of the categorical column to analyze.
        top_n (int, optional): Number of top categories to display in the bar plot. Default is 10. If there are less than top_n, it will readjust.
        report_root (str, optional): Root directory for saving report.
        rare_threshold (float): Rare category threshold. Defaults to less than 1% of total.

    Returns:
        dict: {
            'missingness': dict(total, missing, pct_missing),
            'frequency': dict of category -> {count, proportion},
            'cardinality': int,
            'goodness_of_fit': { 'chi2': float, 'p_value': float } or None
        }
    """
    # 1. Validation
    verify_categorical_column(df, column)

    # Prepare save directory
    save_dir = Path(report_root) / column.replace(' ', '_')
    save_dir.mkdir(parents=True, exist_ok=True)

    total = int(len(df))

    # 2. Missing Data Analysis
    missing_data = missing_data_analysis(df[column], save_dir)

    # 3. Frequency Distribution Analysis
    freq = df[column].value_counts(dropna=False).rename_axis(column)
    props = freq / total
    frequency = {
        str(cat): {
            'count': int(freq_cat),
            'proportion': float(props_cat)
        }
        for cat, freq_cat, props_cat in zip(freq.index, freq.values, props.values)
    }

    # Identify rare categories
    rare_categories = [cat for cat, prop in props.items() if prop < rare_threshold]

    # Category Quality Checks
    category_lengths = {str(cat): len(str(cat)) for cat in freq.index}
    max_length = max(category_lengths.values())
    min_length = min(category_lengths.values())

    # 4. Cardinality and Imbalance Analysis
    cardinality = int(df[column].nunique(dropna=True))
    imbalance_ratio = freq.max() / freq.min()

    # 5. Bar plot of top N categories
    unique_categories = len(freq)

    # If fewer than requested top_n, adjust top_n (e.g., reduce to 5 if <10 categories)
    if unique_categories <= top_n:
        # Set top_n to half of available categories (or at least 1)
        top_n = max(1, unique_categories // 2)

    top = freq.head(top_n)
    others_count = freq.iloc[top_n:].sum()
    top = pd.concat([top, pd.Series({'Others': others_count})])
    top = top.sort_values(ascending=False)

    # Define accessible colors
    color_map = {
        0: "#DAA520",   # Gold
        1: "#C0C0C0",   # Silver
        2: "#CD7F32",   # Bronze
    }
    default_color = "steelblue"
    others_color = "#A9A9A9"

    # Assign colors
    colors = []
    for i, cat in enumerate(top.index):
        if cat == "Others":
            colors.append(others_color)
        elif i in color_map:
            colors.append(color_map[i])
        else:
            colors.append(default_color)

    # Plot
    plt.figure(figsize=(10, 8))
    ax2 = sns.barplot(x=top.values, y=top.index, palette=colors)

    # Add value labels
    for i, v in enumerate(top.values):
        ax2.text(v + max(top.values) * 0.01, i, f"{v:,}", va="center", fontsize=10)

    # Set labels and title
    ax2.set_title(f"Top {top_n} Values in {column.replace('_', ' ').title()} (+Others Aggregated)",
                fontsize=14, weight="bold")
    ax2.set_xlabel("Count", fontsize=12)
    ax2.set_ylabel(column.replace("_", " ").title(), fontsize=12)

    plt.tight_layout()
    fig2 = ax2.get_figure()
    fig2.savefig(save_dir / f"{column.replace(' ', '_')}_top_{top_n}.png")
    plt.close(fig2)

    # 6. Chi-square goodness-of-fit vs uniform
    # Assume a uniform distribution for expected frequencies (i.e., each category is equally likely).
    # Note: In highly imbalanced data, this uniform assumption may not reflect real-world distributions.
    expected = [total / len(freq)] * len(freq)
    chi2_stat, p_val = chisquare(freq.values, f_exp=expected)

    alpha = 0.05
    reject = bool(p_val < alpha)
    goodness_of_fit = {
        'chi2_statistic': float(chi2_stat),
        'p_value':        float(p_val),
        'alpha':          float(alpha),
        'reject_null_uniform': reject
    }

    # 7. write JSON report
    report = {
        'missing_data': missing_data,
        'frequency': frequency,
        'cardinality': cardinality,
        'imbalance_ratio': imbalance_ratio,
        'rare_categories': rare_categories,
        'goodness_of_fit': goodness_of_fit,
        'category_length_stats': {'max_length': max_length, 'min_length': min_length}
    }

    report_path = save_dir / f"{column.replace(' ', '_')}_univariate_analysis_report.json"
    full_report = write_json_report(report, report_path)

    return full_report
