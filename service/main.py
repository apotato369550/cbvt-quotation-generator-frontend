"""
FastAPI service for formatting and exporting quotations as PDF, DOCX, and HTML.
Port: 5000
"""

import io
import os
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from format_rules import format_quotation_html, format_price, apply_indentation

# Try to import PDF/DOCX libraries
try:
    import weasyprint
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    HAS_PYTHON_DOCX = True
except ImportError:
    HAS_PYTHON_DOCX = False


# Pydantic models for request validation
class HeaderModel(BaseModel):
    company_name: str = "Cebu Best Value Trading Corp."
    location: str = "Cebu City"
    phone: str = "032-2670573"
    mobile: str = "Sun-09325314857 Globe-09154657503"
    services: list = ["Sales", "Installation", "Service", "Repair"]


class CustomerModel(BaseModel):
    to: str
    attention: Optional[str] = ""
    greeting: str = "Sir/Madam,"
    location_reference: Optional[str] = ""


class ItemModel(BaseModel):
    level: int = 0
    number: str
    text: str
    price: Optional[float] = None
    sub_items: Optional[list] = None


class SummaryModel(BaseModel):
    warranty: Optional[str] = ""
    terms_of_payment: Optional[str] = ""
    exception: Optional[str] = "(1) Circuit breaker and Gov't Fees\n(2) Power Supply"
    notes: Optional[str] = ""
    total_price: Optional[float] = None


class QuotationRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    date_created: str
    header: HeaderModel = Field(default_factory=HeaderModel)
    customer: CustomerModel
    items: list[ItemModel] = []
    summary: SummaryModel = Field(default_factory=SummaryModel)


# Initialize FastAPI app
app = FastAPI(title="CBVT Quotation Service", version="1.0.0")

# Enable CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_quotation(quotation: QuotationRequest) -> Dict[str, Any]:
    """Validate quotation structure and convert to dict."""
    if not quotation.date_created:
        raise HTTPException(status_code=400, detail="date_created is required")
    if not quotation.customer or not quotation.customer.to:
        raise HTTPException(status_code=400, detail="customer.to is required")

    return quotation.dict()


def html_to_pdf_weasyprint(html_string: str) -> bytes:
    """Convert HTML to PDF using weasyprint."""
    if not HAS_WEASYPRINT:
        raise HTTPException(status_code=500, detail="weasyprint not installed")

    try:
        pdf_bytes = weasyprint.HTML(string=html_string).write_pdf()
        return pdf_bytes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


def html_to_pdf_reportlab(html_string: str) -> bytes:
    """Convert HTML to PDF using reportlab (fallback)."""
    if not HAS_REPORTLAB:
        raise HTTPException(status_code=500, detail="reportlab not installed")

    try:
        # Simple fallback: extract text from HTML and create basic PDF
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)

        # Basic styling
        styles = getSampleStyleSheet()
        story = []

        # Extract text from HTML (simple approach)
        import re
        text = re.sub(r'<[^>]+>', '', html_string)
        text = re.sub(r'\s+', ' ', text).strip()

        # Add paragraphs
        for line in text.split('\n'):
            if line.strip():
                p = Paragraph(line.strip(), styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.1*inch))

        doc.build(story)
        return pdf_buffer.getvalue()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


def html_to_docx(html_string: str) -> bytes:
    """Convert HTML to DOCX using python-docx."""
    if not HAS_PYTHON_DOCX:
        raise HTTPException(status_code=500, detail="python-docx not installed")

    try:
        doc = Document()

        # Set default font to Times New Roman, 10pt
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(10)

        # Parse HTML and add to document (simplified)
        import re
        html_string = re.sub(r'<[^>]+>', '\n', html_string)
        lines = html_string.split('\n')

        for line in lines:
            line = line.strip()
            if line:
                p = doc.add_paragraph(line)
                p.style = 'Normal'
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)

        # Save to bytes
        docx_buffer = io.BytesIO()
        doc.save(docx_buffer)
        docx_buffer.seek(0)
        return docx_buffer.getvalue()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX generation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "weasyprint_available": HAS_WEASYPRINT,
        "reportlab_available": HAS_REPORTLAB,
        "python_docx_available": HAS_PYTHON_DOCX
    }


