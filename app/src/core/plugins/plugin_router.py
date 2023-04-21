from core.plugins.plugin_support import main_plugin_launcher_mode1
from core.plugins.plugins_objects import Plugins
from core.utils import log_plugin


class PluginRouter:
    links: list[dict]
    plugins: Plugins

    def __init__(self, plugins: Plugins):
        self.links = []
        self.plugins = plugins

    def link(self, index, type_values, name):
        # sanity check not yet implemented
        log_plugin(f"name of plugin to add: {name}")
        file_path = self.plugins.get_file_path(name=name)
        log_plugin(f"file path plugin to add: {file_path} for index: {index}")
        self.links.append(dict(index=index, file_path=file_path, name=name))

    def dispatch(self, index, values):
        self.dispatch_by_links(index=index, values=values)

    def dispatch_by_links(self, index, values):
        plugin_name = self.__get_name_by_index(index=index)
        plugin = self.plugins.get_plugin_by_name(name=plugin_name)
        if plugin:
            plugin.execute(values=values)

    def __get_name_by_index(self, index):
        for link in self.links:
            if link["index"] == index:
                return link["name"]
        return ""

    # deprecated method
    def dispatch_by_links_deprecated(self, index, values):
        file_path = self.__get_file_path(index=index)
        log_plugin(f"file path plugin to dispatch: {file_path}")
        try:
            main_plugin_launcher_mode1(file_path=file_path, values=values)
        except ImportError:
            pass

    def __get_file_path(self, index):
        for data in self.links:
            log_plugin(data["file_path"])
            if data["index"] == index:
                return data["file_path"]
        return ""

    def reset(self):
        self.links.clear()


class PluginRouterFront:
    router: PluginRouter
    plugins: Plugins

    def __init__(self, plugins):
        self.router = PluginRouter(plugins)
        self.plugins = plugins

    def plugin_link(self, index, type_values, name):
        # self.plugins.display_info()
        self.router.link(index, type_values, name)

    def plugin_dispatch(self, index, values):
        self.router.dispatch(index, values)

    def plugin_reset(self):
        self.router.reset()
