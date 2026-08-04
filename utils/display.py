"""
Display utilities for SentinelX.
"""


def print_header(title):
    """Display a standard SentinelX header."""

    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_section(title):
    """Display a section title."""

    print(f"\n{title}")
    print("-" * 60)


def print_success(message):
    """Display a success message."""

    print(f"[+] {message}")


def print_error(message):
    """Display an error message."""

    print(f"[-] {message}")


def print_table_header():
    """Display the standard table header."""

    print("-" * 60)
    print(f"{'PORT':<10}{'STATE':<12}{'SERVICE'}")
    print("-" * 60)


def print_separator():
    """Display a separator line."""

    print("-" * 60)