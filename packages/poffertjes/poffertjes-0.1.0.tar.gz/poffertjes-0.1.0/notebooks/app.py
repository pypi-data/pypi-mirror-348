import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    from poffertjes.interface import VariableBuilder, p

    return VariableBuilder, np, p, pd


@app.cell
def _(VariableBuilder, np, pd):
    N_SAMPLES = 100
    columns = ["x", "y", "z", "u"]

    df = pd.DataFrame(
        dict(
            zip(
                columns,
                [np.random.randn(N_SAMPLES).transpose() for _ in range(len(columns))],
            )
        )
    ).map(lambda x: 10 * round(abs(x), 1))

    vb = VariableBuilder.from_data(df)

    x, y, z, u = vb.get_variables()
    x0, y0, z0, u0 = df.iloc[0]
    return u, u0, x, x0, y, y0, z, z0


@app.cell
def _(p, y, y0):
    p(y | (y == y0))
    return


@app.cell
def _(p, u, u0, x, x0, y, y0, z, z0):
    p((y == y0) | (x == x0), (z == z0), (u == u0))
    return


@app.cell
def _():
    # from tests.tests import (
    #     test_conditional_probability_single_variable_condition_tuple,
    #     test_conditional_probability_single_variable_single_condition,
    #     test_marginal_probability_single_variable,
    #     test_pointwise_conditional_probability_single_variable_single_condition,
    #     test_pointwise_marginal_probability,
    #     test_simmetry_conditional_probability_single_variable_condition_tuple,
    #     test_simmetry_joint_probability_two_variables,
    # )

    return


@app.cell
def _():
    # test_conditional_probability_single_variable_condition_tuple(df, x, y, z, y0, z0)
    # test_conditional_probability_single_variable_single_condition(df, x, y, y0)
    # test_marginal_probability_single_variable(df, x)
    # test_pointwise_conditional_probability_single_variable_single_condition(
    #     df, x, y, x0, y0
    # )
    # test_pointwise_marginal_probability(df, x, x0)
    # test_simmetry_conditional_probability_single_variable_condition_tuple(
    #     x, y, z, y0, z0
    # )
    # test_simmetry_joint_probability_two_variables(x, y, x0, y0)
    return


if __name__ == "__main__":
    app.run()
