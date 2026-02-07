#!/usr/bin/env python3
"""
Test FastAPI endpoints using Starlette's TestClient.
"""

import json
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

sample_quotation = {
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
        "to": "University of Cebu",
        "attention": "Mr. Juan Dela Cruz",
    },
    "items": [
        {
            "level": 0,
            "number": "1",
            "text": "Main Campus - One(1) Window Air Conditioner Unit",
            "price": None
        },
        {
            "level": 1,
            "number": "1",
            "text": "General cleaning of the entire unit",
            "price": 600
        }
    ],
    "summary": {
        "warranty": "One(1) Year for parts",
        "terms_of_payment": "COD (Cash on Delivery)",
        "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
        "total_price": 10000
    }
}

def test_health():
    """Test health check endpoint."""
    print("Testing GET /health...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print(f"  ✓ Health check passed")
    print(f"    - weasyprint: {data['weasyprint_available']}")
    print(f"    - reportlab: {data['reportlab_available']}")
    print(f"    - python-docx: {data['python_docx_available']}")

def test_root():
    """Test root endpoint."""
    print("Testing GET /...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    print(f"  ✓ Root endpoint returned API documentation")

def test_html_endpoint():
    """Test HTML formatting endpoint."""
    print("Testing POST /format/html...")
    response = client.post("/format/html", json=sample_quotation)
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "Cebu Best Value Trading Corp." in response.text
    print(f"  ✓ HTML endpoint works ({len(response.text)} chars)")

def test_pdf_endpoint():
    """Test PDF generation endpoint."""
    print("Testing POST /format/pdf...")
    response = client.post("/format/pdf", json=sample_quotation)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    print(f"  ✓ PDF endpoint works ({len(response.content)} bytes)")

def test_docx_endpoint():
    """Test DOCX generation endpoint."""
    print("Testing POST /format/docx...")
    response = client.post("/format/docx", json=sample_quotation)
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    print(f"  ✓ DOCX endpoint works ({len(response.content)} bytes)")

def test_all_endpoint():
    """Test combined formatting endpoint."""
    print("Testing POST /format/all...")
    response = client.post("/format/all", json=sample_quotation)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "html" in data
    assert "<!DOCTYPE html>" in data["html"]
    print(f"  ✓ All formats endpoint works")
    if "pdf_base64" in data:
        print(f"    - PDF included ({len(data['pdf_base64'])} chars base64)")
    if "docx_base64" in data:
        print(f"    - DOCX included ({len(data['docx_base64'])} chars base64)")

def test_missing_required_field():
    """Test validation error for missing required field."""
    print("Testing validation...")
    bad_quotation = {
        "date_created": "02/07/2026",
        "customer": {},  # Missing 'to' field
    }
    response = client.post("/format/html", json=bad_quotation)
    assert response.status_code == 400
    print(f"  ✓ Validation works (returns 400 for missing required fields)")

def main():
    """Run all endpoint tests."""
    print("\n" + "="*60)
    print("CBVT Quotation Service - Endpoint Tests")
    print("="*60 + "\n")

    try:
        test_health()
        test_root()
        test_html_endpoint()
        test_pdf_endpoint()
        test_docx_endpoint()
        test_all_endpoint()
        test_missing_required_field()

        print("\n" + "="*60)
        print("All endpoint tests passed! ✓")
        print("="*60 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
