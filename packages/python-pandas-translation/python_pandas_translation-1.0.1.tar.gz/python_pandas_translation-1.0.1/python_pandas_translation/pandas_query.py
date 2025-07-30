import logging
import pandas as pd
from typing import Any

logger = logging.getLogger(__name__)


class PandasQuery:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def filter_by_value(self, df: pd.DataFrame, column: str, value: Any, op: str = '==') -> pd.DataFrame:
        """ Filter DataFrame by a specific value in a column."""
        ops = {
            '==': df[column] == value,
            '!=': df[column] != value,
            '>': df[column] > value,
            '>=': df[column] >= value,
            '<': df[column] < value,
            '<=': df[column] <= value
        }
        return df[ops[op]]

    def filter_contains(self, df: pd.DataFrame, column: str, pattern: str, regex: bool = False) -> pd.DataFrame:
        """ Filter DataFrame by checking if a column contains a specific pattern."""
        return df[df[column].astype(str).str.contains(pattern, regex=regex)]

    def replace_value(self, df: pd.DataFrame, column: str, old_val: Any, new_val: Any) -> pd.DataFrame:
        """ Replace a specific value in a column with a new value."""
        df[column] = df[column].replace(old_val, new_val)
        return df

    def conditional_replace(
            self,
            df: pd.DataFrame,
            condition_col: str,
            condition_val: Any,
            target_cols: list[str],
            new_vals: list[Any],
            op: str = '=='
    ) -> pd.DataFrame:
        """ Replace values in target columns based on a condition in another column."""
        mask = self.filter_by_value(df=df, column=condition_col, value=condition_val, op=op).index
        for col, val in zip(target_cols, new_vals):
            df.loc[mask, col] = val
        return df


pandas_query = PandasQuery()
