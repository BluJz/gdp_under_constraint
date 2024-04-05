from .limit_implementor import LimitImplementor
from ..utils.f_base import linear_interpolation
import pandas as pd


class WaterGeneralWBLimit(LimitImplementor):
    def __init__(self, config_name, limit_name, dict_parameters=None):
        super().__init__(config_name, limit_name, dict_parameters=dict_parameters)

        self.data_path = "data/eau/eau.csv"

    def data_creation(self):
        data = pd.read_csv(self.data_path, header=2)
        data.drop(
            columns=["Indicator Name", "Indicator Code", "Unnamed: 68", "Country Name"],
            inplace=True,
        )
        data.rename(columns={"Country Code": "country_code"}, inplace=True)

        data = data.melt(id_vars=["country_code"], var_name="year", value_name="water")
        data = data.pivot(index="year", columns="country_code", values="water")

        data.index = data.index.astype(int)
        data = data / 100

        return data

    def f(self, point):
        if point is None:
            return None

        list_points = [(0.5, 1), (0.7, 0.8), (0.8, 0.7), (0.9, 0.5), (1, 0)]
        if self.dict_parameters:
            if "list_points" in self.dict_parameters.keys():
                list_points = self.dict_parameters["list_points"]
        result = linear_interpolation(point, list_points)
        return result

    def calculate(self, indicator):
        indicator_name = indicator.name
        data = self.data_creation()
        try:
            country_code = self.dict_parameters["country_code"]
        except KeyError as e:
            print(f"Country code not specified for limit: {self.limit_name}")

        data = data[country_code]
        data.rename("water", inplace=True).to_frame()
        df = pd.concat([data, indicator], axis=1)

        def adjustment(row):
            if pd.isna(row["water"]):
                return None
            else:
                return self.f(row["water"]) * row[indicator_name]

        indicator_adjusted = df.apply(adjustment, axis=1)

        return indicator_adjusted
