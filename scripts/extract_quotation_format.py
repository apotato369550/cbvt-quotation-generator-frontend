#!/usr/bin/env python3
"""
PDF Quotation Extraction Script

Extracts text, tables, fields, and structure from all PDFs in data/pdfs.
Outputs JSON files with extracted information to output/extraction_output/.
"""

import os
import json
import pdfplumber
from pathlib import Path
from datetime import datetime

# Configuration
PDF_INPUT_DIR = "/home/jay/Desktop/Coding Stuff/cbvt-quotation-generator/data/pdfs"
OUTPUT_DIR = "/home/jay/Desktop/Coding Stuff/cbvt-quotation-generator/output/extraction_output"


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def extract_fields_from_text(text):
    """
    Extract common quotation fields from raw text using pattern matching.
    """
    fields = {}
    lines = text.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Date
        if 'Date :' in line:
            fields['date'] = line_stripped.replace('Date :', '').strip()

        # To/Company
        elif 'To :' in line:
            fields['to'] = line_stripped.replace('To :', '').strip()

        # Attention/Contact Person
        elif 'Attention :' in line:
            fields['attention'] = line_stripped.replace('Attention :', '').strip()

        # Phone/contact info
        elif 'cell' in line.lower() and '-' in line:
            if 'phone' not in fields:
                fields['phone'] = line_stripped

        # Terms of Payment
        elif 'Terms of Payment:' in line:
            fields['terms_of_payment'] = line_stripped.replace('Terms of Payment:', '').strip()

        # Warranty
        elif 'Warranty:' in line:
            fields['warranty'] = line_stripped.replace('Warranty:', '').strip()

        # Total Price
        elif 'Total Price –' in line or 'Total Price -' in line:
            fields['total_price'] = line_stripped.replace('Total Price –', '').replace('Total Price -', '').strip()

    return fields


def extract_from_pdf(pdf_path):
    """
    Extract text, tables, fields, and metadata from a single PDF.
    """
    result = {
        'filename': os.path.basename(pdf_path),
        'filepath': pdf_path,
        'extracted_text': '',
        'tables': [],
        'detected_fields': {},
        'page_count': 0,
        'errors': []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            result['page_count'] = len(pdf.pages)
            all_text = []

            # Process each page
            for page_num, page in enumerate(pdf.pages):
                try:
                    # Extract text
                    text = page.extract_text()
                    if text:
                        all_text.append(text)

                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table_idx, table in enumerate(tables):
                            result['tables'].append({
                                'page': page_num + 1,
                                'table_index': table_idx,
                                'rows': table
                            })

                except Exception as e:
                    result['errors'].append(f"Page {page_num + 1}: {str(e)}")

            # Combine all text
            result['extracted_text'] = '\n'.join(all_text)

            # Extract detected fields
            result['detected_fields'] = extract_fields_from_text(result['extracted_text'])

    except Exception as e:
        result['errors'].append(f"Failed to open PDF: {str(e)}")

    return result


def process_all_pdfs():
    """
    Process all PDFs in the input directory.
    """
    ensure_output_dir()

    # Get all PDF files
    pdf_files = sorted([
        f for f in os.listdir(PDF_INPUT_DIR)
        if f.lower().endswith('.pdf')
    ])

    print(f"Found {len(pdf_files)} PDFs in {PDF_INPUT_DIR}")
    print(f"Extracting to {OUTPUT_DIR}\n")

    results_summary = []

    for pdf_filename in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_filename)
        print(f"Processing: {pdf_filename}...", end=' ')

        # Extract data
        extracted = extract_from_pdf(pdf_path)

        # Generate output filename
        output_filename = pdf_filename.replace('.pdf', '_extracted.json')
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Write JSON output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(extracted, f, indent=2, ensure_ascii=False)
            print(f"✓ ({extracted['page_count']} pages, {len(extracted['tables'])} tables)")
            results_summary.append({
                'file': pdf_filename,
                'pages': extracted['page_count'],
                'tables': len(extracted['tables']),
                'errors': len(extracted['errors'])
            })
        except Exception as e:
            print(f"✗ ERROR: {e}")
            results_summary.append({
                'file': pdf_filename,
                'error': str(e)
            })

    # Write summary
    summary_path = os.path.join(OUTPUT_DIR, '_extraction_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_files': len(pdf_files),
            'results': results_summary
        }, f, indent=2)

    print(f"\nExtraction complete. Summary saved to _extraction_summary.json")


if __name__ == '__main__':
    process_all_pdfs()
