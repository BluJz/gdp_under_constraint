from src.indicator_process import IndicatorImplementorFactory
from src.limit_process import LimitImplementorFactory, process_limits
import src.utils.plotting as plot


def process_all(dict_all_limits, indicator_name, country_code="FRA"):
    indicator_data = IndicatorImplementorFactory.get_implementor(
        indicator_name
    ).data_creation()
    indicator_data = indicator_data[country_code]
    indicator_data.rename(indicator_name, inplace=True)

    indicator_adjusted_data = process_limits(indicator_data, dict_all_limits)
    return indicator_adjusted_data


def main(country_code="FRA", dict_all_limits=None, indicator_name="gdp"):
    if dict_all_limits is None:
        dict_all_limits = {
            "water": {
                "coef": 1.0,
                "config": "water_general_wb",
                "dict_parameters": {"country_code": country_code},
            }
        }

    indicator_adjusted_data = process_all(
        dict_all_limits, indicator_name=indicator_name, country_code=country_code
    )

    indicator_adjusted_data_to_plot = indicator_adjusted_data.dropna()
    first_year_to_plot = indicator_adjusted_data_to_plot.index.min()
    last_year_to_plot = indicator_adjusted_data_to_plot.index.max()
    plot.plot_indicator_with_all_limits(
        indicator_adjusted=indicator_adjusted_data,
        indicator_name=indicator_name,
        dict_limits_config=dict_all_limits,
        from_year=first_year_to_plot,
        to_year=last_year_to_plot,
    )


if __name__ == "__main__":
    main()
