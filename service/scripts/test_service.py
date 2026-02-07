#!/usr/bin/env python3
"""
Test script for the CBVT Quotation Formatter service.
Tests basic functionality of format endpoints without running a server.
"""

import json
from format_rules import format_quotation_html, format_price

# Sample quotation data
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
        "to": "University of Cebu\nBanilad Campus",
        "attention": "Mr. Juan Dela Cruz – Purchasing Officer",
        "greeting": "Sir/Madam,"
    },
    "items": [
        {
            "level": 0,
            "number": "1",
            "text": "DEPT - Main Campus - One(1) Window Air Conditioner Unit",
            "price": None
        },
        {
            "level": 1,
            "number": "1",
            "text": "General cleaning of the entire unit by supplying chemicals",
            "price": 600
        },
        {
            "level": 1,
            "number": "2",
            "text": "Supply and installation of new compressor",
            "price": 8500
        },
        {
            "level": 1,
            "number": "3",
            "text": "Recharging of refrigerant",
            "price": 900
        }
    ],
    "summary": {
        "warranty": "One(1) Year for parts + One(1) Year for the compressor",
        "terms_of_payment": "COD (Cash on Delivery)",
        "exception": "(1) Circuit breaker and Gov't Fees\n(2) Power Supply",
        "notes": None,
        "total_price": 10000
    }
}

def test_format_price():
    """Test price formatting."""
    print("Testing format_price()...")
    assert format_price(600) == "₱ 600"
    assert format_price(8500) == "₱ 8,500"
    assert format_price(10000.50) == "₱ 10,000.50"
    print("  ✓ Price formatting works")

def test_format_html():
    """Test HTML formatting."""
    print("Testing format_quotation_html()...")
    html = format_quotation_html(sample_quotation)

    # Check that key sections exist
    assert "Cebu Best Value Trading Corp." in html
    assert "02/07/2026" in html
    assert "University of Cebu" in html
    assert "Job to be done" in html
    assert "₱ 600" in html
    assert "Warranty:" in html
    assert "Terms of Payment:" in html
    assert "Thank you very much" in html
    assert "Very Truly Yours," in html
    assert "#Q001" in html

    print("  ✓ HTML formatting works")
    print(f"  ✓ Generated {len(html)} characters of HTML")

def test_html_structure():
    """Test HTML document structure."""
    print("Testing HTML structure...")
    html = format_quotation_html(sample_quotation)

    assert html.startswith("<!DOCTYPE html>")
    assert "<html>" in html
    assert "</html>" in html
    assert "<style>" in html
    assert "</style>" in html
    assert "font-family:" in html
    assert "Times New Roman" in html

    print("  ✓ HTML structure is valid")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CBVT Quotation Formatter - Test Suite")
    print("="*60 + "\n")

    try:
        test_format_price()
        test_format_html()
        test_html_structure()

        print("\n" + "="*60)
        print("All tests passed! ✓")
        print("="*60 + "\n")

        # Print sample HTML output (first 1000 chars)
        print("Sample HTML output (first 1000 characters):\n")
        html = format_quotation_html(sample_quotation)
        print(html[:1000] + "...\n")

        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
