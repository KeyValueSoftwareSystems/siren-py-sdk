# examples/basic_usage.py
"""Basic usage examples for the Siren SDK."""

import os
import sys

from dotenv import load_dotenv

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren import SirenClient

if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY not set.")
        sys.exit(1)

    try:
        client = SirenClient(api_key=api_key)
        print("SirenClient initialized.")
    except Exception as e:
        print(f"Initialization Error: {e}")
