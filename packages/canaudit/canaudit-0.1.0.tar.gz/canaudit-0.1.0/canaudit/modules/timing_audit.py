"""
timing_audit.py

Dummy audit module that simulates timing anomaly detection.

Returns fake findings on every 100th message as an example.
"""

import pandas as pd

from canaudit.core.base import AuditModule


class TimingAudit(AuditModule):
    name = "timing"
    description = "Dummy timing audit for testing"

    def run(self, messages: pd.DataFrame) -> list[dict]:
        # Dummy logic: flag every 100th message as "delayed"
        findings = []
        for i in range(0, len(messages), 100):
            row = messages.iloc[i]
            findings.append(
                {
                    "timestamp": row["timestamp"],
                    "id": row["id"],
                    "issue": "irregular timing (simulated)",
                    "severity": "low",
                }
            )

        return findings
