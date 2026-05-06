from fpdf import FPDF
from datetime import datetime
import os

# ==============================
# PROJECT INFORMATION
# ==============================

PROJECT_KEY = "kurapatiharshith_TO-GENERATE-A-SECURE-FRAMEWORK-IN-IDENTITY-MANAGEMENT-USING-BLOCKCHAIN-"
PROJECT_NAME = "Blockchain Identity Management Framework"

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
# EXECUTIVE SUMMARY
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Executive Summary", ln=True)

pdf.set_font("Arial", "", 12)

summary = """
The SonarCloud analysis identified multiple vulnerabilities,
bugs, security hotspots, and maintainability issues in the repository.
Immediate remediation of Critical and Major findings is recommended.
"""

pdf.multi_cell(0, 8, summary)

pdf.ln(5)

# ==============================
# OVERALL STATUS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Overall Status", ln=True)

pdf.set_font("Arial", "", 12)

status_data = [
    ("Quality Gate Status", "Failed"),
    ("Total Issues Found", "4"),
    ("Security Hotspots", "2"),
    ("Code Smells", "1"),
    ("Bugs", "1"),
    ("Vulnerabilities", "2"),
    ("Coverage", "78%"),
    ("Duplications", "2.1%"),
]

for key, value in status_data:
    pdf.cell(80, 8, f"{key}:", border=1)
    pdf.cell(50, 8, value, border=1, ln=True)

pdf.ln(10)

# ==============================
# SEVERITY BREAKDOWN
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Severity Breakdown", ln=True)

pdf.set_font("Arial", "B", 12)
pdf.cell(60, 10, "Severity", border=1)
pdf.cell(40, 10, "Count", border=1, ln=True)

severity_data = [
    ("Blocker", "0"),
    ("Critical", "1"),
    ("Major", "1"),
    ("Minor", "1"),
    ("Info", "1"),
]

pdf.set_font("Arial", "", 12)

for severity, count in severity_data:
    pdf.cell(60, 10, severity, border=1)
    pdf.cell(40, 10, count, border=1, ln=True)

pdf.ln(10)

# ==============================
# DETAILED FINDINGS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Detailed Findings", ln=True)

findings = [
    {
        "Issue ID": "SQ-001",
        "Rule": "Hardcoded Credentials",
        "Severity": "Critical",
        "Type": "Vulnerability",
        "Status": "Open",
        "File": "src/config/auth.js",
        "Line": "24",
        "Description": "Sensitive credentials are hardcoded inside the source code.",
        "Code": 'const apiKey = "SECRET_API_KEY";',
        "Fix": "Use environment variables or secret management services.",
        "Secure": 'const apiKey = process.env.API_KEY;'
    }
]

for finding in findings:

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 8, f"Issue ID: {finding['Issue ID']}", ln=True)

    pdf.set_font("Arial", "", 12)

    details = [
        ("Rule Name", finding["Rule"]),
        ("Severity", finding["Severity"]),
        ("Type", finding["Type"]),
        ("Status", finding["Status"]),
        ("File Location", finding["File"]),
        ("Line Number", finding["Line"]),
    ]

    for key, value in details:
        pdf.cell(50, 8, f"{key}:", border=1)
        pdf.cell(130, 8, value, border=1, ln=True)

    pdf.ln(2)

    pdf.multi_cell(0, 8, f"Description:\n{finding['Description']}")

    pdf.ln(2)

    pdf.multi_cell(0, 8, f"Vulnerable Code:\n{finding['Code']}")

    pdf.ln(2)

    pdf.multi_cell(0, 8, f"Recommended Fix:\n{finding['Fix']}")

    pdf.ln(2)

    pdf.multi_cell(0, 8, f"Secure Example:\n{finding['Secure']}")

    pdf.ln(8)

# ==============================
# ADDITIONAL FINDINGS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Additional Findings", ln=True)

pdf.set_font("Arial", "B", 11)

headers = ["Issue ID", "Severity", "Type", "Description"]
widths = [30, 30, 40, 90]

for i in range(len(headers)):
    pdf.cell(widths[i], 10, headers[i], border=1)

pdf.ln()

pdf.set_font("Arial", "", 10)

additional_findings = [
    ("SQ-002", "Major", "Bug", "Null Pointer Risk"),
    ("SQ-003", "Critical", "Vulnerability", "SQL Injection Risk"),
    ("SQ-004", "Minor", "Code Smell", "Duplicate Code"),
]

for row in additional_findings:
    for i in range(len(row)):
        pdf.cell(widths[i], 10, row[i], border=1)
    pdf.ln()

pdf.ln(10)

# ==============================
# SECURITY HOTSPOTS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Security Hotspots Review", ln=True)

hotspots = [
    ("SH-001", "To Review", "Unsafe Cookie Configuration"),
    ("SH-002", "Acknowledged", "Weak Encryption Algorithm"),
]

pdf.set_font("Arial", "", 12)

for hotspot in hotspots:
    pdf.cell(40, 10, hotspot[0], border=1)
    pdf.cell(50, 10, hotspot[1], border=1)
    pdf.cell(100, 10, hotspot[2], border=1, ln=True)

pdf.ln(10)

# ==============================
# RECOMMENDATIONS
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Remediation Recommendations", ln=True)

recommendations = [
    "Fix Critical and Blocker vulnerabilities immediately.",
    "Remove hardcoded secrets from source code.",
    "Implement secure input validation.",
    "Use parameterized queries to prevent SQL Injection.",
    "Review all Security Hotspots manually.",
    "Improve unit test coverage."
]

pdf.set_font("Arial", "", 12)

for rec in recommendations:
    pdf.multi_cell(0, 8, f"- {rec}")

pdf.ln(10)

# ==============================
# CONCLUSION
# ==============================

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Conclusion", ln=True)

pdf.set_font("Arial", "", 12)

conclusion = """
The SonarCloud analysis identified multiple security vulnerabilities,
bugs, and maintainability issues in the repository.
Immediate remediation of Critical and Major findings is recommended
to improve application security, reliability, and code quality.
"""

pdf.multi_cell(0, 8, conclusion)

# ==============================
# SAVE PDF
# ==============================

pdf.output("sonar-report.pdf")

print("PDF Report Generated Successfully")
