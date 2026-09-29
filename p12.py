import os
import json
from getpass import getpass

from groq import Groq
from pypdf import PdfReader
from docx import Document
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


# ---------- Real Incident ----------

REAL_INCIDENT = """
On September 9, 2026, Brevo, the third-party email provider used
by Trezor, suffered a security incident. An unauthorized actor gained
access to Brevo and used it to send emails from customer accounts,
including Trezor's.

Trezor reported that 347,149 marketing email contacts were exported.
The affected information consisted of newsletter subscriber email
addresses. No other Trezor system was affected.

Trezor suspended the Brevo account, disabled email sending, took down
the malicious domain through DNS, contacted affected customers and
added warnings across its communication channels.
"""


# ---------- Read Report ----------

def read_report(path):
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if path.lower().endswith(".docx"):
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    return open(
        path,
        encoding="utf-8",
        errors="ignore"
    ).read()


# ---------- AI Extraction ----------

def extract_report(text, client):

    fields = [
        "Submitted By",
        "Date & Time",
        "Report Ref No",
        "Title",
        "Company",
        "System / Application",
        "Type of Incident",
        "Description",
        "People Involved",
        "Others Notified",
        "Identification / Verification measures",
        "Containment measures",
        "Evidence collected (system logs etc.)",
        "Eradication measures",
        "Recovery measures",
        "Other mitigation measures",
        "Learning"
    ]

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            field: {"type": "string"}
            for field in fields
        },
        "required": fields
    }

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
Extract information from the incident report and fill the
predefined incident-report fields.

Use only information supported by the report.
Do not invent facts.
If a field is not available, return "Not specified".
Classify the incident into the closest available type.
Return only structured JSON.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "incident_report",
                "strict": True,
                "schema": schema
            }
        }
    )

    return json.loads(
        response.choices[0].message.content
    )


# ---------- Generate PDF ----------

def make_pdf(data):

    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=15,
        alignment=TA_CENTER
    )

    cell = ParagraphStyle(
        "cell",
        parent=styles["BodyText"],
        fontSize=7.5,
        leading=9
    )

    bold = ParagraphStyle(
        "bold",
        parent=cell,
        fontName="Helvetica-Bold"
    )

    pdf = SimpleDocTemplate(
        "incident_report.pdf",
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )

    story = [
        Paragraph(
            "DAYANANDA SAGAR COLLEGE OF ENGINEERING",
            title
        ),
        Paragraph(
            "Department of Artificial Intelligence & Machine Learning",
            title
        ),
        Spacer(1, 4 * mm)
    ]

    def table(rows, widths):
        t = Table(rows, colWidths=widths)

        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
        ]))

        return t

    # Incident Identification

    story.append(
        table(
            [[Paragraph("<b>Incident Identification</b>", cell)]],
            [180 * mm]
        )
    )

    story.append(
        table(
            [
                [
                    Paragraph("<b>Submitted By</b>", bold),
                    Paragraph("<b>Date & Time</b>", bold),
                    Paragraph("<b>Report Ref No</b>", bold)
                ],
                [
                    Paragraph(data["Submitted By"], cell),
                    Paragraph(data["Date & Time"], cell),
                    Paragraph(data["Report Ref No"], cell)
                ],
                [
                    Paragraph("<b>Title</b>", bold),
                    Paragraph("<b>Company</b>", bold),
                    Paragraph("<b>System / Application</b>", bold)
                ],
                [
                    Paragraph(data["Title"], cell),
                    Paragraph(data["Company"], cell),
                    Paragraph(data["System / Application"], cell)
                ]
            ],
            [60 * mm, 60 * mm, 60 * mm]
        )
    )

    story.append(Spacer(1, 3 * mm))

    # Incident Type

    types = [
        "Denial of Service",
        "Malicious Code",
        "Unauthorized Use",
        "Unauthorized Access",
        "Unplanned",
        "Other"
    ]

    incident = data["Type of Incident"]

    rows = [
        [
            Paragraph("<b>Type of Incident Detected</b>", cell)
        ],
        [
            Paragraph(
                "  ".join(
                    ("☒ " if t.lower() in incident.lower()
                     else "☐ ") + t
                    for t in types
                ),
                cell
            )
        ]
    ]

    story.append(table(rows, [180 * mm]))

    # Main sections

    for field in [
        "Description",
        "People Involved",
        "Others Notified"
    ]:

        story.append(Spacer(1, 3 * mm))

        story.append(
            table(
                [
                    [Paragraph(f"<b>{field}</b>", cell)],
                    [Paragraph(data[field], cell)]
                ],
                [180 * mm]
            )
        )

    # Actions

    story.append(Spacer(1, 3 * mm))

    actions = [
        "Identification / Verification measures",
        "Containment measures",
        "Evidence collected (system logs etc.)",
        "Eradication measures",
        "Recovery measures",
        "Other mitigation measures",
        "Learning"
    ]

    rows = [
        [Paragraph("<b>Actions</b>", cell)]
    ]

    for action in actions:
        rows.append([
            Paragraph(
                f"<b>{action}</b>  {data[action]}",
                cell
            )
        ])

    story.append(
        table(
            rows,
            [180 * mm]
        )
    )

    pdf.build(story)


# ---------- Main ----------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = getpass("Enter Groq API Key ")

client = Groq(api_key=api_key)

print("1  Generate Recent Real Incident")
print("2  Upload Incident Report")

choice = input("\nEnter Choice ")

if choice == "1":

    text = REAL_INCIDENT

elif choice == "2":

    path = input("Enter Report File Path ")
    text = read_report(path)

else:

    print("Invalid Choice")
    exit()

print("\nExtracting Incident Parameters using GPT-OSS-120B...")

data = extract_report(
    text,
    client
)

print("\nExtracted Parameters")

for key, value in data.items():
    print(f"{key}  {value}")

make_pdf(data)

print("\nIncident Report Generated")
print("Saved as incident_report.pdf")
