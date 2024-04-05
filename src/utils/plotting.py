import numpy as np
import matplotlib.pyplot as plt

DEFAULT_PLOTTING_CARACTERISTICS = {
    "font": {
        "family": "serif",
        "color": "darkblue",
        "weight": "normal",
        "size": 16,
    },
    "figure_size": (15, 10),
}


def plot_linear_interpolation(
    points,
    inf,
    sup,
    title="Linear Interpolation",
    plotting_caracteristics=DEFAULT_PLOTTING_CARACTERISTICS,
):
    """
    Plots the linear interpolation between a series of points.

    Args:
    - points (list of tuples): A list of (x, f) points where the xs are in sorted order.
    - title (str): The title of the plot.
    """
    x_points, y_points = zip(*points)
    # Ensure the range is within the bounds of the data
    x_range = [min(inf, min(x_points)), max(sup, max(x_points))]
    x_values = np.linspace(x_range[0], x_range[1], 500)
    y_values = np.interp(x_values, x_points, y_points)

    # Now plot the points and the piecewise linear interpolation between them
    fig, axs = plt.subplots(figsize=plotting_caracteristics["figure_size"])

    axs.plot(x_points, y_points, "o", label="Data points")
    axs.plot(x_values, y_values, "-", label="Linear interpolation")

    axs.set_title(title, fontdict=plotting_caracteristics["font"])
    axs.set_xlabel("x", fontdict=plotting_caracteristics["font"])
    axs.set_ylabel("f(x)", fontdict=plotting_caracteristics["font"])
    axs.legend()
    axs.grid(True)

    plt.show()


def plot_linear_interpolation_with_penalty(
    points,
    penalty_coef,
    inf,
    sup,
    title="Linear Interpolation with Penalty",
    plotting_caracteristics=DEFAULT_PLOTTING_CARACTERISTICS,
):
    """
    Plots the linear interpolation with penalty coefficient for x-values greater than the largest x in points.

    Args:
    - points (list of tuples): A list of (x, f) points where the xs are in sorted order.
    - penalty_coef (float): The penalty coefficient to apply for x-values greater than the largest x.
    - title (str): The title of the plot.
    """
    x_points, y_points = zip(*points)
    x_range = [min(inf, min(x_points)), min(sup, x_points[-1])]
    x_values = np.linspace(x_range[0], x_range[1], 500)
    y_values = np.interp(x_values, x_points, y_points)

    # Handle plotting when the sup is beyond the last data point
    if sup > x_points[-1]:
        x_penalty = np.linspace(x_points[-1], sup, 100)
        y_intercept = y_points[-1] - penalty_coef * x_points[-1]
        y_penalty = penalty_coef * x_penalty + y_intercept
        x_values = np.concatenate((x_values, x_penalty))
        y_values = np.concatenate((y_values, y_penalty))

    # Plot the points and the piecewise linear interpolation
    fig, axs = plt.subplots(figsize=plotting_caracteristics["figure_size"])

    axs.plot(x_points, y_points, "o", label="Data points")
    axs.plot(x_values, y_values, "-", label="Interpolation with penalty")
    axs.set_xlim(inf, sup)

    axs.set_title(title, fontdict=plotting_caracteristics["font"])
    axs.set_xlabel("x", fontdict=plotting_caracteristics["font"])
    axs.set_ylabel("f(x)", fontdict=plotting_caracteristics["font"])
    axs.legend()
    axs.grid(True)

    plt.show()


