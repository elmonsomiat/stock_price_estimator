from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import markdown
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf_from_dict(data_dict, output_file):
    """
    Creates a PDF where each dictionary key is a title and its value is the text content.
    Each section starts on a new page.

    Args:
        data_dict (dict): Dictionary with titles as keys and texts as values.
        output_file (str): Path to save the generated PDF.
    """
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    small_text_style = ParagraphStyle(
        name='SmallText',
        parent=styles['Normal'],
        fontSize=8,  # Smaller font size
        leading=10   # Adjust line spacing accordingly
    )
    for title, text in data_dict.items():
        # Add title as Heading
        story.append(Paragraph(title, styles['Heading1']))
        story.append(Spacer(1, 12))  # Space between title and text

        html_text = text.replace('\n', '<br /> ')
        html_content = markdown.markdown(html_text)
        # return html_content
        # Add text as normal paragraph
        story.append(Paragraph(html_content,
                               # styles['Normal'],
                              small_text_style, ))

        # Add a page break after each section
        story.append(PageBreak())

    # Build the PDF
    doc.build(story)
    return story
