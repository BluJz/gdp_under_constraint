from .indicator_implementor import IndicatorImplementor
import pandas as pd


class GDPIndicator(IndicatorImplementor):
    def __init__(self, indicator_name, dict_parameters=None):
        super().__init__(indicator_name, dict_parameters=dict_parameters)

        self.data_path = "data/pib/pib/pib.csv"

    def data_creation(self):
        data = pd.read_csv(self.data_path, header=2)
        data.drop(
            columns=["Indicator Name", "Indicator Code", "Unnamed: 67", "Country Name"],
            inplace=True,
        )
        data.rename(columns={"Country Code": "country_code"}, inplace=True)

        data = data.melt(
            id_vars=["country_code"], var_name="year", value_name=self.indicator_name
        )
        data = data.pivot(
            index="year", columns="country_code", values=self.indicator_name
        )

        data.index = data.index.astype(int)
        data = data / (10**9)

        return data


if __name__ == "__main__":
    print("Testing import")
