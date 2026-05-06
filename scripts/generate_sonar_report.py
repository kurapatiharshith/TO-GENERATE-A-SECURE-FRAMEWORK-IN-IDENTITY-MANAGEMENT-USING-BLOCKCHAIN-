from fpdf import FPDF
from datetime import datetime
import requests
import os
import sys

# ==============================
# CONFIGURATION
# ==============================

SONAR_TOKEN = os.getenv("SONAR_TOKEN")

if not SONAR_TOKEN:
    print("ERROR: SONAR_TOKEN not found")
    sys.exit(1)

PROJECT_KEY = "kurapatiharshith_TO-GENERATE-A-SECURE-FRAMEWORK-IN-IDENTITY-MANAGEMENT-USING-BLOCKCHAIN-"

PROJECT_NAME = "Blockchain Identity Management Framework"

BASE_URL = "https://sonarcloud.io"

REPO_URL = (
    "https://github.com/kurapatiharshith/"
    "TO-GENERATE-A-SECURE-FRAMEWORK-IN-IDENTITY-MANAGEMENT-USING-BLOCKCHAIN-"
)

# ==============================
# FETCH PROJECT METRICS
# ==============================

metrics_url = (
    f"{BASE_URL}/api/measures/component"
    f"?component={PROJECT_KEY}"
    f"&metricKeys=bugs,vulnerabilities,code_smells,"
    f"coverage,duplicated_lines_density,security_hotspots"
)

metrics_response = requests.get(
    metrics_url,
    auth=(SONAR_TOKEN, "")
)

if metrics_response.status_code != 200:
    print("ERROR: Failed to fetch SonarCloud metrics")
    print(metrics_response.text)
    sys.exit(1)

metrics_data = metrics_response.json()

measures = metrics_data.get("component", {}).get("measures", [])

metrics = {}

for item in measures:
    metrics[item["metric"]] = item.get("value", "0")

# ==============================
# FETCH ISSUES
# ==============================

issues_url = (
    f"{BASE_URL}/api/issues/search"
    f"?componentKeys={PROJECT_KEY}"
    f"&ps=50"
)

issues_response = requests.get(
    issues_url,
    auth=(SONAR_TOKEN, "")
)

if issues_response.status_code != 200:
    print("ERROR: Failed to fetch issues")
    print(issues_response.text)
    sys.exit(1)

issues_data = issues_response.json()

issues = issues_data.get("issues", [])

# ==============================
# FETCH QUALITY GATE
# ==============================

quality_url = (
    f"{BASE_URL}/api/qualitygates/project_status"
    f"?projectKey={PROJECT_KEY}"
)

quality_response = requests.get(
    quality_url,
    auth=(SONAR_TOKEN, "")
)

quality_status = "UNKNOWN"

if quality_response.status_code == 200:
    quality_data = quality_response.json()

    quality_status = (
        quality_data.get("projectStatus", {})
        .get("status", "UNKNOWN")
    )

# ==============================
# SEVERITY COUNT
# ==============================

severity_counts = {
    "BLOCKER": 0,
    "CRITICAL": 0,
    "MAJOR": 0,
    "MINOR": 0,
    "INFO": 0
}

for issue in issues:
    severity = issue.get("severity", "INFO")

    if severity in severity_counts:
        severity_counts[severity] += 1

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

pdf.cell(
    200,
    10,
    "SonarCloud Security Analysis Report",
    ln=True,
    align="C"
)

pdf.ln(5)

pdf.set_font("Arial", "", 12)

pdf.cell(200, 8, f"Project Name: {PROJECT_NAME}", ln=True)

pdf.cell(200, 8, f"Project Key: {PROJECT_KEY}", ln=True)

pdf.cell(
    200,
    8,
    f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ln=True
)

pdf.ln(10)

# ==============================
# EXECUTIVE SUMMARY
# ==============================

pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, "Executive Summary", ln=True)

pdf.set_font("Arial", "", 12)

summary = (
    "This report was automatically generated from "
    "SonarCloud scan results."
)

