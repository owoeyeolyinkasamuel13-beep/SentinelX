"""
SentinelX Ping Tool
Version: 1.1.0
Author: Olayinka Samuel Owoeye
Project: SentinelX Community Edition
"""

import platform
import subprocess

from modules.base import Module
from utils.display import (
    print_header,
    print_section,
    print_success,
    print_error
)

def parse_ping_output(output):
    """Parse Windows ping output."""

    data = {
    "host": "",
    "ip": "",
    "packets": "",
    "time": ""
     }
    lines = output.splitlines()

    for line in lines:

        line = line.strip()

        if line.startswith("Pinging"):

            parts = line.split()

            data["host"] = parts[1]

            if "[" in line and "]" in line:
                data["ip"] = line.split("[")[1].split("]")[0]

        elif line.startswith("Packets:"):
            data["packets"] = line

        elif line.startswith("Minimum"):
            data["time"] = line

    return data

class PingTool(Module):
    """Ping Tool Module"""

    name = "Ping Tool"
    category = "Network"
    description = "Check if a host is reachable."

    def run(self):

        print_header("PING TOOL")

        target = input("Enter IP Address or Domain: ").strip()

        if not target:
            print_error("Target cannot be empty.")
            return

        print_section("Target")
        print(f"Host : {target}")

        system = platform.system()

        if system == "Windows":
            command = ["ping", "-n", "4", target]
        else:
            command = ["ping", "-c", "4", target]

        print_section("Ping Status")
        print("Sending 4 ICMP Echo Requests...\n")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            output = result.stdout


            ping_data = parse_ping_output(output)

            print_section("Ping Summary")

            print(f"Host       : {ping_data['host']}")
            print(f"IP Address : {ping_data['ip']}")
            print()

            print(ping_data["packets"])
            print(ping_data["time"])

           

            print_success("Ping operation completed.")

          
        except Exception as e:
            print_error(f"ping failed: {e}")
            return
        input("\nPress Enter to return to the main menu...")