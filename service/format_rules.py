"""
Format rules for Cebu Best Value Trading Corp. quotations.
Implements formatting rules from FORMATTING_RULES.md
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime


def apply_indentation(level: int) -> str:
    """
    Return appropriate tabs/spaces for indentation levels.

    Level 0: No indentation (left-aligned)
    Level 1: 1-2 tabs (0.5-0.75 inches)
    Level 2: 1.5-2.5 tabs (0.75-1.25 inches)
    """
    if level == 0:
        return ""
    elif level == 1:
        return "\t"
    elif level == 2:
        return "\t\t"
    else:
        return "\t" * level


def format_price(amount: float) -> str:
    """
    Format price as ₱X,XXX.XX

    Args:
        amount: Numeric price value

    Returns:
        Formatted price string with Philippine Peso symbol
    """
    if isinstance(amount, str):
        amount = float(amount.replace(",", "").replace("₱", "").strip())

    # Check if amount has decimals
    if amount == int(amount):
        return f"₱ {int(amount):,}"
    else:
        return f"₱ {amount:,.2f}"


def format_quotation_html(quotation: Dict[str, Any]) -> str:
    """
    Format a quotation dictionary into HTML matching grandfather's exact layout.

    Args:
        quotation: Dict with keys:
            - id: quotation ID
            - date_created: date string (MM/DD/YYYY)
            - header: {company_name, location, phone, mobile, services}
            - items: [{level, number, text, price, sub_items}]
            - summary: {warranty, terms_of_payment, exception, notes}
            - customer: {to, attention}

    Returns:
        HTML string formatted per FORMATTING_RULES.md
    """
    html_parts = []

    # Add DOCTYPE and styling
    html_parts.append("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: "Times New Roman", Times, serif;
            font-size: 10pt;
            line-height: 1.5;
            margin: 0.5in;
            max-width: 7.5in;
            color: #000;
        }
        .header-company {
            text-align: center;
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 0.1in;
        }
        .header-separator {
            text-align: center;
            font-size: 10pt;
            margin-bottom: 0.1in;
        }
        .header-location {
            text-align: center;
            font-size: 10pt;
            margin-bottom: 0.5in;
        }
        .contact-info {
            text-align: center;
            font-size: 9pt;
            text-decoration: underline;
            margin-bottom: 0.5in;
        }
        .services {
            text-align: center;
            margin-bottom: 0.5in;
        }
        .services-bold {
            font-weight: bold;
            font-size: 10pt;
        }
        .services-normal {
            font-size: 10pt;
        }
        .customer-section {
            margin-bottom: 1in;
        }
        .customer-line {
            font-size: 10pt;
            margin-bottom: 0.2in;
        }
        .greeting {
            margin-left: 0.3in;
            margin-bottom: 0.3in;
        }
        .reference-statement {
            margin-left: 0.3in;
            margin-bottom: 0.3in;
            font-size: 10pt;
        }
        .pleased-quote {
            margin-left: 0.3in;
            margin-bottom: 0.3in;
            font-size: 10pt;
        }
        .job-header {
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 0.3in;
            font-size: 10pt;
        }
        .items-section {
            margin-bottom: 0.5in;
        }
        .item-level-1 {
            font-weight: bold;
            font-size: 10pt;
            margin-top: 0.3in;
            margin-bottom: 0.2in;
            margin-left: 0;
        }
        .item-level-2 {
            font-size: 10pt;
            margin-bottom: 0.1in;
            margin-left: 0.3in;
        }
        .item-level-3 {
            font-size: 10pt;
            margin-bottom: 0.1in;
            margin-left: 0.6in;
        }
        .total-price {
            font-size: 10pt;
            margin-top: 0.3in;
            margin-bottom: 0.3in;
            margin-left: 0.3in;
        }
        .summary-section {
            margin-bottom: 0.5in;
        }
        .summary-field {
            font-size: 10pt;
            margin-bottom: 0.3in;
            margin-left: 0;
        }
        .summary-field-label {
            font-weight: normal;
        }
        .closing-section {
            margin-top: 0.5in;
            margin-bottom: 0.5in;
        }
        .thank-you {
            font-size: 10pt;
            margin-bottom: 0.3in;
            margin-left: 0.3in;
            text-align: justify;
        }
        .closing-salutation {
            font-size: 10pt;
            margin-bottom: 0.5in;
            margin-left: 0.3in;
        }
        .signature-block {
            font-size: 10pt;
            margin-top: 0.5in;
        }
        .signature-line {
            margin-bottom: 0.2in;
        }
        .quotation-number {
            text-align: right;
            font-size: 9pt;
            margin-top: 0.5in;
        }
        .pre-text {
            font-family: "Courier New", monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 10pt;
        }
    </style>
</head>
<body>
""")

    # HEADER SECTION
    header = quotation.get("header", {})
    html_parts.append(f'<div class="header-company">{header.get("company_name", "Cebu Best Value Trading Corp.")}</div>')

    # Header separator with location
    sep_line = "_" * 34
    html_parts.append(f'<div class="header-separator">{sep_line} {header.get("location", "Cebu City")} {sep_line}</div>')

    # Contact info
    phone = header.get("phone", "032-2670573")
    mobile = header.get("mobile", "Sun-09325314857 Globe-09154657503")
    html_parts.append(f'<div class="contact-info">Telephone Number: {phone} || Mobile Number: {mobile}</div>')

    # Services
    services = header.get("services", ["Sales", "Installation", "Service", "Repair"])
    services_text = "  ".join(services) if isinstance(services, list) else services
    html_parts.append(f'<div class="services"><span class="services-bold">{services_text}</span></div>')
    html_parts.append(f'<div class="services"><span class="services-normal">Ductworks</span></div>')

    # CUSTOMER SECTION
    customer = quotation.get("customer", {})
    date_str = quotation.get("date_created", "")
    html_parts.append('<div class="customer-section">')
    html_parts.append(f'<div class="customer-line">Date : {date_str}</div>')

    to_field = customer.get("to", "")
    html_parts.append(f'<div class="customer-line">To : {to_field}</div>')

    attention_field = customer.get("attention", "")
    if attention_field:
        html_parts.append(f'<div class="customer-line">Attention : {attention_field}</div>')

    # Greeting
    greeting = customer.get("greeting", "Sir/Madam,")
    html_parts.append(f'<div class="greeting">{greeting}</div>')

    # Reference statement
    location_ref = customer.get("location_reference", "")
    reference_text = (
        f"This is with reference to your request for quotation for the installation/repair of the "
        f"following air-conditioner to be installed at:_________________________________________________"
    )
    html_parts.append(f'<div class="reference-statement">{reference_text}</div>')

    # Introduction
    html_parts.append('<div class="pleased-quote">We are pleased to quote the following:</div>')
    html_parts.append('<div class="job-header">Job to be done :</div>')

    # ITEMS SECTION
    html_parts.append('<div class="items-section">')
    items = quotation.get("items", [])

    for item in items:
        level = item.get("level", 0)
        number = item.get("number", "")
        text = item.get("text", "")
        price = item.get("price", "")

        # Format item text with price if available
        item_text = text
        if price:
            formatted_price = format_price(price) if isinstance(price, (int, float)) else price
            item_text = f"{text} – {formatted_price}"

        if level == 0:
            html_parts.append(f'<div class="item-level-1">{number}. {item_text}</div>')
        elif level == 1:
            html_parts.append(f'<div class="item-level-2">{number}. {item_text}</div>')
        else:
            html_parts.append(f'<div class="item-level-3">{number}. {item_text}</div>')

    html_parts.append('</div>')

    # PRICING
    total_price = quotation.get("summary", {}).get("total_price", "")
    if total_price:
        formatted_total = format_price(total_price) if isinstance(total_price, (int, float)) else total_price
        html_parts.append(f'<div class="total-price">Total Price – {formatted_total}</div>')

    # SUMMARY SECTION
    summary = quotation.get("summary", {})
    html_parts.append('<div class="summary-section">')

    # Warranty
    warranty = summary.get("warranty", "")
    if warranty:
        html_parts.append(f'<div class="summary-field"><span class="summary-field-label">Warranty:</span> {warranty}</div>')

    # Terms of Payment
    terms = summary.get("terms_of_payment", "")
    if terms:
        html_parts.append(f'<div class="summary-field"><span class="summary-field-label">Terms of Payment:</span> {terms}</div>')

    # Exception
    exception = summary.get("exception", "")
    if exception:
        exception_text = exception if isinstance(exception, str) else "\n".join(exception)
        html_parts.append(f'<div class="summary-field"><span class="summary-field-label">Exception:</span> {exception_text}</div>')

    # Notes
    notes = summary.get("notes", "")
    if notes:
        html_parts.append(f'<div class="summary-field"><span class="summary-field-label">Note:</span> {notes}</div>')

    html_parts.append('</div>')

    # CLOSING SECTION
    html_parts.append('<div class="closing-section">')
    html_parts.append('<div class="thank-you">Thank you very much for giving us the opportunity to quote and we hope to have the pleasure of serving you.</div>')
    html_parts.append('<div class="closing-salutation">Very Truly Yours,</div>')

    # Signature block
    html_parts.append('<div class="signature-block">')
    html_parts.append('<div class="signature-line">Conforme:______________              J.B Yap Jr.</div>')
    html_parts.append('<div class="signature-line">Date:__________________              Manager Q</div>')
    html_parts.append('</div>')

    # Quotation number
    quotation_id = quotation.get("id", "1")
    html_parts.append(f'<div class="quotation-number">#{quotation_id}</div>')

    html_parts.append('</body></html>')

    return "\n".join(html_parts)


