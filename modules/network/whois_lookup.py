"""RDAP-backed public domain registration lookup for SentinelX."""

import json
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from modules.base import Module
from utils.display import print_error, print_header, print_section, print_success


class WHOISLookup(Module):
    """Retrieve public domain registration details through RDAP."""

    name = "WHOIS Lookup"
    category = "Network"
    description = "Retrieve public domain registration information using RDAP."

    BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
    TIMEOUT_SECONDS = 10
    USER_AGENT = "SentinelX-Community-Edition/1.0"

    def run(self):
        """Prompt for a domain and display selected public RDAP data."""

        print_header("WHOIS / RDAP LOOKUP")

        target = input("Enter Domain Name: ")

        try:
            domain = self.normalize_domain(target)
        except ValueError as error:
            print_error(str(error))
            return

        print_section("Target")
        print(f"Domain : {domain}")

        try:
            endpoint = self.get_rdap_endpoint(domain)
            record = self.fetch_json(f"{endpoint}domain/{quote(domain, safe='')}")
            details = self.parse_record(record)
        except HTTPError as error:
            if error.code == 404:
                print_error("Domain/RDAP record not found.")
            else:
                print_error(f"RDAP service returned HTTP {error.code}.")
            return
        except (URLError, TimeoutError, socket.timeout) as error:
            print_error(f"Unable to contact the RDAP service: {error.reason if isinstance(error, URLError) else error}")
            return
        except json.JSONDecodeError:
            print_error("The RDAP service returned invalid JSON.")
            return
        except ValueError as error:
            print_error(str(error))
            return

        self.display_record(details)
        print_success("RDAP lookup completed successfully.")

    @staticmethod
    def normalize_domain(target):
        """Return a normalized ASCII domain suitable for RDAP queries."""

        domain = target.strip().rstrip(".")
        if not domain:
            raise ValueError("Domain cannot be empty.")
        if len(domain) > 253 or "/" in domain or ":" in domain:
            raise ValueError("Please enter a valid domain name.")

        try:
            labels = domain.split(".")
            if any(not label for label in labels):
                raise ValueError
            ascii_labels = [label.encode("idna").decode("ascii") for label in labels]
        except (UnicodeError, ValueError):
            raise ValueError("Please enter a valid domain name.") from None

        if any(
            len(label) > 63
            or label.startswith("-")
            or label.endswith("-")
            or not all(character.isalnum() or character == "-" for character in label)
            for label in ascii_labels
        ):
            raise ValueError("Please enter a valid domain name.")

        return ".".join(ascii_labels).lower()

    def get_rdap_endpoint(self, domain):
        """Find the authoritative RDAP service from IANA's DNS bootstrap."""

        bootstrap = self.fetch_json(self.BOOTSTRAP_URL)
        services = bootstrap.get("services")
        if not isinstance(services, list):
            raise ValueError("The RDAP bootstrap response was unexpected.")

        labels = domain.split(".")
        for start in range(len(labels)):
            suffix = ".".join(labels[start:])
            for service in services:
                if not isinstance(service, list) or len(service) != 2:
                    continue
                suffixes, urls = service
                if suffix not in suffixes or not isinstance(urls, list):
                    continue
                for url in urls:
                    if isinstance(url, str) and url.startswith("https://"):
                        return url.rstrip("/") + "/"

        raise ValueError("No public RDAP service was found for this domain.")

    def fetch_json(self, url):
        """Fetch and decode a JSON document with a bounded network timeout."""

        request = Request(url, headers={"User-Agent": self.USER_AGENT, "Accept": "application/rdap+json, application/json"})
        with urlopen(request, timeout=self.TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")

        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("The RDAP service returned an unexpected response.")
        return data

    @staticmethod
    def parse_record(record):
        """Extract a small, non-contact-information subset of an RDAP record."""

        domain_name = record.get("ldhName") or record.get("unicodeName")
        if not isinstance(domain_name, str):
            raise ValueError("The RDAP record did not include a domain name.")

        details = {
            "domain_name": domain_name,
            "statuses": WHOISLookup._string_list(record.get("status")),
            "registrar": WHOISLookup._registrar_name(record.get("entities")),
            "registration": WHOISLookup._event_date(record.get("events"), "registration"),
            "expiration": WHOISLookup._event_date(record.get("events"), "expiration"),
            "nameservers": WHOISLookup._nameservers(record.get("nameservers")),
        }
        return details

    @staticmethod
    def _string_list(value):
        return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []

    @staticmethod
    def _event_date(events, action):
        if not isinstance(events, list):
            return None
        for event in events:
            if isinstance(event, dict) and event.get("eventAction") == action:
                date = event.get("eventDate")
                return date if isinstance(date, str) else None
        return None

    @staticmethod
    def _registrar_name(entities):
        if not isinstance(entities, list):
            return None
        for entity in entities:
            if not isinstance(entity, dict) or "registrar" not in entity.get("roles", []):
                continue
            vcard = entity.get("vcardArray")
            if isinstance(vcard, list) and len(vcard) > 1 and isinstance(vcard[1], list):
                for field in vcard[1]:
                    if isinstance(field, list) and len(field) > 3 and field[0] == "fn" and isinstance(field[3], str):
                        return field[3]
            handle = entity.get("handle")
            return handle if isinstance(handle, str) else None
        return None

    @staticmethod
    def _nameservers(nameservers):
        if not isinstance(nameservers, list):
            return []
        values = []
        for nameserver in nameservers:
            if not isinstance(nameserver, dict):
                continue
            name = nameserver.get("ldhName") or nameserver.get("unicodeName")
            if isinstance(name, str):
                values.append(name)
        return values

    @staticmethod
    def display_record(details):
        """Display extracted public RDAP data without registrant contact data."""

        print_section("Registration Information")
        print(f"Domain Name  : {details['domain_name']}")
        print(f"Status       : {', '.join(details['statuses']) or 'Not available'}")
        print(f"Registrar    : {details['registrar'] or 'Not available'}")
        print(f"Registration : {details['registration'] or 'Not available'}")
        print(f"Expiration   : {details['expiration'] or 'Not available'}")

        print_section("Nameservers")
        if details["nameservers"]:
            for nameserver in details["nameservers"]:
                print(f"- {nameserver}")
        else:
            print("Not available")
