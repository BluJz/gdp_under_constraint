import importlib

CONFIG_MAP = {
    "water_general_wb": {
        "module_name": "water_general_wb_limit",
        "class_name": "WaterGeneralWBLimit",
    }
}


class LimitImplementorFactory:
    @staticmethod
    def get_implementor(config_name, limit_name, dict_parameters=None):
        module_name = CONFIG_MAP[config_name]["module_name"]
        class_name = CONFIG_MAP[config_name]["class_name"]
        module_path = f".limits.{module_name}"  # Assuming all limit modules are in a 'limits' package

        try:
            # Dynamically import the module
            module = importlib.import_module(module_path, package="src")
            # Get the class from the module
            cls = getattr(module, class_name)
            # Instantiate the class and return the instance
            return cls(
                config_name, limit_name, dict_parameters
            )  # Assuming the constructor doesn't require arguments; otherwise, adjust as needed
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Could not import {config_name} due to {e}")


def process_limits(
    indicator,
    dict_all_limits,
):
    """Outputs all the calculations under certain limit configurations.
    Note that the configuration specifies the function f and its segmentation but does not specify parameters a priori.

    Args:
        pib_total (pd.DataFrame): index 'Year' and column 'PIB'
        dict_limits_config (dict): format {"limit_1": {"coef": 1, "config": "config_limit_1"}}. Sum of coef must equal 1.
        croissance_reelle (_type_, optional): _description_. Defaults to None.
    """
    indicator_name = indicator.name
    indicator_adjusted = indicator.to_frame()

    for limit_name in dict_all_limits.keys():
        dict_limit = dict_all_limits[limit_name]
        sub_indicator = indicator_adjusted.apply(
            lambda row: row[indicator_name] * dict_limit["coef"], axis=1
        ).to_frame(name="sub_" + indicator_name)

        if "dict_parameters" in dict_limit.keys():
            dict_parameters = dict_limit["dict_parameters"]
        else:
            dict_parameters = None

        limit_implementor = LimitImplementorFactory.get_implementor(
            config_name=dict_limit["config"],
            limit_name=limit_name,
            dict_parameters=dict_parameters,
        )
        sub_indicator_adjusted = limit_implementor.calculate(indicator)

        indicator_adjusted["sub_" + indicator_name + "_" + limit_name] = sub_indicator
        indicator_adjusted["sub_" + indicator_name + "_adjusted_" + limit_name] = (
            sub_indicator_adjusted
        )

    adjusted_keys = [
        "sub_" + indicator_name + "_" + key for key in dict_all_limits.keys()
    ]
    indicator_adjusted[indicator_name + "_adjusted"] = indicator_adjusted[
        adjusted_keys
    ].sum(axis=1)

    return indicator_adjusted
