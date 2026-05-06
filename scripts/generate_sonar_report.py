from fpdf import FPDF
from datetime import datetime
import requests
import os

# ==============================
# SONARCLOUD CONFIG
# ==============================

SONAR_TOKEN = os.getenv("SONAR_TOKEN")

PROJECT_KEY = "kurapatiharshith_TO-GENERATE-A-SECURE-FRAMEWORK-IN-IDENTITY-MANAGEMENT-USING-BLOCKCHAIN-"

PROJECT_NAME = "Blockchain Identity Management Framework"

# ==============================
# FETCH PROJECT METRICS
# ==============================

metrics_url = f"https://sonarcloud.io/api/measures/component?component={PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,security_hotspots"

metrics_response = requests.get(
    metrics_url,
    auth=(SONAR_TOKEN, "")
)

metrics_data = metrics_response.json()

measures = metrics_data["component"]["measures"]

metrics = {}

for item in measures:
    metrics[item["metric"]] = item["value"]

# ==============================
# FETCH ISSUES
# ==============================

issues_url = f"https://sonarcloud.io/api/issues/search?componentKeys={PROJECT_KEY}&ps=20"

issues_response = requests.get(
    issues_url,
    auth=(SONAR_TOKEN, "")
)

issues_data = issues_response.json()

issues = issues_data.get("issues", [])

# ==============================
# PDF SETUP
# ==============================

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ==============================
# TITLE
# ==============================

pdf.set_font("Arial", "B", 20)
pdf.cell(200, 10, "SonarCloud Security Analysis Report", ln=True, align="C")

pdf.ln(5)

pdf.set_font("Arial", "", 12)
pdf.cell(200, 10, f"Project Name: {PROJECT_NAME}", ln=True)
pdf.cell(200, 10, f"Project Key: {PROJECT_KEY}", ln=True)
pdf.cell(200, 10, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

pdf.ln(10)

# ==============================
# OVERALL STATUS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Overall Status", ln=True)

pdf.set_font("Arial", "", 12)

status_data = [
    ("Bugs", metrics.get("bugs", "0")),
    ("Vulnerabilities", metrics.get("vulnerabilities", "0")),
    ("Code Smells", metrics.get("code_smells", "0")),
    ("Coverage", metrics.get("coverage", "0")),
    ("Duplications", metrics.get("duplicated_lines_density", "0")),
    ("Security Hotspots", metrics.get("security_hotspots", "0")),
]

for key, value in status_data:
    pdf.cell(80, 8, f"{key}:", border=1)
    pdf.cell(50, 8, str(value), border=1, ln=True)

pdf.ln(10)

# ==============================
# DETAILED FINDINGS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Detailed Findings", ln=True)

for issue in issues:

    pdf.set_font("Arial", "B", 12)

    issue_key = issue.get("key", "N/A")

    pdf.cell(200, 8, f"Issue ID: {issue_key}", ln=True)

    pdf.set_font("Arial", "", 11)

    details = [
        ("Severity", issue.get("severity", "N/A")),
        ("Type", issue.get("type", "N/A")),
        ("Rule", issue.get("rule", "N/A")),
        ("Status", issue.get("status", "N/A")),
        ("Message", issue.get("message", "N/A")),
        ("File", issue.get("component", "N/A")),
        ("Line", str(issue.get("line", "N/A"))),
    ]

    for key, value in details:
        pdf.multi_cell(0, 8, f"{key}: {value}")

    pdf.ln(5)

# ==============================
# CONCLUSION
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Conclusion", ln=True)

pdf.set_font("Arial", "", 12)

conclusion = """
This report was automatically generated from SonarCloud scan results.
Immediate remediation of Critical and Major findings is recommended.
"""

pdf.multi_cell(0, 8, conclusion)

# ==============================
# SAVE PDF
# ==============================

pdf.output("sonar-report.pdf")

print("Dynamic SonarCloud PDF Report Generated Successfully")
