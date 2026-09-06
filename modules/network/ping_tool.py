"""
SentinelX Ping Tool
Version: 1.1.0
Author: Olayinka Samuel Owoeye
Project: SentinelX Community Edition
"""

import platform
import re
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
        "sent": None,
        "received": None,
        "loss_percent": None,
        "minimum": None,
        "maximum": None,
        "average": None,
    }

    host_match = re.search(
        r"^Pinging\s+(?P<host>[^\s\[]+)(?:\s+\[(?P<ip>[^\]]+)\])?\s+with",
        output,
        re.MULTILINE | re.IGNORECASE,
    )
    if host_match:
        data["host"] = host_match.group("host")
        data["ip"] = host_match.group("ip") or data["host"]

    packet_match = re.search(
        r"Packets:\s*Sent\s*=\s*(?P<sent>\d+),\s*"
        r"Received\s*=\s*(?P<received>\d+),.*?\((?P<loss_percent>\d+)%\s*loss\)",
        output,
        re.IGNORECASE,
    )
    if packet_match:
        data["sent"] = int(packet_match.group("sent"))
        data["received"] = int(packet_match.group("received"))
        data["loss_percent"] = int(packet_match.group("loss_percent"))

    timing_match = re.search(
        r"Minimum\s*=\s*(?P<minimum>\d+)ms,\s*"
        r"Maximum\s*=\s*(?P<maximum>\d+)ms,\s*"
        r"Average\s*=\s*(?P<average>\d+)ms",
        output,
        re.IGNORECASE,
    )
    if timing_match:
        data["minimum"] = int(timing_match.group("minimum"))
        data["maximum"] = int(timing_match.group("maximum"))
        data["average"] = int(timing_match.group("average"))

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

            lost = ""
            if ping_data["sent"] is not None and ping_data["received"] is not None:
                lost = ping_data["sent"] - ping_data["received"]

            print(
                f"Packets: Sent = {ping_data['sent']}, "
                f"Received = {ping_data['received']}, "
                f"Lost = {lost} ({ping_data['loss_percent']}% loss),"
            )
            print(
                f"Minimum = {ping_data['minimum']}ms, "
                f"Maximum = {ping_data['maximum']}ms, "
                f"Average = {ping_data['average']}ms"
            )

           

            print_success("Ping operation completed.")

          
        except Exception as e:
            print_error(f"ping failed: {e}")
            return
        input("\nPress Enter to return to the main menu...")
