import importlib
import os
from types import ModuleType

from core.utils import log_plugin as log, log_error_plugins as log_error


def main_plugin_launcher_mode1(file_path, values):
    plugin = get_function_python_plugin(file_path=file_path)
    if plugin:
        plugin.main_plugin(values)


def get_function_python_plugin(file_path):
    plugin_path = file_path.split('/')
    plugin_path = plugin_path[-4] + "." + plugin_path[-3] + "." + plugin_path[-1].removesuffix(".py")
    log(f"attempt to import dynamically (python): {plugin_path}")
    plugin = import_plugin(plugin_path)
    if plugin:
        return plugin
    return None


def import_plugin(plugin_file_path: str) -> None | ModuleType:
    try:
        return importlib.import_module(name=plugin_file_path)
    except ImportError:
        log_error(f"Import module: {str}")
        return None


def get_specific_config_paths(basepath: str):
    path_list = []
    dir_list = os.listdir(basepath)
    for dir_name in dir_list:
        dir_path = basepath + "/" + dir_name
        if os.path.isdir(dir_path):
            file_list = os.scandir(dir_path)
            for file in file_list:
                if ".ini" in file.name:
                    file_path = dir_path + "/" + file.name
                    path_list.append(file_path)
                    log(f"New config file found: {file_path}")
    return path_list


def get_path_conf_global(basepath: str):
    file_path = basepath + "/" + "config_plugins.ini"
    return file_path
