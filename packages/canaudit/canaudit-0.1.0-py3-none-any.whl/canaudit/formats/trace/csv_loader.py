"""
csv_loader.py

Parses CSV-formatted CAN trace files.

Expected columns:
- timestamp
- id
- dlc
- data

Returns a normalized pandas DataFrame.
"""

import pandas as pd


def load_csv_trace(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = [c.lower().strip() for c in df.columns]

    required = {"timestamp", "id", "dlc", "data"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")

    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df["id"] = df["id"].astype(str)
    df["dlc"] = pd.to_numeric(df["dlc"], errors="coerce")
    df["data"] = df["data"].astype(str)

    return df
