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
import os
from pathlib import Path
import pandas as pd

import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL

def analyze_time_series_structure(df: pd.DataFrame,
                                  value_col: str,
                                  time_col: str,
                                  report_dir: Path,
                                  outlier_iqr_multiplier: float = 1.5,
                                  rolling_window: int = 12) -> None:
    """
    Stage 1: Analyze Time Series Structure
    -------------------------------------
    Understand structure, patterns, and characteristics of a univariate time series.

    Parameters:
    - df (pd.DataFrame): Time-indexed DataFrame or one containing a time column.
    - value_col (str): Name of the numeric series column to analyze.
    - time_col (str): Name of the datetime column (if not already index).
    - report_dir (Path): Directory under which plots and outputs are saved.
    - outlier_iqr_multiplier (float): IQR multiplier for outlier detection.
    - rolling_window (int): Window size for rolling‐mean smoothing.

    Outputs (saved under report_dir):
    - frequency.txt           : Detected sampling frequency
    - outliers.csv            : List of detected outliers
    - line_plot.png           : Raw series over time
    - rolling_mean.png        : Series & rolling mean overlay
    - acf.png                 : Autocorrelation plot
    - pacf.png                : Partial autocorrelation plot
    - stl_decomposition.png   : STL decomposition (trend, seasonality, remainder)
    """

    # 1. Ensure datetime index
    ts = df.copy()
    if time_col in ts.columns:
        if not pd.api.types.is_datetime64_any_dtype(ts[time_col]):
            raise TypeError(f"'{time_col}' must be datetime64 dtype before structure analysis.")
        ts = ts.set_index(time_col)
    ts = ts.sort_index()

    # 2. Check frequency
    # Try the built-in inferred_freq, then fallback to infer_freq
    freq = ts.index.inferred_freq
    if freq is None:
        freq = pd.infer_freq(ts.index)

    with open(os.path.join(report_dir, 'frequency.txt'), 'w') as f:
        f.write(str(freq))
    print(f"[Structure EDA] Detected frequency: {freq}")

    # 3. Detect outliers via IQR
    series = ts[value_col].dropna()
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - outlier_iqr_multiplier * iqr, q3 + outlier_iqr_multiplier * iqr
    outliers = series[(series < lower) | (series > upper)]
    outliers.to_csv(os.path.join(report_dir, 'outliers.csv'))
    print(f"[Structure EDA] Found {len(outliers)} outliers (IQR multiplier = {outlier_iqr_multiplier})")

    # 4. Plot raw series
    plt.figure(figsize=(10, 4))
    series.plot(title=f'{value_col} Time Series')
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'line_plot.png'))
    plt.close()

    # 5. Plot rolling mean
    rolling_mean = series.rolling(window=rolling_window, min_periods=1).mean()
    plt.figure(figsize=(10, 4))
    plt.plot(series, label='Original')
    plt.plot(rolling_mean, label=f'Rolling Mean ({rolling_window})')
    plt.legend()
    plt.title(f'{value_col} Rolling Mean')
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'rolling_mean.png'))
    plt.close()

    # 6. ACF & PACF
    fig_acf = plot_acf(series, lags=min(len(series)//2, 40))
    fig_acf.suptitle('Autocorrelation (ACF)')
    fig_acf.tight_layout()
    fig_acf.savefig(os.path.join(report_dir, 'acf.png'))
    plt.close(fig_acf)

    fig_pacf = plot_pacf(series, lags=min(len(series)//2, 40))
    fig_pacf.suptitle('Partial Autocorrelation (PACF)')
    fig_pacf.tight_layout()
    fig_pacf.savefig(os.path.join(report_dir, 'pacf.png'))
    plt.close(fig_pacf)

    # 7. STL decomposition
    # Infer seasonal period (e.g., 12 for monthly, 7 for daily if weekly seasonality)
    period = None
    if freq is not None:
        if 'M' in str(freq):
            period = 12
        elif 'D' in str(freq):
            period = 7
    if period:
        stl = STL(series, period=period)
        result = stl.fit()
        fig = result.plot()
        fig.suptitle('STL Decomposition')
        fig.tight_layout()
        fig.savefig(os.path.join(report_dir, 'stl_decomposition.png'))
        plt.close(fig)
        print(f"[Structure EDA] STL decomposition completed (period={period})")
    else:
        print("[Structure EDA] Skipped STL decomposition (could not infer period)")


def univariate_timeseries_analysis(df: pd.DataFrame, 
                                   value_col: str, 
                                   time_col: str, 
                                   report_root: str = 'reports/eda/univariate/timeseries',
                                   outlier_iqr_multiplier: float = 1.5,
                                   rolling_window: int = 12) -> pd.DataFrame:
    """
    Stage 0: Prepare Time Series Data for Univariate Analysis.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing time and value columns.
    - value_col (str): Name of the column with numeric values (must already be numeric dtype).
    - time_col (str): Name of the column with time (must already be datetime64 dtype).
    - report_root (str): Root path for saving any generated reports (default is 'reports/eda/univariate/timeseries').

    Returns:
    - pd.DataFrame: Time-indexed DataFrame with validated types.
    """
    print(f"\n\n==== Univariate Time-Series Analysis for '{time_col}' and '{value_col}' ====")

    # Work on a copy to preserve original data
    df_copy = df.copy()

    # 1. Validate that time_col is datetime64
    if not pd.api.types.is_datetime64_any_dtype(df_copy[time_col]):
        raise TypeError(
            f"Column '{time_col}' is of type {df_copy[time_col].dtype}; "
            "expected datetime64 dtype. "
            "Please convert it to datetime in your cleaning pipeline before analysis."
        )

    # 2. Validate that value_col is numeric
    if not pd.api.types.is_numeric_dtype(df_copy[value_col]):
        raise TypeError(
            f"Column '{value_col}' is of type {df_copy[value_col].dtype}; "
            "expected a numeric dtype. "
            "Please convert it to numeric in your cleaning pipeline before analysis."
        )

    # 3. Drop rows with missing values in essential columns
    df_copy = df_copy.dropna(subset=[time_col, value_col])

    # 4. Set datetime index and sort chronologically
    df_copy = df_copy.set_index(time_col).sort_index()

    # 5. Prepare report directory
    report_dir = Path(report_root) / f"{time_col.replace(' ', '_')}_{value_col.replace(' ', '_')}"
    report_dir.mkdir(parents=True, exist_ok=True)

    # 6. Analyze Time Series Structure
    analyze_time_series_structure(df, value_col, time_col, report_dir, outlier_iqr_multiplier, rolling_window)

    return df_copy

# Stage 2: Stationarity Testing & Transformation
# Goal: Determine if the time-series is stationary — i.e., its statistical properties are consistent over time.

# Visual inspection	Informally detect trends, variance shifts
# Augmented Dickey-Fuller (ADF), KPSS tests	Formal tests of stationarity
# Differencing	Remove trend or seasonality to stabilize mean
# Log or Box-Cox transform	Stabilize variance (homoscedasticity)

# Stage 3: Modeling (Post-EDA Phase)
# Model Selection & Fitting - Select based on patterns uncovered during EDA

# Model Diagnostics - Analyze residuals: should be white noise (i.e., no autocorrelation, constant variance).
#* Residual plots
#* ACF/PACF of residuals
#* Ljung-Box test

# Forecasting & Evaluation - Split data into train/test or use walk-forward validation.
# Evaluate using MAE, RMSE, MAPE, etc.
# Plot forecasts with confidence intervals.

