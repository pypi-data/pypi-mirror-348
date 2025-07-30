import os
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from tempfile import NamedTemporaryFile
from python_pandas_translation.pandas_io import PandasIO


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            'name': ['Alice', 'Bob'],
            'age': [30, 25]
        }
    )


@pytest.fixture
def pandas_io():
    return PandasIO()


class TestCSVIO:
    def test_save_csv(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_csv(df=sample_df, path=tmp_path)

            # Verify if the file is saved and content is correct
            saved_df = pandas_io.load_csv(path=tmp_path)
            assert_frame_equal(saved_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_csv(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_csv(df=sample_df, path=tmp_path, index=False)
            loaded_df = pandas_io.load_csv(path=tmp_path)
            assert_frame_equal(loaded_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_csv_error_handling(self, pandas_io: PandasIO) -> None:
        with pytest.raises(Exception):
            pandas_io.load_csv(path="non_existent_file.csv")

    def test_save_csv_error_handling(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        # Simulate an error during save by providing invalid file path
        with pytest.raises(OSError):
            pandas_io.save_csv(df=sample_df, path="/invalid/path/to/file.csv")


class TestExcelIO:
    def test_save_excel(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_excel(df=sample_df, path=tmp_path)
            # Verify if the file is saved and content is correct
            saved_df = pandas_io.load_excel(path=tmp_path)
            assert_frame_equal(saved_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_excel(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_excel(df=sample_df, path=tmp_path, index=False)
            loaded_df = pandas_io.load_excel(path=tmp_path)
            assert_frame_equal(loaded_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_excel_error_handling(self, pandas_io: PandasIO) -> None:
        with pytest.raises(Exception):
            pandas_io.load_excel(path="non_existent_file.xlsx")

    def test_save_excel_error_handling(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        # Simulate an error during save by providing invalid file path
        with pytest.raises(OSError):
            pandas_io.save_excel(df=sample_df, path="/invalid/path/to/file.xlsx")


class TestTXTIO:
    def test_save_txt(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_txt(df=sample_df, path=tmp_path, sep='\t')
            # Verify if the file is saved and content is correct
            saved_df = pandas_io.load_txt(path=tmp_path, sep='\t')
            assert_frame_equal(saved_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_txt(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        with NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            pandas_io.save_csv(df=sample_df, path=tmp_path, index=False, sep='\t')
            loaded_df = pandas_io.load_txt(path=tmp_path, sep='\t')
            assert_frame_equal(loaded_df, sample_df)
        finally:
            os.remove(path=tmp_path)

    def test_load_txt_error_handling(self, pandas_io: PandasIO) -> None:
        with pytest.raises(Exception):
            pandas_io.load_txt(path="non_existent_file.txt")

    def test_save_txt_error_handling(self, sample_df: pd.DataFrame, pandas_io: PandasIO) -> None:
        # Simulate an error during save by providing invalid file path
        with pytest.raises(OSError):
            pandas_io.save_txt(df=sample_df, path="/invalid/path/to/file.txt", sep='\t')
