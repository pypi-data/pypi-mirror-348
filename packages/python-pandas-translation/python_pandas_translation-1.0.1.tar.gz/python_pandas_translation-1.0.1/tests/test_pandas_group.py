import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from python_pandas_translation.pandas_group import PandasGroup


@pytest.fixture
def pandas_group():
    return PandasGroup()


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        data={
            'category': ['A', 'A', 'B', 'B', 'A'],
            'type': ['X', 'X', 'Y', 'Y', 'Z'],
            'value': [10, 20, 30, 40, 50],
            'score': [1.0, 2.0, 3.0, 4.0, 5.0]
        }
    )


class TestPandasGroup:
    def test_group_mean(self, pandas_group: PandasGroup, sample_df: pd.DataFrame) -> None:
        result = pandas_group.group_mean(df=sample_df, by=['category'])
        expected = pd.DataFrame(
            data={
                'value': [26.666666, 35.0],
                'score': [2.6666667, 3.5]
            },
            index=pd.Index(data=['A', 'B'], name='category')
        )

        assert_frame_equal(result, expected, check_exact=False, rtol=1e-4)

    def test_group_sum(self, pandas_group: PandasGroup, sample_df: pd.DataFrame) -> None:
        result = pandas_group.group_sum(df=sample_df, by=['category'])
        expected = pd.DataFrame(
            data={
                'value': [80, 70],
                'score': [8.0, 7.0]
            },
            index=pd.Index(data=['A', 'B'], name='category')
        )

        assert_frame_equal(result, expected)

    def test_group_count(self, pandas_group: PandasGroup, sample_df: pd.DataFrame) -> None:
        result = pandas_group.group_count(df=sample_df, by=['category'])
        expected = pd.DataFrame(
            data={
                'type': [3, 2],
                'value': [3, 2],
                'score': [3, 2]
            },
            index=pd.Index(data=['A', 'B'], name='category')
        )

        assert_frame_equal(result, expected)
