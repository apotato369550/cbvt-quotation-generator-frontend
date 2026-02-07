# CBVT Quotation Service - Quick Start

## 30-Second Setup

```bash
cd service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python verify_service.py
```

All tests should pass. Service is ready.

## Run the Service

```bash
source venv/bin/activate
python main.py
```

Service runs at `http://localhost:5000`

## Test It

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Format as HTML
```bash
curl -X POST http://localhost:5000/format/html \
  -H "Content-Type: application/json" \
  -d '{
    "id": "Q001",
    "date_created": "02/07/2026",
    "customer": {"to": "Test Client"},
    "items": [
      {"level": 0, "number": "1", "text": "Service Item", "price": 5000}
    ],
    "summary": {"total_price": 5000}
  }'
```

Returns: HTML string with formatted quotation

### 3. Download as PDF
```bash
curl -X POST http://localhost:5000/format/pdf \
  -H "Content-Type: application/json" \
  -d '{...same JSON...}' \
  --output quotation.pdf
```

### 4. Download as DOCX
```bash
curl -X POST http://localhost:5000/format/docx \
  -H "Content-Type: application/json" \
  -d '{...same JSON...}' \
  --output quotation.docx
```

## Full JSON Example

```json
{
  "id": "Q001",
  "date_created": "02/07/2026",
  "header": {
    "company_name": "Cebu Best Value Trading Corp.",
    "location": "Cebu City",
    "phone": "032-2670573",
    "mobile": "Sun-09325314857 Globe-09154657503",
    "services": ["Sales", "Installation", "Service", "Repair"]
  },
  "customer": {
    "to": "University of Cebu\nBanilad Campus",
    "attention": "Mr. Juan Dela Cruz – Purchasing Officer",
    "greeting": "Sir/Madam,"
  },
  "items": [
    {
      "level": 0,
      "number": "1",
      "text": "DEPT - Main Campus - One(1) Window Air Conditioner",
      "price": null
    },
    {
      "level": 1,
      "number": "1",
      "text": "General cleaning of the entire unit",
      "price": 600
    },
    {
      "level": 1,
      "number": "2",
      "text": "Supply and install new compressor",
      "price": 8500
    }
  ],
  "summary": {
    "warranty": "One(1) Year for parts + One(1) Year for compressor",
    "terms_of_payment": "COD (Cash on Delivery)",
    "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
    "total_price": 9100
  }
}
```

## Key Points

- **Date format**: MM/DD/YYYY (e.g., 02/07/2026)
- **Price format**: Number (e.g., 5000) → outputs as ₱ 5,000
- **Required**: `date_created` and `customer.to`
- **Items levels**:
  - 0: Main item (bold, no indent)
  - 1: Sub-item (indented ~0.5-0.75")
  - 2: Sub-sub-item (indented ~0.75-1.25")

## API Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | / | API documentation |
| GET | /health | Check libraries |
| POST | /format/html | HTML output |
| POST | /format/pdf | PDF download |
| POST | /format/docx | DOCX download |
| POST | /format/all | All formats (JSON) |

## Troubleshooting

**Port 5000 in use?**
```bash
uvicorn main:app --port 8000
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Test failing?**
```bash
python verify_service.py
```

## Frontend Integration

Service CORS allows requests from:
- http://localhost:3000
- http://127.0.0.1:3000

Change in `main.py` if needed.

## Documentation

- Full API: See `README.md`
- Formatting rules: `/docs/FORMATTING_RULES.md`
- Pydantic models: Search `class ___Request` in `main.py`

## Next

1. Start service: `python main.py`
2. Test endpoint: `curl http://localhost:5000/health`
3. Send quotation JSON to `/format/html`, `/format/pdf`, or `/format/docx`
4. Download or display result

Done!
