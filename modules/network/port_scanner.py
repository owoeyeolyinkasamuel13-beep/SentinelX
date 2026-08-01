"""
SentinelX Port Scanner
Version: 1.0
"""

import socket
from modules.base import Module
from data.services import COMMON_PORTS


class PortScanner(Module):
    """Port Scanner Module"""

    name = "Port Scanner"
    category = "Network"
    description = "Scan a target for open TCP ports."

    def run(self):
        print("\n===================================")
        print("         PORT SCANNER")
        print("===================================\n")

        target = input("Enter an IP Address or Domain: ").strip()

        if not target:
            print("\n[-] Target cannot be empty.\n")
            return

        try:
            ip_address = socket.gethostbyname(target)

            print("\nTarget Information")
            print("------------------")
            print(f"Host : {target}")
            print(f"IP   : {ip_address}")
            print("\nScanning ports 1 - 100...\n")

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

            print("\n===================================")
            print("Scan Complete")
            print("===================================")

            if open_ports:
                 print("\n=========================================")
                 print("         PORT SCAN RESULTS")
                 print("=========================================")
                 print(f"{'PORT':<10}{'STATE':<10}{'SERVICE'}")
                 print("-" * 40)

                 for result in open_ports:
                     print(f"{result['port']:<10}{'OPEN':<10}{result['service']}")

                 print("-" * 40)
                 print(f"Total Open Ports : {len(open_ports)}")

            else:
                 print("\nNo open ports found.")

        except socket.gaierror:
            print("\n[-] Unable to resolve the target.")
            print("Please enter a valid IP address or domain.\n")