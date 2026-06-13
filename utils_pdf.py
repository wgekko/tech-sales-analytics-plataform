from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def generate_executive_pdf(
    file_name,
    resumen
):

    doc = SimpleDocTemplate(
        file_name
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Executive Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,12)
    )

    for linea in resumen:

        content.append(
            Paragraph(
                linea,
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1,6)
        )

    doc.build(content)

    return file_name