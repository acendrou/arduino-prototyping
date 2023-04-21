# Permissive parser, not everything is checked, and it is very sensible to malformed input lots of paths or only
# logged through basic logger, but for hard requirements there is a specific logger: log_error_input hard
# requirements are mostly checked in the backend storage - in folder serial_objects example of hard requirements:
# there can't be two or more probes with the number/id


from multiprocessing import Pipe


from core.plugins.plugin_router import PluginRouterFront
from core.plugins.plugins_objects import Plugins
from core.serial_objects.configuration import Configuration

from core.utils import log


def parse_entrypoint(serial_input: Pipe):
    log("Start parser")
    config = Configuration()
    plugins_loaded = Plugins()
    plugins_loaded.load_from_config_files()

    parser = Parser(config=config, plugins_loaded=plugins_loaded)
    while True:
        if serial_input.poll(timeout=1):
            line = serial_input.recv()
            print(line)
            print("Line received")
            parser.start_parsing(line)


class Parser:
    def __init__(self, config: Configuration, plugins_loaded: Plugins):
        self.config = config
        self.router = PluginRouterFront(plugins_loaded)

    def start_parsing(self, line: str):
        first_character: str = ""
        try:
            first_character = line[0]
        except IndexError:
            log("error line - first character not present")
        match first_character:
            case '!':
                log("RESET")
                self.reset_logic()
            case '>':
                log("Breakpoint")
                self.breakpoint_logic()
            case '#':
                log("configuration")
                self.configuration_parsing(line)
            case '&':
                log("probe data")
                self.probe_data_parsing(line)
            case '+':
                log("data records")
                self.data_data_parsing(line)
            case '=':
                log("debug entry")
                self.debug_data_parsing(line)
            case _:
                log("PARSING START: WARN - unrecognised or not yet supported/implemented feature")
                self.external_log_logic(line)

    # ************************************* PARSING
    def configuration_parsing(self, line: str):
        key = line[1]
        match key:
            case '&':
                log("probe configuration")
                conf = line[2:]
                conf = conf.split(':')
                self.configuration_probe_logic(index=int(conf[0]), name=conf[1])
            case '%':
                log("data configuration")
                conf = line[2:]
                conf = conf.split(':')
                self.configuration_data_logic(index=int(conf[0]), type_values=conf[1], name=conf[2])
            case _:
                log("configuration key unrecognised")

    def probe_data_parsing(self, line: str):
        log("probe data record")
        line = line[1:]
        info = line.split(':')
        self.probe_data_logic(index=int(info[0]), record=int(info[1]))

    def data_data_parsing(self, line: str):
        log("data record")
        line = line[1:]
        info = line.split(':')
        values = info[1].split(';')[:-1]
        self.data_data_logic(index=int(info[0]), record=values)

    def debug_data_parsing(self, line: str):
        pass

    # ************************************* LOGIC

    def reset_logic(self):
        self.config.reset()
        self.router.plugin_reset()

    def breakpoint_logic(self):
        pass

    def configuration_probe_logic(self, index: int, name: str):
        self.config.add_probe(index=index, name=name)

    def configuration_data_logic(self, index: int, type_values: str, name: str):
        self.config.add_data_source(index=index, type_values=type_values, name=name)
        self.router.plugin_link(index=index, type_values=type_values, name=name)

    def probe_data_logic(self, index: int, record: int):
        self.config.add_probe_data(index=index, time=record)

    def data_data_logic(self, index: int, record: list):
        self.config.add_data_data(index=index, values=record)
        self.router.plugin_dispatch(index=index, values=record)

    def data_debug_logic(self):
        pass

    def external_log_logic(self, line: str):
        pass
