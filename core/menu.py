"""
Main menu for SentinelX.
"""


class MainMenu:
    """Displays the main menu and gets user input."""

    def display(self):
        print("\n========== MAIN MENU ==========\n")

        print("[ Network Tools ]")
        print("1. Port Scanner")
        print("2. Ping Host")
        print("3. DNS Lookup")
        print("4. WHOIS Lookup")

        print("\n[ Password & Hash Tools ]")
        print("5. Password Strength Checker")
        print("6. Hash Generator")
        print("7. Hash Verifier")

        print("\n[ Utilities ]")
        print("8. System Information")
        print("9. Report History")

        print("\n[ Settings ]")
        print("10. Settings")
        print("11. About SentinelX")

        print("\n0. Exit\n")

        return input("Select an option: ")