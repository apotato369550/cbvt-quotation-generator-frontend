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
from parse_quotation_items import extract_quotation_items


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

    # Track item structures (for item structure analysis)
    item_structures = []  # List of item analysis results

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

        # Parse item structure
        try:
            item_result = extract_quotation_items(data)
            item_structures.append(item_result)
        except Exception as e:
            print(f"Warning: Failed to parse items in {filename}: {e}", file=sys.stderr)

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

    # Analyze item structures
    item_structure_analysis = analyze_item_structures(item_structures)

    return {
        'total_files_analyzed': total_files,
        'common_fields': common_fields,
        'field_variations': field_variations,
        'format_classes': format_classes,
        'page_count_distribution': page_count_dist,
        'extracted_text_length_stats': text_stats,
        'anomalies': anomalies,
        'item_structure_analysis': item_structure_analysis
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


def analyze_item_structures(item_structures):
    """
    Aggregate item structure metrics across all files.

    Args:
        item_structures: List of results from extract_quotation_items()

    Returns:
        Dict with aggregated metrics for item_structure_analysis section
    """
    if not item_structures:
        return {
            'item_count_stats': {'min': 0, 'max': 0, 'median': 0, 'mean': 0},
            'hierarchy_depth_distribution': {'1_level': 0, '2_levels': 0, '3_levels': 0},
            'location_grouping': {'files_with_grouping': 0, 'percentage': 0},
            'pricing_patterns_frequency': {},
            'sample_item_extractions': []
        }

    # Collect item counts
    item_counts = [item['item_count'] for item in item_structures]

    # Collect hierarchy depths
    hierarchy_depths = [item['hierarchy_depth'] for item in item_structures]

    # Collect location grouping info
    files_with_location = sum(1 for item in item_structures if item['has_location_grouping'])

    # Aggregate pricing patterns
    pricing_pattern_freq = Counter()
    for item in item_structures:
        for pattern in item['pricing_patterns']:
            pricing_pattern_freq[pattern] += 1

    # Build hierarchy depth distribution
    hierarchy_dist = {
        '1_level': sum(1 for d in hierarchy_depths if d == 1),
        '2_levels': sum(1 for d in hierarchy_depths if d == 2),
        '3_levels': sum(1 for d in hierarchy_depths if d == 3),
    }

    # Calculate item count statistics
    item_stats = {
        'min': min(item_counts) if item_counts else 0,
        'max': max(item_counts) if item_counts else 0,
        'median': int(median(item_counts)) if item_counts else 0,
        'mean': int(sum(item_counts) / len(item_counts)) if item_counts else 0,
    }

    # Build sample extractions (up to 10 diverse examples)
    sample_extractions = []
    # Sort by item count to get diverse examples
    sorted_items = sorted(item_structures, key=lambda x: x['item_count'])

    # Select every nth item to get diversity
    step = max(1, len(sorted_items) // 10)
    for idx in range(0, len(sorted_items), step):
        if len(sample_extractions) < 10:
            item = sorted_items[idx]
            sample_extractions.append({
                'filename': item['filename'],
                'item_count': item['item_count'],
                'hierarchy_depth': item['hierarchy_depth'],
                'has_location_grouping': item['has_location_grouping'],
                'pricing_patterns': item['pricing_patterns']
            })

    return {
        'item_count_stats': item_stats,
        'hierarchy_depth_distribution': hierarchy_dist,
        'location_grouping': {
            'files_with_grouping': files_with_location,
            'percentage': f"{(files_with_location / len(item_structures) * 100):.1f}%"
        },
        'pricing_patterns_frequency': dict(pricing_pattern_freq),
        'sample_item_extractions': sample_extractions
    }


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
    if 'item_structure_analysis' in analysis:
        item_stats = analysis['item_structure_analysis']['item_count_stats']
        print(f"\nItem Structure Analysis:")
        print(f"  Item count range: {item_stats['min']}-{item_stats['max']} (median: {item_stats['median']}, mean: {item_stats['mean']})")
        print(f"  Hierarchy depths: {analysis['item_structure_analysis']['hierarchy_depth_distribution']}")
        print(f"  Location grouping: {analysis['item_structure_analysis']['location_grouping']['percentage']} of files")
        print(f"  Pricing patterns: {len(analysis['item_structure_analysis']['pricing_patterns_frequency'])} types found")


if __name__ == '__main__':
    main()
