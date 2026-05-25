import os
import re
import textwrap
from html import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from utils.config import OUTPUT_DIR


def export_txt(content: str, filename: str = "meeting_output.txt") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

    return output_path


def clean_text_for_pdf(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
        "₹": "Rs.",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Break extremely long words/URLs/tokens
    def break_long_token(match):
        token = match.group(0)
        return " ".join(textwrap.wrap(token, width=60))

    text = re.sub(r"\S{80,}", break_long_token, text)

    return text


def export_pdf(content: str, filename: str = "meeting_output.pdf") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, filename)

    cleaned_content = clean_text_for_pdf(content)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.fontName = "Helvetica"
    normal_style.fontSize = 10
    normal_style.leading = 14

    story = []

    for line in cleaned_content.split("\n"):
        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        safe_line = escape(line)
        story.append(Paragraph(safe_line, normal_style))
        story.append(Spacer(1, 4))

    doc.build(story)

    return output_path