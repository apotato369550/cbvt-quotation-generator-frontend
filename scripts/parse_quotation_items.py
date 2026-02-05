#!/usr/bin/env python3
"""
Quotation Item Parser

Parses itemization structure from extracted quotation text.
Input: raw quotation text from JSON extraction
Output: structured item hierarchy with pricing information
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


def detect_item_line(line: str) -> bool:
    """
    Detect if line starts with numbering pattern (1., a., i), (1), (a), etc.

    Args:
        line: Text line to check

    Returns:
        True if line starts with item numbering pattern, False otherwise
    """
    line = line.strip()
    if not line:
        return False

    # Patterns: 1., 1), (1), a., a), (a), i., i), (i), etc.
    patterns = [
        r'^\d+[\.\)]',           # 1., 1)
        r'^\(\d+\)',             # (1), (2), etc.
        r'^[a-z][\.\)]',         # a., a), b., b), etc.
        r'^\([a-z]\)',           # (a), (b), etc.
        r'^[ivxlcdm]+[\.\)]',    # Roman numerals i., v., x., etc.
        r'^\([ivxlcdm]+\)',      # (i), (v), (x), etc.
    ]

    for pattern in patterns:
        if re.match(pattern, line, re.IGNORECASE):
            return True

    return False


def extract_number_and_text(line: str) -> Tuple[str, str]:
    """
    Extract numbering prefix and remaining text from an item line.

    Args:
        line: "1. Item description – ₱1,000"

    Returns:
        Tuple of (number_str, remaining_text)
        ("1", "Item description – ₱1,000")
    """
    line = line.strip()

    # Match patterns and capture number and text
    patterns = [
        (r'^(\d+)[\.\)]\s*(.*)', lambda m: (m.group(1), m.group(2))),           # 1. or 1)
        (r'^\((\d+)\)\s*(.*)', lambda m: (m.group(1), m.group(2))),             # (1)
        (r'^([a-z])[\.\)]\s*(.*)', lambda m: (m.group(1), m.group(2))),         # a. or a)
        (r'^\(([a-z])\)\s*(.*)', lambda m: (m.group(1), m.group(2))),           # (a)
        (r'^([ivxlcdm]+)[\.\)]\s*(.*)', lambda m: (m.group(1), m.group(2))),    # i. v. x. etc
        (r'^\(([ivxlcdm]+)\)\s*(.*)', lambda m: (m.group(1), m.group(2))),      # (i) (v) etc
    ]

    for pattern, extractor in patterns:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            return extractor(match)

    return ("", line)


def determine_hierarchy_level(number_str: str) -> int:
    """
    Determine hierarchy depth based on numbering format.

    Args:
        number_str: "1" → 1, "a" → 2, "i" → 3 (or 2 if ambiguous)

    Returns:
        Hierarchy level (1, 2, or 3)
    """
    number_str = number_str.lower().strip()

    if not number_str:
        return 0

    # Decimal/parenthesized digits -> level 1
    if re.match(r'^\d+$', number_str):
        return 1

    # Roman numerals (length > 1 or specific patterns) -> level 3
    # Single letter that could be roman (i,v,x,l,c,d,m) -> level 3
    # Multi-char roman numerals -> level 3
    if len(number_str) > 1 and re.match(r'^[ivxlcdm]+$', number_str):
        return 3

    # Single lowercase letter -> level 2 (includes single roman numerals)
    if re.match(r'^[a-z]$', number_str):
        return 2

    # Anything else
    return 0


def parse_pricing_from_line(text: str) -> Dict[str, Any]:
    """
    Identify pricing pattern in text and return structured pricing info.

    Args:
        text: "₱600/unit – ₱29,400" or "– ₱8,500" or "Plus: Installation – ₱19,500"

    Returns:
        Dict with keys: format, unit_price (optional), total/amount, calculation (optional)
    """
    pricing = {
        "format": None,
        "raw": text,
    }

    # Remove common prefix text to isolate pricing
    text_clean = re.sub(r'(Plus:|Additional:|Additional|Extra|Less discount:)\s*', '', text, flags=re.IGNORECASE)

    # Detect "Plus:" or "Additional:" prefix (additive pricing)
    if re.search(r'(Plus:|Additional:)', text, re.IGNORECASE):
        pricing["format"] = "additive"
        # Extract label and amount
        label_match = re.search(r'(Plus:|Additional:)?\s*([^–=₱]*?)\s*[–=]\s*₱\s*([\d,]+)', text)
        if label_match:
            pricing["label"] = label_match.group(2).strip() or "Installation"
            pricing["amount"] = int(label_match.group(3).replace(',', ''))
        return pricing

    # Detect unit-based pricing (₱X/unit = Y or ₱X/unit – Y)
    unit_match = re.search(r'₱\s*([\d,]+)\s*/unit\s*[–=]\s*₱\s*([\d,]+)', text)
    if unit_match:
        pricing["format"] = "unit-based"
        pricing["unit_price"] = int(unit_match.group(1).replace(',', ''))
        pricing["total"] = int(unit_match.group(2).replace(',', ''))
        return pricing

    # Detect lump-sum pricing (– ₱X or = ₱X)
    lump_match = re.search(r'[–=]\s*₱\s*([\d,]+)', text)
    if lump_match:
        pricing["format"] = "lump-sum"
        pricing["amount"] = int(lump_match.group(1).replace(',', ''))
        return pricing

    # Check for distance-based surcharge calculation
    if re.search(r'[–=]\s*₱\s*([\d,]+)', text):
        pricing["format"] = "calculation"
        calc_match = re.search(r'₱\s*([\d,]+)', text)
        if calc_match:
            pricing["amount"] = int(calc_match.group(1).replace(',', ''))

    return pricing


def parse_item_section(extracted_text: str) -> List[Dict[str, Any]]:
    """
    Parse itemization section from "Job to be done:" to end of text or "Total Price".

    Args:
        extracted_text: Full extracted text from JSON

    Returns:
        List of item dictionaries with hierarchy structure
    """
    # Extract the job section
    job_match = re.search(r'Job to be done\s*:', extracted_text, re.IGNORECASE)
    if not job_match:
        return []

    job_section = extracted_text[job_match.end():]

    # Find end of items (usually marked by Terms of Payment, Warranty, etc.)
    end_markers = ['Terms of Payment', 'Warranty', 'Exception', 'Thank you', 'Conforme']
    end_pos = len(job_section)
    for marker in end_markers:
        pos = job_section.lower().find(marker.lower())
        if pos != -1:
            end_pos = min(end_pos, pos)

    job_section = job_section[:end_pos].strip()

    # Split into lines and process
    lines = job_section.split('\n')

    items = []
    current_item = None
    prev_level = 0
    item_stack = [items]  # Stack to track hierarchy

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is an item line
        if detect_item_line(line):
            number_str, text = extract_number_and_text(line)
            level = determine_hierarchy_level(number_str)

            current_item = {
                "number": number_str,
                "description": text,
                "level": level,
                "pricing": None,
                "children": [],
            }

            # Extract pricing from current line if present
            if "–" in text or "=" in text or "₱" in text:
                current_item["pricing"] = parse_pricing_from_line(text)
                # Remove pricing from description
                current_item["description"] = re.sub(
                    r'\s*[–=]\s*₱[\d,/()ft\s×-]*',
                    '',
                    text,
                    flags=re.IGNORECASE
                ).strip()

            # Manage hierarchy
            if level == 1:
                items.append(current_item)
                item_stack = [items, current_item["children"]]
                prev_level = 1
            elif level == 2 and prev_level >= 1:
                if item_stack[-1] is not None:
                    items[-1]["children"].append(current_item)
                    item_stack.append(current_item["children"])
                prev_level = 2
            elif level == 3 and prev_level >= 2:
                if items and items[-1]["children"]:
                    items[-1]["children"][-1]["children"].append(current_item)
                prev_level = 3
            else:
                items.append(current_item)
                prev_level = level

        elif current_item is not None:
            # Multi-line description or additional pricing line
            if re.search(r'₱', line):
                # This line contains pricing information
                if "Plus:" in line or "Additional:" in line or "Total Price" in line:
                    # Additional pricing or total marker
                    if "Total Price" in line:
                        current_item["total_price"] = line
                    else:
                        # Add to pricing structure
                        if current_item["pricing"] is None:
                            current_item["pricing"] = {}
                        if "additional" not in current_item["pricing"]:
                            current_item["pricing"]["additional"] = []
                        current_item["pricing"]["additional"].append(parse_pricing_from_line(line))
                else:
                    # Calculation line (distance surcharge, etc.)
                    if current_item["pricing"] is None:
                        current_item["pricing"] = {}
                    if "calculations" not in current_item["pricing"]:
                        current_item["pricing"]["calculations"] = []
                    current_item["pricing"]["calculations"].append(line)
            else:
                # Append to description
                current_item["description"] += " " + line

    # Clean up empty children
    def clean_items(item_list):
        for item in item_list:
            if item["children"]:
                clean_items(item["children"])
            else:
                del item["children"]

    clean_items(items)

    return items


def extract_quotation_items(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured items from full quotation JSON.

    Args:
        json_data: Full extracted JSON with "extracted_text" key

    Returns:
        Dict with filename, items, counts, and analysis metadata
    """
    extracted_text = json_data.get("extracted_text", "")
    filename = json_data.get("filename", "unknown")

    items = parse_item_section(extracted_text)

    # Count hierarchy depth
    def get_max_depth(item_list, current_depth=1):
        if not item_list:
            return current_depth
        max_d = current_depth
        for item in item_list:
            if "children" in item and item["children"]:
                max_d = max(max_d, get_max_depth(item["children"], current_depth + 1))
        return max_d

    hierarchy_depth = get_max_depth(items) if items else 0

    # Detect pricing patterns used
    pricing_patterns = set()

    def collect_patterns(item_list):
        for item in item_list:
            if item.get("pricing") and item["pricing"].get("format"):
                pricing_patterns.add(item["pricing"]["format"])
            if "children" in item and item["children"]:
                collect_patterns(item["children"])

    collect_patterns(items)

    # Detect location grouping (items with location-like labels)
    has_location_grouping = False
    location_keywords = ['floor', 'room', 'dept', 'office', 'area', 'section']
    for item in items:
        desc_lower = item["description"].lower()
        if any(kw in desc_lower for kw in location_keywords):
            has_location_grouping = True
            break

    return {
        "filename": filename,
        "items": items,
        "item_count": len(items),
        "hierarchy_depth": hierarchy_depth,
        "has_location_grouping": has_location_grouping,
        "pricing_patterns": sorted(list(pricing_patterns)),
    }


