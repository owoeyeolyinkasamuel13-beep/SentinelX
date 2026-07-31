"""
Module Registry

Responsible for storing and providing access to all SentinelX modules.
"""


class ModuleRegistry:
    """Stores and manages registered modules."""

    def __init__(self):
        self._modules = []

    def register(self, module):
        """Register a new module."""
        self._modules.append(module)

    def get_modules(self):
        """Return all registered modules."""
        return self._modules

    def get_module(self, index):
        """Return a module by its menu number."""
        if 1 <= index <= len(self._modules):
            return self._modules[index - 1]
        return None

    def total_modules(self):
        """Return the number of registered modules."""
        return len(self._modules)