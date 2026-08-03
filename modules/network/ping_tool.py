"""
SentinelX Ping Tool
"""

import platform
import subprocess

from modules.base import Module


class PingTool(Module):
    """Ping Tool Module"""

    name = "Ping Tool"
    category = "Network"
    description = "Check if a host is reachable."

    def run(self):

        print("\n===================================")
        print("          PING TOOL")
        print("===================================\n")

        target = input("Enter IP Address or Domain: ").strip()

        if not target:
            print("\n[-] Target cannot be empty.\n")
            return

        system = platform.system()

        if system == "Windows":
            command = ["ping", "-n", "4", target]
        else:
            command = ["ping", "-c", "4", target]

        print("\nPinging...\n")

        subprocess.run(command)