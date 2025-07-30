import logging
import pandas as pd
from typing import Optional, Union

logger = logging.getLogger(__name__)


class PandasIO:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_csv(
            self,
            path: str,
            sep: str = ',',
            header: Optional[int] = 0,
            index_col: Optional[Union[int, str]] = None
    ) -> pd.DataFrame:
        self.logger.debug(f"Loading CSV from {path}")
        try:
            return pd.read_csv(filepath_or_buffer=path, sep=sep, header=header, index_col=index_col)
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            raise

    def load_excel(self, path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        self.logger.debug(f"Loading Excel from {path}")
        try:
            return pd.read_excel(io=path, sheet_name=sheet_name)
        except Exception as e:
            self.logger.error(f"Error loading Excel: {e}")
            raise

    def load_txt(self, path: str, sep: str = ',') -> pd.DataFrame:
        self.logger.debug(f"Loading TXT from {path}")
        return self.load_csv(path=path, sep=sep)

    def save_csv(self, df: pd.DataFrame, path: str, sep: str = ',', mode: str = 'w', header: bool = True,
                 index: bool = False) -> None:
        self.logger.debug(f"Saving CSV to {path}")
        df.to_csv(path_or_buf=path, mode=mode, header=header, index=index, sep=sep)

    def save_excel(self, df: pd.DataFrame, path: str, index: bool = False) -> None:
        self.logger.debug(f"Saving Excel to {path}")
        with pd.ExcelWriter(path) as writer:
            df.to_excel(excel_writer=writer, index=index)

    def save_txt(
            self,
            df: pd.DataFrame,
            path: str,
            sep: str = ',',
            mode: str = 'w',
            header: bool = True,
            index: bool = False
    ) -> None:
        self.logger.debug(f"Saving TXT to {path}")
        df.to_csv(path, sep=sep, mode=mode, header=header, index=index)


pandas_io = PandasIO()
