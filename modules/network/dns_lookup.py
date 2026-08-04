"""
SentinelX DNS Lookup Tool
Version: 1.1.0
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
            ip_address = socket.gethostbyname(domain)

            print_section("Lookup Result")
            print(f"Resolved IP : {ip_address}")
            print_success("DNS lookup completed successfully.")

        except socket.gaierror:
            print_error("Unable to resolve domain.")