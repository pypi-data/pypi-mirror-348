import logging
import pandas as pd

logger = logging.getLogger(__name__)


class PandasGroup:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def group_mean(self, df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
        """ Group DataFrame by specific columns and calculate the mean."""
        return df.groupby(by=by).mean(numeric_only=True)

    def group_sum(self, df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
        """ Group DataFrame by specific columns and calculate the sum."""
        return df.groupby(by=by).sum(numeric_only=True)

    def group_count(self, df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
        """ Group DataFrame by specific columns and count the occurrences."""
        return df.groupby(by=by).count()


pandas_group = PandasGroup()
