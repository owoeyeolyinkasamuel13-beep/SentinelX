"""
Base module class for all SentinelX tools.
"""


class Module:
    """Base class that every SentinelX module must inherit from."""

    option = ""
    name = ""
    category = ""

    def run(self):
        """Execute the module."""
        raise NotImplementedError("Each module must implement the run() method.")