def plot_indicator_with_all_limits(
    indicator_adjusted,
    indicator_name,
    dict_limits_config,
    from_year=None,
    to_year=None,
    plotting_caracteristics=DEFAULT_PLOTTING_CARACTERISTICS,
):
    nb_limits = len(dict_limits_config)
    indicator_adjusted_to_plot = indicator_adjusted.copy()
    if from_year:
        if to_year:
            indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[
                from_year:to_year
            ].copy()
        else:
            indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[
                from_year:
            ].copy()
    elif to_year:
        indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[:to_year].copy()

    count = 0
    for limit in list(dict_limits_config.keys()):
        if count == 0:
            indicator_adjusted_to_plot["sub_" + indicator_name + "_" + str(count)] = (
                indicator_adjusted_to_plot["sub_" + indicator_name + "_" + limit]
            )
            indicator_adjusted_to_plot[
                "sub_" + indicator_name + "_adjusted_" + str(count)
            ] = indicator_adjusted_to_plot[
                "sub_" + indicator_name + "_adjusted_" + limit
            ]
        else:
            indicator_adjusted_to_plot["sub_" + indicator_name + "_" + str(count)] = (
                indicator_adjusted_to_plot["sub_" + indicator_name + "_" + limit]
                + indicator_adjusted_to_plot[
                    "sub_" + indicator_name + "_" + str(count - 1)
                ]
            )
            indicator_adjusted_to_plot[
                "sub_" + indicator_name + "_adjusted_" + str(count)
            ] = (
                indicator_adjusted_to_plot[
                    "sub_" + indicator_name + "_adjusted_" + limit
                ]
                + indicator_adjusted_to_plot[
                    "sub_" + indicator_name + "_adjusted_" + str(count - 1)
                ]
            )

        count += 1

    fig, axs = plt.subplots(figsize=plotting_caracteristics["figure_size"])
    list_colors = ["red", "blue", "green", "brown", "yellow", "purple", "pink"]
    list_labels = list(dict_limits_config.keys())

    x = indicator_adjusted_to_plot.index
    for k in range(nb_limits):
        y_1 = indicator_adjusted_to_plot["sub_" + indicator_name + "_" + str(k)]
        y_2 = indicator_adjusted_to_plot[
            "sub_" + indicator_name + "_adjusted_" + str(k)
        ]
        color = list_colors[k]
        label = list_labels[k]
        axs.plot(x, y_1, color=color, linestyle="dashed", label=label)
        axs.plot(x, y_2, color=color, linestyle="dotted")

    y_1 = indicator_adjusted_to_plot[indicator_name]
    y_2 = indicator_adjusted_to_plot[indicator_name + "_adjusted"]
    color = "black"
    axs.plot(x, y_1, color=color, linestyle="solid", label=indicator_name)
    axs.plot(
        x, y_2, color=color, linestyle="dotted", label=indicator_name + "_adjusted"
    )

    axs.set_title(
        "Évolution de l'indicateur en USD courant",
        fontdict=plotting_caracteristics["font"],
    )
    axs.set_xlabel("Année", fontdict=plotting_caracteristics["font"])
    axs.set_ylabel(
        "Indicateur en USD courant", fontdict=plotting_caracteristics["font"]
    )
    plt.legend()

    plt.show()


def plot_indicator_with_one_limit(
    indicator_adjusted,
    indicator_name,
    limit,
    with_indicator=False,
    from_year=None,
    to_year=None,
    plotting_caracteristics=DEFAULT_PLOTTING_CARACTERISTICS,
):
    indicator_adjusted_to_plot = indicator_adjusted.copy()
    if from_year:
        if to_year:
            indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[
                from_year:to_year
            ].copy()
        else:
            indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[
                from_year:
            ].copy()
    elif to_year:
        indicator_adjusted_to_plot = indicator_adjusted_to_plot.loc[:to_year].copy()

    fig, axs = plt.subplots(figsize=plotting_caracteristics["figure_size"])

    x = indicator_adjusted_to_plot.index

    y_sub_indicator = indicator_adjusted_to_plot["sub_" + indicator_name + "_" + limit]
    y_sub_indicator_adjusted = indicator_adjusted_to_plot[
        "sub_" + indicator_name + "_adjusted_" + limit
    ]
    color = "red"
    axs.plot(
        x,
        y_sub_indicator,
        color=color,
        linestyle="solid",
        label="Sous-indicateur de la limite " + limit,
    )
    axs.plot(
        x,
        y_sub_indicator_adjusted,
        color=color,
        linestyle="dotted",
        label="Sous-indicateur ajusté de la limite " + limit,
    )

    if with_indicator:
        y_indicator = indicator_adjusted_to_plot[indicator_name]
        y_indicator_ajuste = indicator_adjusted_to_plot[indicator_name + "_adjusted"]
        color = "black"
        axs.plot(x, y_indicator, color=color, linestyle="solid", label=indicator_name)
        axs.plot(
            x,
            y_indicator_ajuste,
            color=color,
            linestyle="dotted",
            label=indicator_name + "_adjusted",
        )

    axs.set_title(
        "Évolution de l'indicateur en USD courant avec limite " + limit,
        fontdict=plotting_caracteristics["font"],
    )
    axs.set_xlabel("Année", fontdict=plotting_caracteristics["font"])
    axs.set_ylabel(
        "Indicateur en USD courant", fontdict=plotting_caracteristics["font"]
    )
    plt.legend()

    plt.show()
