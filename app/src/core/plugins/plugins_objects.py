import subprocess
from enum import Enum
import configparser
import os

from core.plugins.plugin_support import get_function_python_plugin, get_specific_config_paths, get_path_conf_global
from core.utils import log_error_plugins as log_error
from core.utils import log_plugin as log
from core.utils import MyException


class TypePlugins(Enum):
    none = 0
    simple_values_processing = 1


class ValueType(Enum):
    none = 0
    int = 1
    float = 2


# plugin:
#   mode:
#       values: 1 or 2
#       1 for python based plugin
#       2 for compiled/binary plugin (C, C++, or rust mostly supported - but anything could work)
class Plugin:
    active: bool = True

    path: str
    path_exec: str

    name: str
    description: str
    mode: int
    type: TypePlugins
    name_data_default: str
    value_type_accepted_default: ValueType
    name_data: str = ""
    value_type_accepted: ValueType = None

    def __init__(self, path: str, name: str,
                 mode: str,
                 type_plugins: str,
                 name_data: str = "",
                 value_type_accepted_default: str = None,
                 description: str = ""):
        self.path = path
        self.name = name
        self.description = description
        self.mode = int(mode)
        if self.mode == 1:
            # file path to python file where main function of plugin is
            self.path_exec = self.path + "/" + self.name + ".py"
            # load plugin and register function main
            self.python_function_to_call = get_function_python_plugin(self.path_exec)
        elif self.mode == 2: # only works on windows for now
            self.path_exec = self.path + "/" + self.name + ".exe"
        self.type = self.__get_type(type_plugins)
        self.name_data_default = name_data
        self.value_type_accepted_default = self.__get_value_type(value_type_accepted_default)

    def execute(self, values):
        if self.active:
            if self.mode == 1:
                self.python_function_to_call.main_plugin(values)
            elif self.mode == 2:
                # call binary with values on stdin
                result = subprocess.run(self.__get_params_mode2_plugin(values=values))
                print(result.stdout)

    def __get_params_mode2_plugin(self, values: list[int | float]) -> str:
        values_str = ""
        for value in values:
            values_str += str(value) + " "
        return self.path_exec + " " + values_str

    def set_name_data(self, name_data):
        self.name_data = name_data
        return self

    def set_value_type_accepted(self, value_type_accepted: str):
        self.value_type_accepted = self.__get_value_type(value_type_accepted)
        return self

    # to convert from string value, key found in config to internal representation (Enum)
    # use in this file only
    @staticmethod
    def __get_value_type(value_type: str) -> ValueType:
        match value_type:
            case 'int':
                return ValueType.int
            case 'float':
                return ValueType.float
            case _:
                log_error(f"Value type not supported : {value_type}")
                return ValueType.none

    # to convert from string value, key found in config to internal representation (Enum)
    # use in this file only
    @staticmethod
    def __get_type(type_plugin: str) -> TypePlugins:
        match type_plugin:
            case 'simple_values_processing':
                return TypePlugins.simple_values_processing
            case _:
                log_error(f"Type of plugin not supported : {type_plugin}")
                return TypePlugins.none

    def display_info(self):
        print("******************************** PLUGIN *****************************")
        print(f"Path: {self.path}")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"mode: {self.mode}")
        print(f"name data default: {self.name_data_default}")
        print("*********************************************************************")


# class that holds all loaded plugins and that form a public interface for other parts of app
class Plugins:
    plugins: list[Plugin]

    def __init__(self):
        self.plugins = []

    def load_from_config_files(self):
        basepath = os.getcwd()
        if "serial-gui-analysis" not in basepath or not basepath.endswith("serial-gui-analysis\\src"):
            print("You have to launch application from its base folder!")
            exit(-1)

        # get all plugins conf
        log("Starting to load plugin specific conf")
        log("Bundled plugins")
        list_paths_bundled_plugins = get_specific_config_paths(basepath=basepath + "/bundled_plugins")
        self.load_specific_config(list_paths_bundled_plugins)

        log("User Plugins")
        list_paths_user_plugins = get_specific_config_paths(basepath=basepath + "/user_plugins")
        self.load_specific_config(list_paths_user_plugins)

        # self.display_info()

        # get global conf (always after because global config does not include every plugins + values here overwrite
        # defaults)
        global_conf_path = get_path_conf_global(basepath=basepath)
        self.load_global_conf(global_conf_path)

    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)

    # helper for internal class usage only
    def __lookup_by_data_name(self, name):
        for plugin in self.plugins:
            if plugin.name_data_default == name:
                return plugin
        return None

    # return file path of executable
    def get_file_path(self, name: str):
        plugin = self.__lookup_by_data_name(name)
        if plugin:
            return plugin.path_exec
        return ""

    def display_info(self):
        for plugin in self.plugins:
            plugin.display_info()

    def get_plugin_by_name(self, name: str):
        return self.__lookup_by_data_name(name=name)

    def load_specific_config(self, config_paths: list[str]):
        config = configparser.ConfigParser()
        for config_path in config_paths:
            config.read(config_path)

            pl_name = config["plugin"]["name"]

            try:  # optionnal key
                pl_desc = config["plugin"]["description"]
            except KeyError:
                pl_desc = ""

            pl_mode = config["plugin"]["mode"]
            pl_type = config["plugin"]["type"]
            pl_name_data = config["plugin"]["name_data_default"]
            pl_data_type = config["plugin"]["value_type_accepted_default"]

            log(f"Plugin file correctly loaded; {config_path}")

            try:
                plugin_path = config_path.removesuffix("config.ini")

                if int(pl_mode) == 1:
                    file_exec_path = plugin_path + pl_name + ".py"
                elif int(pl_mode) == 2:
                    file_exec_path = plugin_path + pl_name + ".exe"
                else:
                    log_error(f"plugin mode not supported {plugin_path}")
                    raise MyException(f"plugin mode not supported {plugin_path}")

                if os.path.isfile(file_exec_path) is False:
                    log_error(f"plugin file (executable) not found at {file_exec_path}")
                    raise MyException(f"plugin file not found at {plugin_path}")

            except MyException as e:
                print(e)
                log_error(f"Plugin file not correctly written; {config_path}")
            else:
                try:
                    temp = Plugin(path=plugin_path, name=pl_name, description=pl_desc, mode=pl_mode,
                                  type_plugins=pl_type,
                                  name_data=pl_name_data,
                                  value_type_accepted_default=pl_data_type)
                    # temp.display_info()
                    self.add_plugin(temp)
                    self.display_info()
                except RuntimeError:
                    log_error("Plugin not loaded in memory")

    def load_global_conf(self, global_config_path: str):
        config = configparser.ConfigParser()
        config.read(global_config_path)
        for plugin in self.plugins:
            try:
                config[plugin.name]
            except KeyError:
                plugin.active = False
                continue
            try:
                plugin.name_data_default = config[plugin.name]["name_data"]
            except KeyError:
                pass
            try:
                plugin.set_value_type_accepted(config[plugin.name]["value_type_accepted"])
            except KeyError:
                pass
