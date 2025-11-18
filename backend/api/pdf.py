"""Utility helpers for generating PDF summaries."""

from io import BytesIO
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Dataset


def _table(data: List[List], column_widths=None) -> Table:
    table = Table(data, colWidths=column_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ]
        )
    )
    return table


def build_dataset_report(dataset: Dataset) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Dataset Report: {dataset.name}", styles["Heading1"]))
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            f"Uploaded on {dataset.uploaded_at:%d %b %Y, %I:%M %p} | Records: {dataset.total_records}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 18))

    summary_rows = [
        ["Metric", "Value"],
        ["Average Flowrate", f"{dataset.avg_flowrate}"],
        ["Average Pressure", f"{dataset.avg_pressure}"],
        ["Average Temperature", f"{dataset.avg_temperature}"],
    ]
    story.append(_table(summary_rows, column_widths=[200, 200]))
    story.append(Spacer(1, 18))

    distribution_rows = [["Equipment Type", "Count"]]
    for equipment_type, count in sorted(dataset.type_distribution.items()):
        distribution_rows.append([equipment_type, count])
    story.append(Paragraph("Equipment Distribution", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(_table(distribution_rows, column_widths=[250, 150]))
    story.append(Spacer(1, 18))

    if dataset.metrics:
        story.append(Paragraph("Highlights", styles["Heading2"]))
        story.append(Spacer(1, 6))
        highlights = [["Insight", "Equipment", "Value"]]
        for key, payload in dataset.metrics.items():
            label = key.replace("_", " ").title()
            equipment = f"{payload.get('equipment_name')} ({payload.get('equipment_type')})"
            value = ", ".join(
                f"{field.title()}: {payload[field]}"
                for field in payload
                if field not in {"equipment_name", "equipment_type"}
            )
            highlights.append([label, equipment, value])
        story.append(_table(highlights, column_widths=[180, 180, 140]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
