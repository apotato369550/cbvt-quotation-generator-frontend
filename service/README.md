# CBVT Quotation Formatter Service

FastAPI service for formatting and exporting quotations as PDF, DOCX, and HTML, matching the exact layout and typography rules documented in `/docs/FORMATTING_RULES.md`.

## Quick Start

### 1. Install Dependencies

```bash
cd service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Service

```bash
python main.py
```

The service will start on `http://localhost:5000`.

Alternatively, using uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

### 3. Verify Installation

```bash
python verify_service.py
```

## API Endpoints

### Health Check
```
GET /health
```
Returns status and library availability.

### Format HTML
```
POST /format/html
Content-Type: application/json

{
  "id": "Q001",
  "date_created": "02/07/2026",
  "header": {...},
  "customer": {...},
  "items": [...],
  "summary": {...}
}
```
Returns formatted HTML string.

### Format PDF
```
POST /format/pdf
Content-Type: application/json
```
Returns PDF file (application/pdf) as downloadable attachment.

### Format DOCX
```
POST /format/docx
Content-Type: application/json
```
Returns DOCX file (application/vnd.openxmlformats-officedocument.wordprocessingml.document) as downloadable attachment.

### Format All
```
POST /format/all
Content-Type: application/json
```
Returns JSON with:
- `html`: Formatted HTML string
- `pdf_base64`: Base64-encoded PDF (if weasyprint/reportlab available)
- `docx_base64`: Base64-encoded DOCX (if python-docx available)

### Root Documentation
```
GET /
```
Returns API documentation with full request/response schemas.

## Request Structure

### Quotation JSON

```json
{
  "id": "Q001",
  "date_created": "MM/DD/YYYY",
  "header": {
    "company_name": "Cebu Best Value Trading Corp.",
    "location": "Cebu City",
    "phone": "032-2670573",
    "mobile": "Sun-09325314857 Globe-09154657503",
    "services": ["Sales", "Installation", "Service", "Repair"]
  },
  "customer": {
    "to": "Company Name",
    "attention": "Contact Name – Title",
    "greeting": "Sir/Madam,"
  },
  "items": [
    {
      "level": 0,
      "number": "1",
      "text": "Item description",
      "price": 1000
    },
    {
      "level": 1,
      "number": "1",
      "text": "Sub-item",
      "price": 500
    }
  ],
  "summary": {
    "warranty": "One(1) Year for parts",
    "terms_of_payment": "COD (Cash on Delivery)",
    "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
    "notes": "Optional notes",
    "total_price": 1500
  }
}
```

### Required Fields
- `date_created`: Date in MM/DD/YYYY format
- `customer.to`: Client name/company
- At least one of: `items` or `summary.total_price`

## Formatting Rules

The service implements formatting rules from `/docs/FORMATTING_RULES.md`:

- **Font**: Times New Roman, serif
- **Body size**: 10pt
- **Header size**: 12-14pt
- **Items hierarchy**:
  - Level 0: Bold, left-aligned
  - Level 1: Indented ~0.5-0.75"
  - Level 2: Indented ~0.75-1.25"
- **Price format**: ₱X,XXX.XX
- **Spacing**: 0.5-2 line breaks between sections
- **Layout**: Standard 8.5" x 11" letter size, 0.5-0.75" margins

## Files

- `main.py` - FastAPI application with endpoints
- `format_rules.py` - HTML formatting logic implementing FORMATTING_RULES.md
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns
- `verify_service.py` - Verification script (no server required)
- `test_service.py` - Format rules unit tests
- `test_endpoints.py` - API endpoint tests

## Dependencies

### Core
- fastapi - Web framework
- uvicorn - ASGI server
- pydantic - Data validation
- python-multipart - Form data handling
- aiofiles - Async file operations

### Output Formats
- python-docx - DOCX generation
- weasyprint - HTML to PDF (preferred)
- reportlab - PDF generation (fallback)

### Testing
- httpx - HTTP client for testing

## CORS Configuration

Cross-Origin Resource Sharing is enabled for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Modify in `main.py` if frontend is running on different origin.

## Error Handling

The service returns HTTP status codes:
- `200`: Success
- `400`: Bad request (missing/invalid fields)
- `500`: Server error (conversion failure)

Error responses include a `detail` field with error message.

## Environment Variables

None required. Service uses hardcoded defaults:
- Port: 5000
- Host: 0.0.0.0 (all interfaces)
- CORS origins: localhost:3000, 127.0.0.1:3000

## Troubleshooting

### PDF Generation Not Working
- Check library availability: `python verify_service.py`
- Install weasyprint: `pip install weasyprint>=59.0`
- Fallback uses reportlab (lower fidelity)

### DOCX Not Available
- Ensure python-docx is installed: `pip install python-docx`

### Service Won't Start
- Check port 5000 is not in use: `lsof -i :5000`
- Verify all dependencies: `pip list | grep -E "fastapi|uvicorn|pydantic"`

## Example Usage

```bash
curl -X POST http://localhost:5000/format/html \
  -H "Content-Type: application/json" \
  -d '{
    "id": "Q001",
    "date_created": "02/07/2026",
    "customer": {"to": "Test Client"},
    "items": [{"level": 0, "number": "1", "text": "Item 1", "price": 1000}],
    "summary": {"total_price": 1000}
  }'
```

## License

Part of CBVT Quotation Generator project.
