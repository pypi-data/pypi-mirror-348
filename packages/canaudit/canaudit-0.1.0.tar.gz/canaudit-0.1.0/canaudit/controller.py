"""
controller.py

Orchestrates the end-to-end audit workflow:
1. Loads CAN trace data from supported formats
2. Runs selected audit modules
3. Generates a report of findings

Used by CLI and scripting interfaces.
"""

import logging

from canaudit import audit_manager, parser, reports


class AuditController:
    def __init__(self, module_names: list[str], config: dict = {}):
        self.state = "idle"
        self.module_names = module_names
        self.config = config
        self.messages = None
        self.results = None

    def load_trace(self, input_path: str):
        logging.info(f"[Controller] Loading trace from {input_path}")
        self.messages = parser.load_trace(input_path)
        self.state = "parsed"

    def run_audits(self):
        if self.state != "parsed":
            raise RuntimeError("Trace must be loaded before running audits.")
        logging.info(f"[Controller] Running audits: {self.module_names}")
        self.results = audit_manager.run_audits(
            self.messages, enabled_modules=self.module_names, config=self.config
        )
        self.state = "audited"

    def generate_report(self, output_path: str):
        if self.state != "audited":
            raise RuntimeError("Audits must be completed before generating report.")
        logging.info(f"[Controller] Generating report to {output_path}")
        reports.generate_html_report(self.results, output_path)
        self.state = "reported"

    def run_all(self, input_path: str, output_path: str):
        self.load_trace(input_path)
        self.run_audits()
        self.generate_report(output_path)
