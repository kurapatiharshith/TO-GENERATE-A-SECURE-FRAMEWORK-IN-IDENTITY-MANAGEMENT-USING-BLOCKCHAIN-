import requests
from fpdf import FPDF
import os

SONAR_TOKEN = os.getenv("SONAR_TOKEN")

PROJECT_KEY = "kurapatiharshith_TO-GENERATE-A-SECURE-FRAMEWORK-IN-IDENTITY-MANAGEMENT-USING-BLOCKCHAIN-"

url = f"https://sonarcloud.io/api/measures/component?component={PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density"

response = requests.get(url, auth=(SONAR_TOKEN, ""))
data = response.json()

metrics = data["component"]["measures"]

pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="SonarCloud Analysis Report", ln=True, align='C')

pdf.ln(10)

pdf.set_font("Arial", size=12)

for metric in metrics:
    line = f"{metric['metric']} : {metric['value']}"
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("sonar-report.pdf")

print("PDF Report Generated")