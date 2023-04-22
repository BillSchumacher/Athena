import os
import importlib
import pkgutil

class PluginManager:
    def __init__(self, plugin_base_class, plugin_package):
        self.plugin_base_class = plugin_base_class
        self.plugin_package = plugin_package
        self.plugins = []

    def discover_plugins(self):
        plugins_path = os.path.dirname(self.plugin_package.__file__)
        for (_, module_name, _) in pkgutil.iter_modules([plugins_path]):
            module = importlib.import_module(f"{self.plugin_package.__name__}.{module_name}")
            for plugin_class in module.__dict__.values():
                if (isinstance(plugin_class, type) and
                        issubclass(plugin_class, self.plugin_base_class) and
                        plugin_class != self.plugin_base_class):
                    self.plugins.append(plugin_class())

    def process_input(self, input_text):
        for plugin in self.plugins:
            if plugin.can_process(input_text):
                return plugin.process(input_text)
        return None
