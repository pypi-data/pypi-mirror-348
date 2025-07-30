import logging
import pandas as pd
from typing import Optional, Any, Union

logger = logging.getLogger(__name__)


class PandasColumn:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_columns(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """ Get specific columns from a DataFrame."""
        return df[columns]

    def drop_columns(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """ Drop specific columns from a DataFrame."""
        return df.drop(columns=columns)

    def rename_columns(self, df: pd.DataFrame, new_names: dict[str, str]) -> pd.DataFrame:
        """ Rename columns in a DataFrame."""
        return df.rename(columns=new_names)

    def add_column(self, df: pd.DataFrame, column_name: str, values: list[Any]) -> pd.DataFrame:
        """ Add a new column to a DataFrame."""
        if len(values) != len(df):
            raise ValueError("Length of values does not match number of rows in DataFrame")
        df[column_name] = values
        return df

    def insert_column(self, df: pd.DataFrame, index: int, column_name: str, values: Any) -> pd.DataFrame:
        """ Insert a new column at a specific index in a DataFrame."""
        if len(values) != len(df):
            raise ValueError("Length of values does not match number of rows in DataFrame")
        df.insert(loc=index, column=column_name, value=values)
        return df

    def find_nan_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Find columns with NaN values. """
        return df.loc[:, df.isna().any(axis=0)]

    def fill_nan(self, df: pd.DataFrame, value: Any) -> pd.DataFrame:
        """ Fill NaN values in a DataFrame."""
        return df.fillna(value=value)

    def fill_nan_columns(self, df: pd.DataFrame, columns: list[str], value: Any) -> pd.DataFrame:
        """ Fill NaN values in specific columns of a DataFrame."""
        for col in columns:
            df[col] = df[col].fillna(value)
        return df

    def drop_nan_columns(self, df: pd.DataFrame, how: str = 'any') -> pd.DataFrame:
        """ Drop columns with NaN values."""
        return df.dropna(axis=1, how=how)

    def drop_nan_in_columns(self, df: pd.DataFrame, columns: list[str], how: str = 'any') -> pd.DataFrame:
        """ Drop rows with NaN values in specific columns."""
        return df.dropna(subset=columns, how=how)


pandas_column = PandasColumn()
