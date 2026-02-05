#!/usr/bin/env python3
"""
Analyze quotation extraction formats and generate summary report.

Reads all *_extracted.json files from extraction_output/
Produces FORMAT_ANALYSIS.json with format patterns, variations, and anomalies.
"""

import json
import os
import sys
from collections import defaultdict, Counter
from pathlib import Path
from statistics import median


def load_extracted_files(extraction_dir):
    """Load all *_extracted.json files from the extraction output directory."""
    files_data = []

    for filename in os.listdir(extraction_dir):
        if filename.endswith('_extracted.json') and not filename.startswith('_'):
            filepath = os.path.join(extraction_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    files_data.append({
                        'filename': filename,
                        'filepath': filepath,
                        'data': data
                    })
            except Exception as e:
                print(f"Warning: Failed to load {filename}: {e}", file=sys.stderr)

    return files_data


def analyze_files(files_data):
    """Analyze all extracted files and produce format insights."""

    if not files_data:
        print("Error: No *_extracted.json files found.", file=sys.stderr)
        return None

    total_files = len(files_data)

    # Track field presence
    field_counts = Counter()
    all_fields = set()
    field_files = defaultdict(list)  # field -> list of files that have it

    # Track structure metrics
    page_counts = Counter()
    text_lengths = []
    file_structures = []  # Track which fields each file has

    # Collect all data
    for file_info in files_data:
        filename = file_info['filename']
        data = file_info['data']

        detected_fields = data.get('detected_fields', {})
        page_count = data.get('page_count', 1)
        extracted_text = data.get('extracted_text', '')

        # Track fields
        field_set = set(detected_fields.keys())
        file_structures.append({
            'filename': filename,
            'fields': field_set,
            'page_count': page_count,
            'text_length': len(extracted_text)
        })

        for field in field_set:
            field_counts[field] += 1
            all_fields.add(field)
            field_files[field].append(filename)

        # Track metrics
        page_counts[page_count] += 1
        text_lengths.append(len(extracted_text))

    # Find common fields (>90% threshold)
    threshold = total_files * 0.9
    common_fields = [field for field, count in field_counts.items() if count > threshold]
    common_fields.sort()

    # Build field variations
    field_variations = {}
    for field in sorted(all_fields):
        count_with = field_counts[field]
        count_without = total_files - count_with
        field_variations[field] = {
            'files_with_field': count_with,
            'files_without': count_without
        }

    # Group into format classes based on field combinations
    format_classes = identify_format_classes(file_structures, common_fields)

    # Page count distribution
    page_count_dist = {f"{k}_page{'s' if k != 1 else ''}": v
                      for k, v in sorted(page_counts.items())}

    # Text length stats
    text_stats = {
        'min': min(text_lengths),
        'max': max(text_lengths),
        'median': int(median(text_lengths))
    }

    # Find anomalies
    anomalies = detect_anomalies(file_structures, common_fields, text_stats)

    return {
        'total_files_analyzed': total_files,
        'common_fields': common_fields,
        'field_variations': field_variations,
        'format_classes': format_classes,
        'page_count_distribution': page_count_dist,
        'extracted_text_length_stats': text_stats,
        'anomalies': anomalies
    }


def identify_format_classes(file_structures, common_fields):
    """Group files into format classes based on field combinations."""

    # Create a signature for each file (which common fields it has)
    signatures = defaultdict(list)

    for file_info in file_structures:
        filename = file_info['filename']
        fields = file_info['fields']

        # Create signature: tuple of common fields present
        sig = tuple(sorted([f for f in common_fields if f in fields]))
        signatures[sig].append(filename)

    # Convert to format classes
    classes = []
    for idx, (sig, files) in enumerate(sorted(signatures.items(),
                                               key=lambda x: -len(x[1]))):
        characteristic_fields = list(sig)

        # Select up to 5 example files
        example_files = files[:5]

        class_name = f"Format Class {chr(65 + idx)}"
        if len(characteristic_fields) == len(common_fields):
            class_name += ": Complete Format (all common fields)"
        else:
            missing_count = len(common_fields) - len(characteristic_fields)
            class_name += f": Variant ({missing_count} common field(s) missing)"

        classes.append({
            'class_name': class_name,
            'file_count': len(files),
            'characteristic_fields': characteristic_fields,
            'example_files': example_files
        })

    return classes


def detect_anomalies(file_structures, common_fields, text_stats):
    """Identify files with unusual structures or outliers."""

    anomalies = []

    median_length = text_stats['median']
    very_short_threshold = median_length * 0.5
    very_long_threshold = median_length * 2

    for file_info in file_structures:
        filename = file_info['filename']
        fields = file_info['fields']
        text_len = file_info['text_length']
        page_count = file_info['page_count']

        issues = []

        # Check for missing common fields
        missing_common = [f for f in common_fields if f not in fields]
        if missing_common:
            issues.append(f"Missing {len(missing_common)} common field(s): {', '.join(missing_common[:3])}")

        # Check for unusual text length
        if text_len < very_short_threshold:
            issues.append(f"Unusually short text ({text_len} chars, median is {median_length})")
        elif text_len > very_long_threshold:
            issues.append(f"Unusually long text ({text_len} chars, median is {median_length})")

        # Check for unusual page count
        if page_count > 5:
            issues.append(f"Very high page count: {page_count} pages")

        if issues:
            anomalies.append({
                'file': filename,
                'issue': '; '.join(issues)
            })

    return anomalies


def main():
    """Main execution."""

    # Determine extraction output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    extraction_dir = os.path.join(project_root, 'output', 'extraction_output')

    if not os.path.isdir(extraction_dir):
        print(f"Error: Extraction directory not found: {extraction_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading extracted files from: {extraction_dir}")
    files_data = load_extracted_files(extraction_dir)
    print(f"Loaded {len(files_data)} extracted files")

    print("Analyzing format patterns...")
    analysis = analyze_files(files_data)

    if not analysis:
        sys.exit(1)

    # Write output
    output_file = os.path.join(extraction_dir, 'FORMAT_ANALYSIS.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)

    print(f"\nFormat analysis complete!")
    print(f"Output written to: {output_file}")
    print(f"\nSummary:")
    print(f"  Total files: {analysis['total_files_analyzed']}")
    print(f"  Common fields (>90%): {len(analysis['common_fields'])}")
    print(f"  Format classes identified: {len(analysis['format_classes'])}")
    print(f"  Anomalies detected: {len(analysis['anomalies'])}")


if __name__ == '__main__':
    main()