@app.post("/format/html")
async def format_html(quotation: QuotationRequest):
    """
    Format quotation as HTML.

    Input: Quotation JSON with id, date_created, header, customer, items, summary
    Output: Formatted HTML string matching grandfather's exact format
    """
    try:
        quotation_dict = validate_quotation(quotation)
        html_output = format_quotation_html(quotation_dict)
        return PlainTextResponse(html_output, media_type="text/html")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTML formatting failed: {str(e)}")


@app.post("/format/pdf")
async def format_pdf(quotation: QuotationRequest):
    """
    Format quotation as PDF.

    Input: Quotation JSON
    Output: PDF file (application/pdf)
    """
    try:
        quotation_dict = validate_quotation(quotation)
        html_output = format_quotation_html(quotation_dict)

        # Try weasyprint first, fall back to reportlab
        if HAS_WEASYPRINT:
            pdf_bytes = html_to_pdf_weasyprint(html_output)
        elif HAS_REPORTLAB:
            pdf_bytes = html_to_pdf_reportlab(html_output)
        else:
            raise HTTPException(
                status_code=500,
                detail="No PDF library available (install weasyprint or reportlab)"
            )

        # Return as downloadable file
        filename = f"quotation_{quotation_dict.get('id', 'unknown')}.pdf"
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.post("/format/docx")
async def format_docx(quotation: QuotationRequest):
    """
    Format quotation as DOCX.

    Input: Quotation JSON
    Output: DOCX file (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
    """
    try:
        quotation_dict = validate_quotation(quotation)
        html_output = format_quotation_html(quotation_dict)
        docx_bytes = html_to_docx(html_output)

        # Return as downloadable file
        filename = f"quotation_{quotation_dict.get('id', 'unknown')}.docx"
        return FileResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX generation failed: {str(e)}")


@app.post("/format/all")
async def format_all(quotation: QuotationRequest):
    """
    Format quotation in all formats: HTML, PDF, DOCX.

    Returns JSON with base64-encoded outputs.
    """
    try:
        quotation_dict = validate_quotation(quotation)
        html_output = format_quotation_html(quotation_dict)

        result = {
            "id": quotation_dict.get('id'),
            "html": html_output,
        }

        # Generate PDF if possible
        if HAS_WEASYPRINT:
            pdf_bytes = html_to_pdf_weasyprint(html_output)
            import base64
            result["pdf_base64"] = base64.b64encode(pdf_bytes).decode()
        elif HAS_REPORTLAB:
            pdf_bytes = html_to_pdf_reportlab(html_output)
            import base64
            result["pdf_base64"] = base64.b64encode(pdf_bytes).decode()

        # Generate DOCX if possible
        if HAS_PYTHON_DOCX:
            docx_bytes = html_to_docx(html_output)
            import base64
            result["docx_base64"] = base64.b64encode(docx_bytes).decode()

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Formatting failed: {str(e)}")


@app.get("/")
async def root():
    """API documentation."""
    return {
        "service": "CBVT Quotation Formatter",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check with library availability",
            "POST /format/html": "Format quotation as HTML",
            "POST /format/pdf": "Format quotation as PDF",
            "POST /format/docx": "Format quotation as DOCX",
            "POST /format/all": "Format quotation in all formats (JSON response with base64)",
        },
        "request_schema": {
            "id": "string (optional)",
            "date_created": "string (MM/DD/YYYY)",
            "header": {
                "company_name": "string",
                "location": "string",
                "phone": "string",
                "mobile": "string",
                "services": "array of strings"
            },
            "customer": {
                "to": "string (required)",
                "attention": "string",
                "greeting": "string",
                "location_reference": "string"
            },
            "items": "array of {level, number, text, price, sub_items}",
            "summary": {
                "warranty": "string",
                "terms_of_payment": "string",
                "exception": "string",
                "notes": "string",
                "total_price": "number"
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