def extract_quotation_from_json(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and normalize quotation data from JSON.

    Args:
        json_data: Raw JSON data from extraction

    Returns:
        Normalized quotation dictionary
    """
    quotation = {}

    # Extract basic fields
    quotation["id"] = json_data.get("id", json_data.get("filename", "").split(".")[0])
    quotation["date_created"] = json_data.get("date_created", json_data.get("detected_fields", {}).get("date", ""))

    # Extract customer info
    customer = {}
    detected = json_data.get("detected_fields", {})
    customer["to"] = detected.get("to", "")
    customer["attention"] = detected.get("attention", "")
    customer["greeting"] = "Sir/Madam,"
    quotation["customer"] = customer

    # Extract header
    header = {
        "company_name": "Cebu Best Value Trading Corp.",
        "location": "Cebu City",
        "phone": "032-2670573",
        "mobile": "Sun-09325314857 Globe-09154657503",
        "services": ["Sales", "Installation", "Service", "Repair"]
    }
    quotation["header"] = header

    # Extract items and summary
    quotation["items"] = json_data.get("items", [])
    quotation["summary"] = {
        "warranty": detected.get("warranty", ""),
        "terms_of_payment": detected.get("terms_of_payment", ""),
        "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
        "total_price": detected.get("total_price", "")
    }

    return quotation
