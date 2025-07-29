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
import pandas as pd

def clean_series(series: pd.Series) -> pd.Series:
    """
    Drop null values from a pandas Series and ensure it is not empty.

    Args:
        series (pd.Series): Input Series, may contain NaNs.

    Returns:
        pd.Series: Series with NaNs dropped.

    Raises:
        ValueError: If the cleaned Series is empty after dropping NaNs.
    """
    clean = series.dropna()
    if clean.empty:
        raise ValueError("Series is empty after dropping NAs.")
    return clean
