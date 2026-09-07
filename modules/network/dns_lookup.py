"""
SentinelX DNS Lookup Tool
Version: 1.2.0
Author: Olayinka Samuel Owoeye
Project: SentinelX Community Edition
"""

import socket

from modules.base import Module
from utils.display import (
    print_header,
    print_section,
    print_success,
    print_error
)

class DNSLookup(Module):
    """DNS Lookup Module"""

    name = "DNS Lookup"
    category = "Network"
    description = "Resolve a domain name to an IP address."

    def run(self):

        print_header("DNS LOOKUP")

        domain = input("Enter Domain Name: ").strip()

        if not domain:
            print_error("Domain cannot be empty.")
            return
        
        print_section("Target")
        print(f"Domain : {domain}")

        try:
            ipv4_addresses, ipv6_addresses = self._resolve_addresses(domain)

            print_section("Lookup Result")
            self._display_addresses("IPv4 Address", ipv4_addresses)
            self._display_addresses("IPv6 Address", ipv6_addresses)
            print_success("DNS lookup completed successfully.")

        except socket.gaierror:
            print_error("Unable to resolve domain.")

    @staticmethod
    def _resolve_addresses(domain):
        """Resolve a domain and return unique IPv4 and IPv6 addresses."""

        results = socket.getaddrinfo(domain, None)
        ipv4_addresses = []
        ipv6_addresses = []

        for address_family, _, _, _, sockaddr in results:
            address = sockaddr[0]

            if address_family == socket.AF_INET and address not in ipv4_addresses:
                ipv4_addresses.append(address)
            elif address_family == socket.AF_INET6 and address not in ipv6_addresses:
                ipv6_addresses.append(address)

        return ipv4_addresses, ipv6_addresses

    @staticmethod
    def _display_addresses(address_label, addresses):
        """Display resolved addresses for an IP family."""

        if addresses:
            for address in addresses:
                print(f"{address_label}: {address}")
        else:
            print(f"{address_label}s: None found")