def main():
    """
    Test function: Load sample JSON and parse items.
    """
    # Find a sample extracted JSON
    base_path = Path("/home/jay/Desktop/Coding Stuff/cbvt-quotation-generator")
    extraction_dir = base_path / "output" / "extraction_output"

    sample_file = None
    if extraction_dir.exists():
        json_files = list(extraction_dir.glob("*_extracted.json"))
        if json_files:
            sample_file = json_files[0]

    if not sample_file:
        print("ERROR: No sample JSON found in extraction_output")
        return

    print(f"Loading: {sample_file.name}")
    print("=" * 80)

    with open(sample_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    result = extract_quotation_items(json_data)

    print(f"Filename: {result['filename']}")
    print(f"Item Count: {result['item_count']}")
    print(f"Hierarchy Depth: {result['hierarchy_depth']}")
    print(f"Location Grouping: {result['has_location_grouping']}")
    print(f"Pricing Patterns: {result['pricing_patterns']}")
    print("\n" + "=" * 80)
    print("ITEMS:")
    print("=" * 80)

    def print_item(item, indent=0):
        prefix = "  " * indent
        print(f"{prefix}[{item['number']}] Level {item['level']}: {item['description'][:60]}")
        if item.get("pricing"):
            pricing = item["pricing"]
            if pricing.get("format"):
                print(f"{prefix}  → Pricing: {pricing['format']}", end="")
                if pricing.get("unit_price"):
                    print(f" (₱{pricing['unit_price']}/unit = ₱{pricing.get('total', '?')})", end="")
                elif pricing.get("amount"):
                    print(f" (₱{pricing['amount']:,})", end="")
                print()
        if "children" in item:
            for child in item["children"]:
                print_item(child, indent + 1)

    for item in result["items"]:
        print_item(item)

    print("\n" + "=" * 80)
    print("FULL RESULT (JSON):")
    print("=" * 80)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
