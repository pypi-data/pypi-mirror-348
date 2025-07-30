# report_generator.py
from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'Machine Learning Evaluation Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        # Arial 12
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_metrics_table(self, metrics: dict):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Evaluation Metrics', 0, 1)
        self.set_font('Arial', '', 12)

        # Column widths
        col1_width = 70
        col2_width = 30

        # Header
        self.set_fill_color(220, 220, 220)
        self.cell(col1_width, 10, 'Metric', 1, 0, 'C', fill=True)
        self.cell(col2_width, 10, 'Score', 1, 1, 'C', fill=True)

        # Rows
        for metric, score in metrics.items():
            self.cell(col1_width, 10, metric, 1)
            self.cell(col2_width, 10, f"{score:.4f}", 1, 1)
        self.ln(5)

    def add_image(self, image_path, title=None, w=160):
        if title:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1)
        # Check if image file exists
        if os.path.exists(image_path):
            self.image(image_path, w=w)
            self.ln(10)
        else:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f"[Image not found: {image_path}]", 0, 1)
            self.ln(5)

def generate_pdf_report(filename, metrics: dict, image_paths: dict, output_dir="outputs"):
    """
    Generate a PDF report with metrics and plots.

    Args:
        filename (str): Name of the input file or model name.
        metrics (dict): Dictionary of evaluation metrics.
        image_paths (dict): Dictionary with keys as titles and values as image file paths.
        output_dir (str): Directory to save the PDF report.

    Returns:
        str: Path to the generated PDF report.
    """
    os.makedirs(output_dir, exist_ok=True)

    pdf = PDFReport()
    pdf.add_page()

    # Title
    pdf.chapter_title(f"Report for: {filename}")

    # Add metrics table
    pdf.add_metrics_table(metrics)

    # Add images
    if image_paths:
        for title, img_path in image_paths.items():
            pdf.add_image(img_path, title=title)

    # Save PDF
    sanitized_name = filename.replace(" ", "_").replace(".", "_")
    pdf_path = os.path.join(output_dir, f"{sanitized_name}_evaluation_report.pdf")
    pdf.output(pdf_path)

    return pdf_path
