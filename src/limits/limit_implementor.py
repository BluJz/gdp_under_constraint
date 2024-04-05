from abc import ABC, abstractmethod


class LimitImplementor(ABC):
    def __init__(self, config_name, limit_name, dict_parameters=None):
        self.config_name = config_name
        self.limit_name = limit_name
        self.data_path = None
        self.dict_parameters = dict_parameters

    @abstractmethod
    def data_creation(self):
        pass

    @abstractmethod
    def f(self, point, dict_parameters=None):
        pass

    @abstractmethod
    def calculate(self, indicator):
        pass
