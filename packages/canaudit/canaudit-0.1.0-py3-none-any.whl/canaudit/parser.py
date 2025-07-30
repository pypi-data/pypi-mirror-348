"""
parser.py

High-level interface for loading CAN trace and DBC files.
Delegates to specific format loaders under `formats/`.

Supported trace formats:
- CSV
- candump (.log)

Supported DBC format:
- Vector DBC files via cantools
"""

from canaudit.formats.dbc.dbc_loader import load_dbc_file
from canaudit.formats.trace.candump_loader import load_candump_log
from canaudit.formats.trace.csv_loader import load_csv_trace


def load_trace(file_path: str):
    if file_path.endswith(".csv"):
        return load_csv_trace(file_path)
    elif file_path.endswith(".log"):
        return load_candump_log(file_path)
    else:
        raise ValueError(f"Unsupported trace file format: {file_path}")


def load_dbc(path: str):
    return load_dbc_file(path)
