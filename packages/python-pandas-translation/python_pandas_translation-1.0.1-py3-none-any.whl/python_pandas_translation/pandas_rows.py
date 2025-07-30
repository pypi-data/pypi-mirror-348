import logging
import pandas as pd
from typing import Optional, Any, Union

logger = logging.getLogger(__name__)


class PandasRows:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_rows(self, df: pd.DataFrame, start: int = 0, end: Optional[int] = None) -> pd.DataFrame:
        """ Get rows from a DataFrame."""
        return df.iloc[start:end+1]

    def drop_rows(self, df: pd.DataFrame, index: Union[int, list[int]]) -> pd.DataFrame:
        """ Drop rows from a DataFrame."""
        if isinstance(index, int):
            index = [index]
        return df.drop(index=index)

    def add_row(self, df: pd.DataFrame, row: list[Any]) -> pd.DataFrame:
        """ Add a row to a DataFrame."""
        if len(row) != len(df.columns):
            raise ValueError("Row length does not match number of columns")
        return pd.concat([df, pd.DataFrame([row], columns=df.columns)], ignore_index=True)

    def insert_row(self, df: pd.DataFrame, index: int, row: list[Any]) -> pd.DataFrame:
        """ Insert a row at a specific index in a DataFrame."""
        new_row = pd.DataFrame([row], columns=df.columns)
        return pd.concat([df.iloc[:index], new_row, df.iloc[index:]]).reset_index(drop=True)

    def find_duplicates(
            self,
            df: pd.DataFrame,
            subset: Optional[list[str]] = None,
            keep: Union[str, bool] = 'first'
    ) -> pd.DataFrame:
        """ Find duplicates in a DataFrame."""
        return df[df.duplicated(subset=subset, keep=keep)]

    def drop_duplicates(
            self, df: pd.DataFrame,
            subset: Optional[list[str]] = None,
            keep: Union[str, bool] = 'first'
    ) -> pd.DataFrame:
        """ Drop duplicates from a DataFrame."""
        return df.drop_duplicates(subset=subset, keep=keep)

    def find_unique(self, df: pd.DataFrame, column: str) -> pd.Series:
        """ Find unique values in a column."""
        return df[column].unique()

    def drop_unique(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """ Drop unique values from a column."""
        unique_values = df[column].unique()
        return df[~df[column].isin(unique_values)]

    def find_nan_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Find rows with NaN values."""
        return df[df.isna().any(axis=1)]

    def fill_nan_rows(self, df: pd.DataFrame, value: Any) -> pd.DataFrame:
        """ Fill NaN values in rows."""
        return df.fillna(value=value)

    def fill_nan_rows_in_columns(self, df: pd.DataFrame, columns: list[str], value: Any) -> pd.DataFrame:
        """ Fill NaN values in specific columns of rows."""
        for col in columns:
            df[col] = df[col].fillna(value)
        return df

    def drop_nan_rows(self, df: pd.DataFrame, how='any') -> pd.DataFrame:
        """ Drop rows with NaN values."""
        return df.dropna(axis=0, how=how)


pandas_row = PandasRows()
