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
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from scipy.stats import probplot

from .validate_numeric_named_series import validate_numeric_named_series

def _save_and_close(fig, path):
    """
    Save a Matplotlib figure to `path` and ensure it gets closed.
    """
    try:
        fig.savefig(path)
    finally:
        plt.close(fig)

def distribution_visualizations(
    s: pd.Series,
    report_dir: Path,
    transform: str = "raw"
) -> dict:
    """
    Display and save distribution plots for a numeric Series, annotating
    whether the data are raw or have been transformed.

    Args:
        s (pd.Series): Series containing the data.
        report_dir (Path): Directory for saving plot files.
        transform (str): Label for the data transformation applied
                         (e.g. "raw", "box-cox", "yeo-johnson").

    Returns:
        dict: Mapping from plot type to saved filepath.
    """
    # 1. Input validation
    validate_numeric_named_series(s)

    # 2. Drop nulls and short-circuit if empty
    s_clean = s.dropna()
    if s_clean.empty:
        return {}

    # Sanitize transform label for filenames
    label = transform.strip().replace(" ", "_")

    viz_paths: dict[str,str] = {}

    # 1. Histogram + KDE
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(s_clean, kde=True, ax=ax)
    ax.set_title(f"Histogram & KDE of '{s_clean.name}' ({transform})")
    ax.set_xlabel(s_clean.name)
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    hist_file = report_dir / f"{s_clean.name}_{label}_hist_kde.png"
    _save_and_close(fig, hist_file)
    viz_paths["hist_kde"] = str(hist_file)

    # 2. Boxplot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=s_clean, ax=ax)
    ax.set_title(f"Boxplot of '{s_clean.name}' ({transform})")
    ax.set_xlabel(s_clean.name)
    plt.tight_layout()
    box_file = report_dir / f"{s_clean.name}_{label}_boxplot.png"
    _save_and_close(fig, box_file)
    viz_paths["boxplot"] = str(box_file)

    # 3. ECDF
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.ecdfplot(s_clean, ax=ax)
    ax.set_title(f"ECDF of '{s_clean.name}' ({transform})")
    ax.set_xlabel(s_clean.name)
    ax.set_ylabel("ECDF")
    plt.tight_layout()
    ecdf_file = report_dir / f"{s_clean.name}_{label}_ecdf.png"
    _save_and_close(fig, ecdf_file)
    viz_paths["ecdf"] = str(ecdf_file)

    # 4. Q–Q plot
    fig = plt.figure(figsize=(6, 6))
    probplot(s_clean, dist="norm", plot=plt)
    plt.title(f"Q–Q Plot of '{s_clean.name}' ({transform})")
    plt.tight_layout()
    qq_file = report_dir / f"{s_clean.name}_{label}_qq_plot.png"
    _save_and_close(fig, qq_file)
    viz_paths["qq_plot"] = str(qq_file)

    return viz_paths
