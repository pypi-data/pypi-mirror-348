"""
audit_manager.py

Manages the execution of audit modules.

- Dynamically loads and runs enabled modules
- Passes configuration and message data
- Aggregates results for reporting
"""

import logging

from canaudit.modules import timing_audit

AVAILABLE_MODULES = {
    "timing": timing_audit.TimingAudit,
    # scale up with more modules as needed
}


def run_audits(messages, enabled_modules: list[str], config: dict = {}):
    """
    Runs selected audit modules on the CAN message data.
    Returns a dictionary of results keyed by module name.
    """
    results = {}

    for module_name in enabled_modules:
        if module_name not in AVAILABLE_MODULES:
            logging.warning(f"[AuditManager] Unknown module: {module_name}, skipping.")
            continue

        logging.info(f"[AuditManager] Running module: {module_name}")
        module_class = AVAILABLE_MODULES[module_name]
        module_instance = module_class(config.get(module_name, {}))
        findings = module_instance.run(messages)

        results[module_name] = findings

    return results
