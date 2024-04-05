from abc import ABC, abstractmethod


class IndicatorImplementor(ABC):
    def __init__(self, indicator_name, dict_parameters=None):
        self.indicator_name = indicator_name
        self.data_path = None
        self.dict_parameters = dict_parameters

    @abstractmethod
    def data_creation(self):
        pass
