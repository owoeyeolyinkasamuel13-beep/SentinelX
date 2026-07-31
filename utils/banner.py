"""
Banner display for SentinelX.
"""

from core.version import (
    APP_NAME,
    VERSION,
    EDITION,
    STATUS,
    TAGLINE,
)


def display_banner():
    print("=" * 60)
    print(f"{APP_NAME} {EDITION}")
    print(f"Version : {VERSION}")
    print(f"Status  : {STATUS}")
    print(f"{TAGLINE}")
    print("=" * 60)