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
from pandas.api.types import is_numeric_dtype
import pandas as pd

def verify_numeric_column(df: pd.DataFrame, column: str) -> None:
    """
    Ensure the specified column exists in the DataFrame and is numeric.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        column (str): Name of the column to verify.

    Raises:
        KeyError: If `column` is not present in `df`.
        TypeError: If `column` exists but is not of a numeric dtype.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")
    if not is_numeric_dtype(df[column]):
        raise TypeError(f"Column '{column}' must be numeric for analysis.")
