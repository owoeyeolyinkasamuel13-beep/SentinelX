"""
SentinelX Port Scanner
Version: 1.0
Author: Olayinka Samuel Owoeye
Project: SentinelX Community Edition
"""

import socket
from modules.base import Module
from data.services import COMMON_PORTS
from utils.display import (
    print_header,
    print_section,
    print_table_header,
    print_separator,
    print_error
)

class PortScanner(Module):
    """Port Scanner Module"""

    name = "Port Scanner"
    category = "Network"
    description = "Scan a target for open TCP ports."

    def run(self):
        print_header("PORT SCANNER")

        target = input("Enter an IP Address or Domain: ").strip()

        if not target:
            print_error("Target cannot be empty.")
            return

        try:
            ip_address = socket.gethostbyname(target)

            print_section("Target Information")
            print(f"Host : {target}")
            print(f"IP   : {ip_address}")
            print_section("Scanning")
            print ("Scanning ports 1-100...")

            open_ports = []

            for port in range(1, 101):

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                sock.settimeout(0.5)

                result = sock.connect_ex((ip_address, port))

                if result == 0:
                    service = COMMON_PORTS.get(port, "Unknown Service")
                    
                    open_ports.append({
                        "port": port,
                        "service": service
                    })

                sock.close()

            print_section("Scan Complete")

            if open_ports:
                print_header("PORT SCAN RESULTS")
                print_table_header()

                for port_info in open_ports:
                     print(f"{port_info['port']:<10}{'OPEN':<12}{port_info['service']}")

                print_separator()
                print(f"Total Open Ports : {len(open_ports)}")

            else:
                 print_error("No open ports found.")

        except socket.gaierror:
            print_error("Unable to resolve the target.")
            print("Please enter a valid IP address or domain.")