pdf.multi_cell(0, 8, summary)

pdf.ln(5)

# ==============================
# OVERALL STATUS
# ==============================

pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, "Overall Status", ln=True)

pdf.set_font("Arial", "", 12)

status_data = [
    ("Quality Gate Status", quality_status),
    ("Total Issues Found", str(len(issues))),
    ("Security Hotspots", metrics.get("security_hotspots", "0")),
    ("Code Smells", metrics.get("code_smells", "0")),
    ("Bugs", metrics.get("bugs", "0")),
    ("Vulnerabilities", metrics.get("vulnerabilities", "0")),
    ("Coverage", metrics.get("coverage", "0")),
    ("Duplications", metrics.get("duplicated_lines_density", "0")),
]

for key, value in status_data:

    pdf.cell(80, 8, f"{key}:", border=1)

    pdf.cell(60, 8, str(value), border=1, ln=True)

pdf.ln(10)

# ==============================
# SEVERITY BREAKDOWN
# ==============================

pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, "Severity Breakdown", ln=True)

pdf.set_font("Arial", "B", 12)

pdf.cell(60, 10, "Severity", border=1)

pdf.cell(40, 10, "Count", border=1, ln=True)

pdf.set_font("Arial", "", 12)

for severity, count in severity_counts.items():

    pdf.cell(60, 10, severity, border=1)

    pdf.cell(40, 10, str(count), border=1, ln=True)

pdf.ln(10)

# ==============================
# DETAILED FINDINGS
# ==============================

pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, "Detailed Findings", ln=True)

if not issues:

    pdf.set_font("Arial", "", 12)

    pdf.cell(200, 10, "No issues found.", ln=True)

for issue in issues:

    issue_key = issue.get("key", "N/A")

    severity = issue.get("severity", "N/A")

    issue_type = issue.get("type", "N/A")

    rule = issue.get("rule", "N/A")

    status = issue.get("status", "N/A")

    message = issue.get("message", "N/A")

    raw_component = issue.get("component", "N/A")

    # Clean SonarCloud component path
    if ":" in raw_component:
        file_path = raw_component.split(":", 1)[1]
    else:
        file_path = raw_component

    line_number = str(issue.get("line", "N/A"))

    # GitHub File URL
    github_file_url = (
        f"{REPO_URL}/blob/main/{file_path}"
    )

    if line_number != "N/A":
        github_file_url += f"#L{line_number}"

    # SonarCloud Issue URL
    issue_url = (
        f"{BASE_URL}/project/issues"
        f"?id={PROJECT_KEY}"
        f"&issues={issue_key}"
        f"&open={issue_key}"
    )

    pdf.set_font("Arial", "B", 12)

    pdf.multi_cell(0, 8, f"Issue ID: {issue_key}")

    pdf.set_font("Arial", "", 11)

    details = [
        ("Severity", severity),
        ("Type", issue_type),
        ("Rule", rule),
        ("Status", status),
        ("Message", message),
        ("Repository File", file_path),
        ("Line Number", line_number),
    ]

    for key, value in details:

        pdf.multi_cell(
            0,
            7,
            f"{key}: {value}"
        )

    pdf.set_text_color(0, 0, 255)

    pdf.multi_cell(
        0,
        7,
        f"GitHub File URL: {github_file_url}"
    )

    pdf.multi_cell(
        0,
        7,
        f"Issue URL: {issue_url}"
    )

    pdf.set_text_color(0, 0, 0)

    pdf.ln(5)

# ==============================
# CONCLUSION
# ==============================

pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, "Conclusion", ln=True)

pdf.set_font("Arial", "", 12)

conclusion = (
    "Immediate remediation of Critical and Major "
    "findings is recommended to improve security "
    "and code quality."
)

pdf.multi_cell(0, 8, conclusion)

# ==============================
# SAVE PDF
# ==============================

pdf.output("sonar-report.pdf")

print("Dynamic SonarCloud PDF Report Generated Successfully")
