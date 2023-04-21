from core import utils


class Unit:
    name: str
    index: int

    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index

    def add_record(self, record):
        pass


class Probe(Unit):
    records: list = []

    def add_record(self, record: int):
        utils.log(f"Probe record: {record} added")
        self.records.append(record)


class Data(Unit):
    type_values: str = ""
    records: list[list] = []

    def __init__(self, name: str, index: int, type_values: str):
        super().__init__(name=name, index=index)
        if type_values == "int" or "float":
            self.type_values = type_values
        else:
            utils.log_error_input('type values unsupported')

    def convert(self, values: list):
        list_converted = []
        match self.type_values:
            case 'int':
                list_converted = [int(value) for value in values]
            case 'float':
                list_converted = [float(value) for value in values]
            case _:
                pass
                # utils.log_error_input('type values unsupported')
        return list_converted

    def add_record(self, record: list):
        record = self.convert(values=record)
        utils.log(f"Data record: {record} added")
        self.records.append(record)


class UnitList:
    unit_list: list[Unit]

    def __init__(self):
        self.unit_list = []

    def add_unit(self, unit) -> bool:
        # check if there is not already one with same index or name
        if self.already_present(name=unit.name, index=unit.index):
            return False
        self.unit_list.append(unit)
        return True

    def already_present(self, name: str, index: int) -> bool:
        for unit in self.unit_list:
            if unit.name == name:
                return True
            if unit.index == index:
                return True
        return False

    def add_record(self, index: int, record):
        for unit in self.unit_list:
            if unit.index == index:
                unit.add_record(record=record)

    def reset(self):
        self.unit_list = []


class Configuration:
    probe_list: UnitList
    data_list: UnitList

    def __init__(self):
        self.probe_list = UnitList()
        self.data_list = UnitList()

    def add_probe(self, name: str, index: int):
        if self.probe_list.add_unit(Probe(name=name, index=index)):
            utils.log(f"Probe {index} : {name} added")
        else:
            utils.log_error_input("probe already configured")

    def add_probe_data(self, index: int, time: int):
        self.probe_list.add_record(index=index, record=time)

    def add_data_source(self, name: str, type_values: str, index: int):
        if self.data_list.add_unit(Data(name=name, index=index, type_values=type_values)):
            utils.log(f"Data source {index} : {name} added - {type_values} values")
        else:
            utils.log_error_input("data source already configured")

    def add_data_data(self, index: int, values: list):
        self.data_list.add_record(index=index, record=values)

    def reset(self):
        self.__reset()

    def __reset(self):
        self.probe_list.reset()
        self.data_list.reset()
