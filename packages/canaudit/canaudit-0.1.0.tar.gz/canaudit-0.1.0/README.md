# CANaudit
A stand-alone, offline, and OS-agnostic CAN security analysis tool.

## Usage
1. ensure you have Python 3 installed (v3.10 recommended).
1. 
1. Install package
```pip install canaudit```

## Known limitations

The accuracy of CAN trace data depends on the logging tool and hardware used.
- Software-based loggers (e.g., `candump`, USB-CAN) may introduce timestamp noise or latency.
- Message loss or jitter can affect the precision of timing-based audits.
- For critical analysis, use timestamped hardware interfaces and synchronized logging (e.g., [STM32G474RE](https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html), FPGAs).

CANaudit provides best-effort analysis and may produce **false positives or negatives on inaccurate logs**.

## Contribution

### Development Setup

1. Clone this repo.
2. If not installed, [Install Poetry](https://python-poetry.org/docs/#installation) (I use v2.1.3).
3. Install dependencies and enable development environment.
4. Enable pre-commit hooks (recommended).

### Run example

assuming your dev env is all set up. run the following command:
```
C:\git\CANaudit [main ≡ +0 ~2 -0 ~]> poetry run python scripts/analyze.py
INFO:root:[Controller] Loading trace from examples/sample_trace.log
INFO:root:[Controller] Running audits: ['timing']
INFO:root:[AuditManager] Running module: timing
INFO:root:[Controller] Generating report to reports/sample_report.html
INFO:root:[Report] Writing report to: reports/sample_report.html
INFO:root:[Report] Report generated successfully.

>> Report generated: file:///C%3A/git/CANaudit/reports/sample_report.html
```