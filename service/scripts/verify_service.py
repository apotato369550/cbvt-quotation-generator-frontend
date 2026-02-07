#!/usr/bin/env python3
"""
Verification script for CBVT Quotation Service.
Tests that all components load and work correctly without running a server.
"""

import sys
import traceback
from format_rules import format_quotation_html, format_price
from main import app

print("\n" + "="*60)
print("CBVT Quotation Service - Verification Script")
print("="*60 + "\n")

try:
    # 1. Verify format_rules module
    print("1. Verifying format_rules module...")
    assert format_price(1000) == "₱ 1,000"
    assert format_price(1500.50) == "₱ 1,500.50"
    print("   ✓ format_price() works correctly")

    # 2. Verify HTML generation
    print("2. Verifying HTML generation...")
    sample_quotation = {
        "id": "TEST-001",
        "date_created": "02/07/2026",
        "header": {
            "company_name": "Cebu Best Value Trading Corp.",
            "location": "Cebu City",
            "phone": "032-2670573",
            "mobile": "Sun-09325314857 Globe-09154657503",
            "services": ["Sales", "Installation", "Service", "Repair"]
        },
        "customer": {
            "to": "Test Customer",
            "attention": "John Doe",
            "greeting": "Sir/Madam,"
        },
        "items": [
            {
                "level": 0,
                "number": "1",
                "text": "Main Item - Test Service",
                "price": None
            },
            {
                "level": 1,
                "number": "1",
                "text": "Sub-item with cost",
                "price": 5000
            }
        ],
        "summary": {
            "warranty": "One(1) Year for parts",
            "terms_of_payment": "COD (Cash on Delivery)",
            "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
            "total_price": 5000
        }
    }

    html = format_quotation_html(sample_quotation)
    assert "<!DOCTYPE html>" in html
    assert "Cebu Best Value Trading Corp." in html
    assert "02/07/2026" in html
    assert "Test Customer" in html
    assert "₱ 5,000" in html
    assert "Very Truly Yours" in html
    assert "#TEST-001" in html
    print(f"   ✓ HTML formatting works ({len(html)} chars generated)")

    # 3. Verify FastAPI app
    print("3. Verifying FastAPI app...")
    assert app is not None
    routes = [route.path for route in app.routes]
    required_routes = ["/health", "/format/html", "/format/pdf", "/format/docx", "/format/all", "/"]
    for route in required_routes:
        assert route in routes, f"Missing route: {route}"
    print(f"   ✓ FastAPI app loaded with {len(routes)} routes")
    print(f"     Routes: {', '.join(required_routes)}")

    # 4. Check CORS middleware
    print("4. Verifying CORS configuration...")
    cors_found = False
    for middleware in app.user_middleware:
        if "CORSMiddleware" in str(middleware):
            cors_found = True
    assert cors_found
    print("   ✓ CORS middleware configured")

    # 5. Verify Pydantic models
    print("5. Verifying Pydantic request models...")
    from main import QuotationRequest, CustomerModel, SummaryModel

    # Test valid quotation
    test_req = QuotationRequest(
        id="Q001",
        date_created="02/07/2026",
        customer=CustomerModel(to="Test"),
        items=[],
        summary=SummaryModel()
    )
    assert test_req.id == "Q001"
    print("   ✓ Request models validate correctly")

    # 6. Check library availability
    print("6. Checking optional library availability...")
    from main import HAS_WEASYPRINT, HAS_REPORTLAB, HAS_PYTHON_DOCX
    print(f"   - weasyprint: {'available' if HAS_WEASYPRINT else 'not available'}")
    print(f"   - reportlab: {'available' if HAS_REPORTLAB else 'not available'}")
    print(f"   - python-docx: {'available' if HAS_PYTHON_DOCX else 'not available'}")

    # At least one PDF library should be available
    assert HAS_WEASYPRINT or HAS_REPORTLAB, "No PDF library available"
    assert HAS_PYTHON_DOCX, "python-docx not available"
    print("   ✓ All required libraries available")

    print("\n" + "="*60)
    print("All verifications passed! ✓")
    print("="*60)
    print("\nService is ready to run:")
    print("  cd /home/jay/Desktop/Coding\\ Stuff/cbvt-quotation-generator/service")
    print("  source venv/bin/activate")
    print("  python main.py")
    print("\nOr with uvicorn:")
    print("  uvicorn main:app --host 0.0.0.0 --port 5000")
    print("\n" + "="*60 + "\n")

    sys.exit(0)

except AssertionError as e:
    print(f"\n✗ Assertion failed: {e}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
