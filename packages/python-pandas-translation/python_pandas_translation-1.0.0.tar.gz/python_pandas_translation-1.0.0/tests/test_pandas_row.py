import numpy as np
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from python_pandas_translation.pandas_rows import PandasRows


@pytest.fixture
def sample_df():
    """Fixture providing a sample DataFrame for the tests."""
    return pd.DataFrame(
        {
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [30, 25, 35]
        }
    )


@pytest.fixture
def pandas_rows():
    """Fixture for creating an instance of PandasRows."""
    return PandasRows()


class TestPandasRows:
    def test_get_rows(self, sample_df, pandas_rows):
        """Test getting rows from a DataFrame."""
        result = pandas_rows.get_rows(sample_df, start=0, end=1)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob'],
                'age': [30, 25]
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_drop_rows(self, sample_df, pandas_rows):
        """Test dropping rows from a DataFrame."""
        result = pandas_rows.drop_rows(sample_df, index=1)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Charlie'],
                'age': [30, 35]
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_add_row(self, sample_df, pandas_rows):
        """Test adding a row to a DataFrame."""
        new_row = ['David', 40]
        result = pandas_rows.add_row(sample_df, new_row)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie', 'David'],
                'age': [30, 25, 35, 40]
            }
        )
        assert_frame_equal(result, expected_df)

    def test_add_row_invalid_length(self, sample_df, pandas_rows):
        """Test adding a row with invalid length (doesn't match number of columns)."""
        new_row = ['David']  # Only one value instead of two
        with pytest.raises(ValueError):
            pandas_rows.add_row(sample_df, new_row)

    def test_insert_row(self, sample_df, pandas_rows):
        """Test inserting a row at a specific index."""
        new_row = ['David', 40]
        result = pandas_rows.insert_row(sample_df, index=1, row=new_row)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'David', 'Bob', 'Charlie'],
                'age': [30, 40, 25, 35]
            }
        )
        assert_frame_equal(result, expected_df)

    def test_find_duplicates(self, pandas_rows):
        """Test finding duplicates in a DataFrame."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Alice'],
                'age': [30, 25, 30]
            }
        )
        result = pandas_rows.find_duplicates(df)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice'],
                'age': [30]
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_drop_duplicates(self, pandas_rows):
        """Test dropping duplicates from a DataFrame."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Alice'],
                'age': [30, 25, 30]
            }
        )
        result = pandas_rows.drop_duplicates(df)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob'],
                'age': [30, 25]
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_find_unique(self, sample_df, pandas_rows):
        """Test finding unique values in a column."""
        result = pandas_rows.find_unique(sample_df, column='name')
        expected = ['Alice', 'Bob', 'Charlie']
        assert list(result) == expected

    def test_drop_unique(self, sample_df, pandas_rows):
        """Test dropping unique values from a column."""
        result = pandas_rows.drop_unique(sample_df, column='name')
        expected_df = pd.DataFrame(
            {
                'name': pd.Series(dtype='object'),
                'age': pd.Series(dtype='int64')
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_find_nan_rows(self, pandas_rows):
        """Test finding rows with NaN values."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': [30, None, 35]
            }
        )
        result = pandas_rows.find_nan_rows(df)
        expected_df = pd.DataFrame(
            {
                'name': ['Bob'],
                'age': [np.nan]
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_fill_nan_rows(self, pandas_rows):
        """Test filling NaN values in rows."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 28, 35], dtype='int64')
            }
        )
        result = pandas_rows.fill_nan_rows(df, value=28)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 28, 35], dtype='int64')
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_fill_nan_rows_in_columns(self, pandas_rows):
        """Test filling NaN values in specific columns."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, None, 35], dtype='Int64')
            }
        )
        result = pandas_rows.fill_nan_rows_in_columns(df, columns=['age'], value=28)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 28, 35], dtype='Int64')
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)

    def test_drop_nan_rows(self, pandas_rows):
        """Test dropping rows with NaN values."""
        df = pd.DataFrame(
            {
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, None, 35], dtype='Int64')
            }
        )
        result = pandas_rows.drop_nan_rows(df)
        expected_df = pd.DataFrame(
            {
                'name': ['Alice', 'Charlie'],
                'age': pd.Series([30, 35], dtype='Int64')
            }
        )

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        assert_frame_equal(result, expected_df)
