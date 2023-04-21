# API, common or useful methods for use in python based plugins

class NumericalMethods:
    def __init__(self):
        pass

    @staticmethod
    def mean(values: list[float | int]) -> float | int:
        return sum(values) / len(values)
