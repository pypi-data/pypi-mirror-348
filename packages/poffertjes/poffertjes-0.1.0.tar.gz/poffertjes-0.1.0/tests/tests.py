import pandas as pd
import numpy as np

from poffertjes import p, Variable
from typing import Any


def test_marginal_probability_single_variable(df: pd.DataFrame, x: Variable) -> None:
    pd.testing.assert_series_equal(df[x.name].value_counts(normalize=True), p(x))


def test_conditional_probability_single_variable_single_condition(
    df: pd.DataFrame, x: Variable, y: Variable, y0: Any
) -> None:
    pd.testing.assert_series_equal(
        df.loc[df[y.name] == y0, x.name].value_counts(normalize=True), p(x | (y == y0))
    )


def test_conditional_probability_single_variable_condition_tuple(
    df: pd.DataFrame, x: Variable, y: Variable, z: Variable, y0: Any, z0: Any
) -> None:
    pd.testing.assert_series_equal(
        df.loc[(df[y.name] == y0) & (df[z.name] == z0), x.name].value_counts(
            normalize=True
        ),
        p(x | (y == y0, z == z0)),
    )


def test_simmetry_conditional_probability_single_variable_condition_tuple(
    x: Variable, y: Variable, z: Variable, y0: Any, z0: Any
) -> None:
    pd.testing.assert_series_equal(
        p(x | (z == z0, y == y0)),
        p(x | (y == y0, z == z0)),
    )


def test_pointwise_marginal_probability(df: pd.DataFrame, x: Variable, x0: Any) -> None:
    assert (len(df.loc[df[x.name] == x0]) / len(df)) == p(x == x0)


def test_pointwise_conditional_probability_single_variable_single_condition(
    df: pd.DataFrame, x: Variable, y: Variable, x0: Any, y0: Any
) -> None:
    assert (
        len(df.loc[(df[x.name] == x0) & (df[y.name] == y0)])
        / len(df.loc[df[x.name] == x0])
        if not df.loc[df[x.name] == x0].empty
        else 0
    ) == p((y == y0) | (x == x0))


def test_simmetry_joint_probability_two_variables(
    x: Variable, y: Variable, x0: Any, y0: Any
) -> None:
    assert np.isclose(p(x == x0, y == y0), p(y == y0, x == x0))
