import importlib

CONFIG_MAP = {
    "gdp": {
        "module_name": "gdp_indicator",
        "class_name": "GDPIndicator",
    }
}


class IndicatorImplementorFactory:
    @staticmethod
    def get_implementor(indicator_name, dict_parameters=None):
        module_name = CONFIG_MAP[indicator_name]["module_name"]
        class_name = CONFIG_MAP[indicator_name]["class_name"]
        module_path = f".indicators.{module_name}"  # Assuming all limit modules are in a 'limits' package

        try:
            # Dynamically import the module
            module = importlib.import_module(module_path, package="src")
            # Get the class from the module
            cls = getattr(module, class_name)
            # Instantiate the class and return the instance
            return cls(
                indicator_name, dict_parameters
            )  # Assuming the constructor doesn't require arguments; otherwise, adjust as needed
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Could not import {indicator_name} due to {e}")
