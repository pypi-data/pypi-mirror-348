"""
dbc_loader.py

Loads and parses Vector DBC files using cantools.

Returns a `cantools.database.Database` object.
"""

import cantools


def load_dbc_file(path: str):
    """Load a DBC file using cantools."""
    return cantools.database.load_file(path)
