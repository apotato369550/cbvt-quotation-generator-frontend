# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CBVT (Cebu Best Value Trading Corp.) Quotation Generator - A system for extracting, formatting, and generating quotations from DOCX/PDF files. The project consists of:

1. **Python extraction scripts** - Extract structured data from existing quotation documents
2. **FastAPI service** - Format and export quotations as HTML/PDF/DOCX
3. **Node.js webpage** - Interactive frontend for quotation generation

## Development Commands

### Service (FastAPI)

```bash
# Setup
cd service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run service
python main.py
# Or: uvicorn main:app --host 0.0.0.0 --port 5000

# Test
python scripts/verify_service.py    # Verify without running server
python scripts/test_service.py      # Unit tests for format rules
python scripts/test_endpoints.py    # API endpoint tests
```

Service runs on `http://localhost:5000` with CORS enabled for `localhost:3000`.

### Webpage (Node.js)

```bash
# Setup
cd webpage
npm install

# Run
npm start
# Or: node server.js
```

Webpage runs on `http://localhost:3000`.

### Extraction Scripts (Python)

```bash
# Setup
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install pdfplumber python-docx  # No requirements.txt in scripts/

# Extract from PDFs
python extract_quotation_format.py

# Analyze quotation patterns
python analyze_quotation_formats.py
```

Extraction scripts read from `data/pdfs/` or `data/docx_files/` and write to `output/extraction_output/`.

## Architecture

### Three-Component System

```
data/                     # Input documents (DOCX/PDFs)
  ├── docx_files/        # Historical quotations
  └── pdfs/              # PDF versions

scripts/                  # Python extraction utilities
  ├── extract_quotation_format.py    # Extract text/tables from PDFs
  ├── analyze_quotation_formats.py   # Pattern analysis
  └── parse_quotation_items.py       # Parse item hierarchies

service/                  # FastAPI formatting service
  ├── main.py            # Endpoints: /format/{html,pdf,docx}
  ├── format_rules.py    # HTML generation matching FORMATTING_RULES.md
  └── requirements.txt   # fastapi, uvicorn, weasyprint, python-docx

webpage/                  # Node.js/Express frontend
  ├── index.html         # Interactive quotation builder
  ├── server.js          # Static file server
  └── package.json       # express, cors

docs/
  └── ITEMIZATION_PATTERNS.md   # Analysis of quotation numbering patterns

output/
  └── extraction_output/         # JSON extracted data
```

### Data Flow

1. **Extraction**: `scripts/extract_quotation_format.py` converts DOCX/PDF → JSON with structured fields
2. **Analysis**: `scripts/analyze_quotation_formats.py` identifies patterns (numbering, pricing, hierarchy)
3. **Generation**: FastAPI service accepts JSON quotation → outputs HTML/PDF/DOCX
4. **Frontend**: Webpage sends quotation JSON to service, displays/downloads results

### Key Patterns

**Quotation Structure** (from `docs/ITEMIZATION_PATTERNS.md`):
- **Primary items**: Decimal numbering (1., 2., 3.)
- **Secondary items**: Alphabetic (a., b.) or numeric sub-steps
- **Location grouping**: Items grouped by floor/room with numbering resets
- **Pricing**: Unit-based (`₱600/unit = ₱29,400`) or lump-sum (`– ₱8,500`)
- **Distance charges**: Base + excess distance calculation (`32ft - 10ft = 22ft × ₱350/ft = ₱7,700`)

**API Request Format** (service/main.py):
```json
{
  "id": "Q001",
  "date_created": "MM/DD/YYYY",
  "header": {...},
  "customer": {"to": "Company", "attention": "Person"},
  "items": [{"level": 0, "number": "1", "text": "...", "price": 1000}],
  "summary": {"warranty": "...", "total_price": 1000}
}
```

### Service Endpoints

- `GET /health` - Library availability check
- `POST /format/html` - Returns HTML string
- `POST /format/pdf` - Returns PDF file (uses weasyprint or reportlab)
- `POST /format/docx` - Returns DOCX file (uses python-docx)
- `POST /format/all` - Returns JSON with base64-encoded outputs

### Format Rules Implementation

The service implements grandfather's exact formatting rules:
- Font: Times New Roman, 10pt body, 12-14pt headers
- Indentation: Level 0 (none), Level 1 (~0.5-0.75"), Level 2 (~0.75-1.25")
- Price format: `₱X,XXX.XX` with Philippine Peso symbol
- Layout: Letter size (8.5"×11"), 0.5-0.75" margins

See `service/format_rules.py:format_quotation_html()` for implementation.

## Important Notes

- **Python venvs**: Both `scripts/venv/` and `service/venv/` exist. Activate the correct one.
- **No shared requirements.txt**: Scripts and service have separate dependencies.
- **CORS**: Service only allows `localhost:3000` and `127.0.0.1:3000` by default.
- **PDF libraries**: Service tries weasyprint first, falls back to reportlab (lower fidelity).
- **Data extraction**: Input files in `data/docx_files/` follow naming pattern `ClientName-N-M_D_YYYY.docx`.
