import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from python_pandas_translation.pandas_column import PandasColumn
from pandas import DataFrame


# Sample fixture for DataFrame with field names
@pytest.fixture
def sample_df() -> DataFrame:
    return pd.DataFrame(
        data={
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': pd.Series([30, 25, None], dtype='Int64'),
            'score': [85.5, None, 92.0]
        }
    )


# Fixture for the PandasColumn instance
@pytest.fixture
def pandas_column() -> PandasColumn:
    return PandasColumn()


class TestPandasColumn:
    def test_get_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.get_columns(df=sample_df, columns=['name', 'score'])

        # Manually constructing expected DataFrame
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_drop_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.drop_columns(df=sample_df, columns=['age'])

        # Manually constructing expected DataFrame
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_rename_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.rename_columns(df=sample_df, new_names={'name': 'full_name'})

        # Manually constructing expected DataFrame with 'name' column renamed to 'full_name'
        expected = pd.DataFrame(
            data={
                'full_name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 25, None], dtype='Int64'),
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_add_column(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        values: list[str] = ['A', 'B', 'C']
        result = pandas_column.add_column(df=sample_df.copy(), column_name='grade', values=values)

        # Manually constructing expected DataFrame with the new column 'grade' added
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 25, None], dtype='Int64'),
                'score': [85.5, None, 92.0],
                'grade': ['A', 'B', 'C']
            }
        )

        assert_frame_equal(result, expected)

    def test_add_column_invalid_length(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        with pytest.raises(ValueError):
            pandas_column.add_column(df=sample_df.copy(), column_name='grade', values=['A'])

    def test_insert_column(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        values: list[str] = ['A', 'B', 'C']
        result = pandas_column.insert_column(
            df=sample_df.copy(),
            index=1,
            column_name='grade',
            values=values
        )

        # Manually constructing expected DataFrame with 'grade' inserted at index 1
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'grade': ['A', 'B', 'C'],
                'age': pd.Series([30, 25, None], dtype='Int64'),
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_insert_column_invalid_length(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        with pytest.raises(ValueError):
            pandas_column.insert_column(df=sample_df.copy(), index=1, column_name='grade', values=['A'])

    def test_find_nan_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.find_nan_columns(df=sample_df)

        # Manually constructing expected DataFrame with columns containing NaN values ('age', 'score')
        expected = pd.DataFrame(
            data=
            {
                'age': pd.Series([30, 25, None], dtype='Int64'),
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_fill_nan(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.fill_nan(df=sample_df.copy(), value=0)

        # Manually constructing expected DataFrame with NaN values filled with 0
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 25, 0], dtype='Int64'),
                'score': [85.5, 0, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_fill_nan_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.fill_nan_columns(df=sample_df.copy(), columns=['age'], value=99)

        # Manually constructing expected DataFrame with NaN values in 'age' column filled with 99
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie'],
                'age': pd.Series([30, 25, 99], dtype='Int64'),
                'score': [85.5, None, 92.0]
            }
        )

        assert_frame_equal(result, expected)

    def test_drop_nan_columns_any(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.drop_nan_columns(df=sample_df.copy(), how='any')

        # Manually constructing expected DataFrame after dropping columns with any NaN values
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Bob', 'Charlie']
            }
        )

        assert_frame_equal(result, expected)

    def test_drop_nan_columns_all(self, pandas_column: PandasColumn) -> None:
        df = pd.DataFrame(
            data={
                'A': [None, None],
                'B': [1, 2]
            }
        )
        result = pandas_column.drop_nan_columns(df=df, how='all')

        # Manually constructing expected DataFrame after dropping columns with all NaN values
        expected = pd.DataFrame(
            data={
                'B': [1, 2]
            }
        )

        assert_frame_equal(result, expected)

    def test_drop_nan_in_columns(self, sample_df: DataFrame, pandas_column: PandasColumn) -> None:
        result = pandas_column.drop_nan_in_columns(df=sample_df.copy(), columns=['score'], how='any')

        # Manually constructing expected DataFrame after dropping rows where 'score' has NaN
        expected = pd.DataFrame(
            data={
                'name': ['Alice', 'Charlie'],
                'age': pd.Series([30, None], dtype='Int64'),
                'score': [85.5, 92.0]
            }
        )

        assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
