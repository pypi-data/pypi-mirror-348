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

from ...core import write_json_report, missing_data_analysis, validate_categorical_named_series, categorical_inferential_analysis, categorical_distribution_analysis

def univariate_categorical_analysis(
    series: pd.Series,
    top_n: int = 10,
    report_root: str = 'reports/eda/univariate/categorical',
    rare_threshold: float = 0.01,
    alpha: float = 0.05,
) -> dict:
    """
    Conducts a full univariate analysis on a categorical column, saves plots and summary JSON:
      1. Validate categorical series.
      2. Missing Data Analysis
      3. Frequency Distribution Analysis
      4. Cardinality and Imbalance Analysis
      5. Bar plot of top categories (others grouped as 'Other')
      6. Chi-square goodness-of-fit against uniform distribution

    Args:
        series (pd.Series): Series to analyze.
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
    validate_categorical_named_series(series)

    # Prepare save directory
    save_dir = Path(report_root) / series.name.replace(' ', '_')
    save_dir.mkdir(parents=True, exist_ok=True)

    total = int(len(series))

    # 2. Missing Data Analysis
    missing_data = missing_data_analysis(series, save_dir)

    # 3. Distribution Analysis
    distribution_result = categorical_distribution_analysis(series, save_dir, top_n)
    freq_tbl = distribution_result['report']['frequency_report']['frequency_table']

    # 4. Outlier Analysis
    # Identify rare categories
    rare_categories = [
        cat
        for cat, stats in freq_tbl.items()
        if stats['proportion'] < rare_threshold
    ]

    outliers = {
        'rare_categories': rare_categories,
    }

    # 5. Inferential Analysis
    inferential = categorical_inferential_analysis(freq_tbl, total, alpha)

    # 6. Generate report
    report = {
        'missing_data': missing_data,
        'distribution': distribution_result['report'],
        'outliers': outliers,
        'inferential': inferential
    }

    report_path = save_dir / f"{series.name.replace(' ', '_')}_univariate_analysis_report.json"
    full_report = write_json_report(report, report_path)

    return full_report
