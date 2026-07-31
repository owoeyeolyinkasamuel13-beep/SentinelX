"""
SentinelX Port Scanner
"""

import socket

from modules.base import Module


class PortScanner(Module):

    name = "Port Scanner"
    category = "Network"
    description = "Scan a target for open TCP ports."

    def run(self):

        print("\n===================================")
        print("         PORT SCANNER")
        print("===================================\n")

        target = input("Enter an IP Address or Domain: ").strip()

        try:
            ip = socket.gethostbyname(target)

        except socket.gaierror:
            print("\n[-] Invalid host or domain.\n")
            return

        print(f"\nTarget IP : {ip}")
        print("Scanning ports 1 - 100...\n")

        open_ports = []

        for port in range(1, 101):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(0.5)

            result = sock.connect_ex((ip, port))

            if result == 0:
                print(f"[OPEN] Port {port}")
                open_ports.append(port)

            sock.close()

        print("\n===================================")
        print("Scan Complete")
        print("===================================")

        if open_ports:
            print(f"\nOpen Ports Found: {len(open_ports)}")
        else:
            print("\nNo open ports found.")