"""
Module Manager
"""

from modules.network.port_scanner import PortScanner


class ModuleManager:
    """Registers and launches SentinelX modules."""

    def __init__(self):
        self.modules = {}
        self.register(PortScanner())

    def register(self, module):
        """Register a module."""
        self.modules[module.option] = module

    def get_module(self, option):
        """Return a module by menu option."""
        return self.modules.get(option)

    def launch(self, option):
        """Launch a registered module."""
        module = self.get_module(option)

        if module:
            module.run()
        else:
            print("\nInvalid option.\n")