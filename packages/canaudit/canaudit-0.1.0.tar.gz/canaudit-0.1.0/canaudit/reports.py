"""
reports.py

Generates human-readable audit reports.

Currently supports:
- HTML report generation using Jinja2 templates

Output includes:
- List of audit modules run
- Detailed findings per module (if any)
"""

import logging

from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>CANaudit Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        h1 { color: #333; }
        .module { margin-bottom: 2em; }
        table { width: 100%%; border-collapse: collapse; margin-top: 1em; }
        th, td { border: 1px solid #ccc; padding: 0.5em; text-align: left; }
        th { background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>CANaudit Report</h1>
    <p>Modules run: {{ modules | join(", ") }}</p>

    {% for name, findings in results.items() %}
    <div class="module">
        <h2>Module: {{ name }}</h2>
        {% if findings %}
            <table>
                <thead>
                    <tr>
                        {% for key in findings[0].keys() %}
                        <th>{{ key }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in findings %}
                    <tr>
                        {% for value in row.values() %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p>No findings reported.</p>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""


def generate_html_report(results: dict, output_path: str):
    logging.info(f"[Report] Writing report to: {output_path}")
    try:
        template = Template(HTML_TEMPLATE)
        rendered = template.render(results=results, modules=list(results.keys()))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        logging.info("[Report] Report generated successfully.")
    except Exception as e:
        logging.error(f"[Report] Failed to generate report: {e}")
        raise
