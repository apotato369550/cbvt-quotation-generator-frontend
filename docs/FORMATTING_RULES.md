# Formatting Rules: Cebu Best Value Trading Corp. Quotations

## Overview

This document codifies the visual and structural formatting patterns observed across 346 quotation documents issued by Cebu Best Value Trading Corp. (CBVTC). The analysis is based on visual inspection of PDF samples and extraction of 10 diverse JSON-extracted quotations spanning three client categories (Homemaker Furniture, University of Cebu, Standard Insurance, WTS Constech, BC), multiple dates (2023-2025), and varying item complexity.

---

## Header Section

### Company Name and Location
- **Placement**: Top-center of page, bold, large font (estimated 12-14pt)
- **Text**: "Cebu Best Value Trading Corp."
- **Below**: Underlined separator line spanning full width (approximately 80 characters of underscores)
- **Location**: "Cebu City" centered below separator, regular font (10-11pt)

### Contact Information
- **Placement**: Directly below company name/location section
- **Format**: "Telephone Number: [phone] || Mobile Number: [provider]-[number] [provider]-[number]"
- **Example**: "Telephone Number: 032-2670573 || Mobile Number: Sun-09325314857 Globe-09154657503"
- **Font**: Regular, 9-10pt, underlined
- **Spacing**: Approximately 1 line break above and 2 lines below

### Service Categories Line
- **Placement**: After contact info, approximately 1-2 lines below
- **Format**: "Sales  Installation  Service  Repair" centered, with "Ductworks" on second line
- **Font**: Bold, 10-11pt for categories; "Ductworks" in regular font
- **Spacing**: Visual spacing equal across categories

---

## Customer Section

### Date Field
- **Label**: "Date :"
- **Placement**: Left-aligned, 1-2 lines below service categories
- **Format**: MM/DD/YYYY (e.g., "10/16/2025")
- **Font**: Regular, 10pt
- **Indentation**: Starts at left margin with label followed by colon

### "To" Field (Client Name)
- **Label**: "To :"
- **Placement**: Directly below Date field (same left alignment)
- **Content**: Company/person name, may span 1-3 lines depending on name length
- **Examples**:
  - "Homemaker" / "Mandaue City" (multi-line)
  - "University of Cebu, Banilad" / "Cebu City" (multi-line)
  - "Standard Insurance" / "Cebu City" (multi-line)
- **Font**: Regular, 10pt
- **Spacing**: 0.5-1 line between Date and To fields

### Attention Field
- **Label**: "Attention :"
- **Placement**: Directly below To field (same left alignment)
- **Content**: Recipient name and optional title/role
- **Examples**:
  - "Madame Judith Casas – Purchasing in-charge"
  - "Mrs. Alice Bacalso"
  - "Mr. Raul N. Arnibal – Purchasing in-charge"
  - Empty/blank for some quotations (approximately 1/346)
- **Font**: Regular, 10pt
- **Format**: Title/role follows name after dash or comma
- **Spacing**: 0.5-1 line between To and Attention fields

### Greeting
- **Placement**: Below Attention field, 1 line break
- **Content**: "Sir/Madam," or "Madame," or "Sir/Madame," depending on context
- **Font**: Regular, 10pt
- **Indentation**: 0.5-1 tab indent or 4-5 spaces

### Reference Statement
- **Placement**: Below greeting, 0.5-1 line break
- **Content**: "This is with reference to your request for quotation for the installation/repair of the following air-conditioner to be installed at:_________________________________________________"
- **Font**: Regular, 10pt
- **Line fills**: Blank line with underscores for handwritten location entry
- **Spacing**: Line break after

---

## Introduction Section

### "We are pleased to quote" Statement
- **Placement**: 0.5-1 line break below reference statement
- **Content**: "We are pleased to quote the following:"
- **Font**: Regular, 10pt
- **Indentation**: 0.5-1 tab or 4-5 spaces
- **Spacing**: 0.5-1 line break after

### "Job to be done" Header
- **Placement**: After "pleased to quote" statement, 0.5-1 line break
- **Content**: "Job to be done :" with colon and optional underscore fill
- **Font**: Underlined, bold, 10pt
- **Indentation**: 0 (left-aligned or very slight indent)
- **Spacing**: 0.5-1 line break after before first item

---

## Items Section

### Hierarchy and Numbering

#### Level 1 (Primary Items/Locations/Departments)
- **Numbering**: Arabic numerals (1, 2, 3, ...) followed by period
- **Format**: "1. DEPT - [Department Name]" or "1. [Location Name] - [Description]"
- **Examples**:
  - "1. DEPT - Anatomy Lab - 1 (Installation Only)"
  - "1. Sales Division - One(1) Panasonic Air conditioner 2.5Hp"
  - "1. Six(6) units Ceiling Cassettes Air Conditioner"
- **Font**: Bold, 10-11pt
- **Indentation**: 0 (left-aligned, or minimal left margin)
- **Spacing**: 0.5-1 line above and below level 1 item

#### Level 2 (Sub-items under Level 1)
- **Numbering**: Arabic numerals or sub-bullets (1., 2., 3., ... or indented items)
- **Format**: Detailed findings, recommendations, or service line items
- **Examples**:
  - "1. Findings – Compressor Loose Compression (Beyond Repair)"
  - "2. Recommendations – Replace with One(1) new Koppel Floor-mounted"
  - "1. General cleaning of the entire unit by supplying chemicals – ₱600"
- **Font**: Regular, 10pt
- **Indentation**: 1-2 tabs (approximately 0.5-0.75 inches) from left margin
- **Spacing**: Single-spaced within level 1 group

#### Level 3 (Sub-sub-items)
- **Numbering**: Continued Arabic numerals (1., 2., 3., ...)
- **Format**: Breakdown of level 2 items
- **Examples**:
  - "(1) One(1) Carrier Floor-mounted Air Conditioner 3Trs"
  - "At maximum distance of 10ft only – ₱10,500"
  - "Additional installation costs in excess of 10ft (₱350/ft)"
- **Font**: Regular, 10pt
- **Indentation**: 1.5-2.5 tabs (approximately 0.75-1.25 inches) from left margin
- **Spacing**: Single-spaced or minimal line breaks

### Price Placement

#### Inline Prices
- **Format**: Price appears on same line as item, after dash
- **Example**: "1. General cleaning of the entire unit by supplying chemicals – ₱600"
- **Currency**: Philippine Peso symbol (₱) followed by amount
- **Font**: Regular, 10pt
- **Alignment**: Right side of line or after description

#### Sub-total Prices
- **Format**: "Total Price – ₱ [amount]" on separate line
- **Placement**: After all sub-items, indented to match sub-item level
- **Example**: "Total Price – ₱ 13,750"
- **Font**: Regular, 10pt
- **Spacing**: 0.5-1 line break above and below

#### Grand Total Price
- **Placement**: After all grouped items
- **Format**: "Total Price of items 1, 2, and 3 – ₱ [amount]" or "Total Price – ₱ [amount]"
- **Examples**:
  - "Total Price of items 1, 2, and 3 – ₱ 9,050"
  - "Total Price – ₱ 252,348.00"
  - "Total Price = ₱ 8,800"
- **Font**: Regular, 10pt, sometimes bold
- **Indentation**: 0-0.5 tabs from left margin
- **Spacing**: 1-2 line breaks above and below

### Numbering Style Patterns

**Observed Patterns**:
1. **Consistent use of Arabic numerals** (1., 2., 3.) across all hierarchy levels
2. **No Roman numerals** (i., ii., iii.) observed in main items
3. **Letter designations** (a., b., c.) not used in primary numbering
4. **Sub-items occasionally parenthetical** (1), (2) for sub-sub-items

---

## Summary Section

### Warranty Field

#### Placement
- **Position**: Below all item pricing, 1-2 line breaks
- **Label**: "Warranty:" left-aligned, optional bold

#### Format Variations
- **Complete warranty statement** (most common, ~99%):
  - "Warranty: One(1) Year for parts + One(1) Year for the compressor"
  - "Warranty: None, including compressor and all spare parts"
  - "Warranty: Gen. Cleaning - NO Warranty, including compressor and all spare parts; Repair - Ninety (90) days, excluding compressor and all spare parts"
- **No warranty field** (rare, ~1%):
  - Omitted entirely in some quotations

#### Content
- **Font**: Regular, 10pt
- **Typical duration phrases**: "One(1) Year", "Ninety (90) days", "None"
- **Exclusions**: Always specify what is NOT covered (e.g., "excluding compressor and all spare parts")
- **Indentation**: Continuation lines indented 0.5-1 tab if multi-line

### Terms of Payment Field

#### Placement
- **Position**: Before or after Warranty field, no fixed order observed
- **Label**: "Terms of Payment:" left-aligned, optional bold

#### Format Variations
- **COD (Cash on Delivery)**: "Terms of Payment: COD (Cash on delivery)"
- **Full payment upfront**: "Terms of Payment: Full Payment Before Repair + Cleaning"
- **Cash before delivery**: "Terms of Payment: Cash Before Delivery (₱51,500)"
- **Cash upon completion**: "Terms of Payment: Cash upon completion"

#### Content
- **Font**: Regular, 10pt
- **Indentation**: Continuation lines indented 0.5-1 tab if multi-line

### Exception/Notes Field

#### Placement
- **Position**: After Warranty and Terms of Payment, or within warranty block
- **Label**: "Exception:" or "Note :" left-aligned, optional bold

#### Format
- **Standard exceptions** (consistent across all quotations):
  1. "(1) Circuit breaker and Gov't Fees"
  2. "(2) Power Supply"
  - Alternative (rare): "(1) Power Supply; (2) Circuit breaker and Gov't Fees"

#### Special Notes (occasional)
- **Placement**: Integrated with exception field or separate
- **Example**: "Note : The check issued must be payable to Concordia C. Yap"
- **Example**: "Exception : Any spare parts to be replaced or repaired shall be charged to the account of the customer"
- **Font**: Regular, 10pt
- **Indentation**: 0.5-1 tab for continuation lines

### Spacing Between Summary Sections
- **Above Warranty**: 1-2 line breaks from last item price
- **Between Warranty/Terms**: 0.5-1 line break
- **Between Terms/Exception**: 0.5-1 line break
- **Below Exception**: 1-2 line breaks before closing statement

---

## Closing Section

### Thank You Statement
- **Placement**: 1-2 line breaks below exception field
- **Content**: "Thank you very much for giving us the opportunity to quote and we hope to have the pleasure of serving you."
- **Font**: Regular, 10pt
- **Indentation**: 0.5-1 tab indent or centered
- **Line break**: 1-2 lines below

### Closing Salutation
- **Placement**: 1 line break below thank you
- **Content**: "Very Truly Yours,"
- **Font**: Regular, 10pt
- **Indentation**: Right-aligned or 0.5-1 tab indent

### Signature Block

#### Conforme Line
- **Label**: "Conforme:______________"
- **Font**: Regular, 10pt
- **Placement**: 2-3 lines below "Very Truly Yours," (space for handwritten signature)
- **Length**: Approximately 10-15 underscores

#### Manager Name/Title Line
- **Placement**: Right side, aligned vertically with Conforme line or below
- **Format**: "J.B Yap Jr." followed by title on next line
- **Example**:
  ```
  Conforme:______________     J.B Yap Jr.
  Date:__________________     Manager Q
  ```
- **Font**: Regular, 10pt (or handwritten for actual signature)
- **Title**: "Manager", "Manager Q", or "Manager" only

#### Date Signature Line
- **Label**: "Date:__________________"
- **Font**: Regular, 10pt
- **Placement**: Below Conforme line (space for handwritten date)
- **Length**: Approximately 10-15 underscores

#### Quotation Number
- **Format**: "#1", "#2", etc.
- **Placement**: Bottom right or bottom center of page
- **Font**: Regular, 9pt
- **Meaning**: Sequential quotation number or revision number

---

## Visual Elements

### Separator Lines

#### Company Header Separator
- **Style**: Full-width underscores (approximately 80 characters)
- **Placement**: Below company name, framing "Cebu City"
- **Examples**: `____________________________________ Cebu City ____________________________________`
- **Purpose**: Visual separation between company header and contact info

#### Section Underlines
- **Style**: Underscored text for headers
- **Examples**: "Job to be done:", "Warranty:", "Terms of Payment:"
- **Placement**: Directly under label text
- **Purpose**: Visual distinction and section clarity

#### Fill Lines
- **Style**: Underscores for blank entry fields
- **Examples**: 
  - "to be installed at:_________________________________________________"
  - "Conforme:______________"
  - "Date:__________________"
- **Purpose**: Space for handwritten entries or signatures

### Fonts and Sizes

#### Estimated Font Hierarchy
| Section | Element | Size | Style |
|---------|---------|------|-------|
| Header | Company name | 12-14pt | Bold |
| Header | Contact info | 9-10pt | Regular, underlined |
| Header | Service categories | 10-11pt | Bold (categories), Regular (Ductworks) |
| Customer | Date/To/Attention labels | 10pt | Regular |
| Items | Level 1 numbering | 10-11pt | Bold |
| Items | Level 2/3 details | 10pt | Regular |
| Summary | Labels (Warranty, Terms, Exception) | 10pt | Regular/Bold |
| Closing | Body text | 10pt | Regular |
| Closing | Manager signature | 10pt | Regular or handwritten |

#### Typography Observations
- **Primary font**: Times New Roman or similar serif font (estimated from visual inspection)
- **Bold usage**: Limited to headers, level 1 items, and company name
- **Underline usage**: Contact info, section headers, fill lines
- **No color**: All documents appear monochrome (black text on white)
- **No decorative fonts**: Consistent professional appearance

### Page Layout and Margins

#### Standard Page Dimensions
- **Size**: Letter size (8.5" x 11")
- **Margins**: 
  - Left: 0.5-0.75 inches
  - Right: 0.5-0.75 inches
  - Top: 0.5-0.75 inches (header begins near top)
  - Bottom: 0.5-1 inch (signature block at bottom of page)

#### Page Breaks
- **Typical layout**: 2-page quotations (99% of sample)
  - Page 1: Header, customer info, items section, partial summary
  - Page 2: Continuation of items/summary, closing, signature block
- **Page indicators**: "Page 1", "Page 2" marked at bottom of some documents
- **Pagination**: Bottom center or bottom right

#### Vertical Spacing Guidelines

| Section Transition | Spacing |
|--------------------|---------|
| Header to Date | 1-2 line breaks |
| Date to To | 0.5-1 line break |
| To to Attention | 0.5-1 line break |
| Attention to Greeting | 1 line break |
| Greeting to Reference | 0.5-1 line break |
| Reference to "Pleased to Quote" | 0.5-1 line break |
| "Pleased to Quote" to "Job to be done" | 0.5-1 line break |
| Job header to First Item | 0.5-1 line break |
| Level 1 items to next Level 1 | 0.5-1 line break |
| Last item to Total Price | 0.5-1 line break |
| Total Price to Warranty | 1-2 line breaks |
| Summary sections (Warranty/Terms/Exception) | 0.5-1 line break |
| Exception to Thank you | 1-2 line breaks |
| Thank you to "Very Truly Yours" | 1 line break |
| "Very Truly Yours" to Signature block | 2-3 line breaks |

---

## Pricing Patterns

### Price Format
- **Currency symbol**: Philippine Peso (₱) always precedes amount
- **Spacing**: Consistent space between ₱ and number (₱ 600, ₱1,500, ₱ 8,800)
- **Decimal places**:
  - Without decimals: ₱600, ₱1,500, ₱9,050 (majority)
  - With decimals: ₱24,720.00, ₱60,036.00, ₱252,348.00 (less common, ~20%)
- **Thousands separator**: Comma used for amounts ≥1,000 (₱1,500, ₱24,720)

### Price Placement Logic
- **Per-unit prices**: Appear on same line as item, after dash
  - "Six(6) units Ceiling Cassettes Air Conditioner – ₱1000/unit = ₱ 6,000"
- **Calculated totals**: Multi-line calculation shown
  - "Additional installation costs in excess of 10ft (₱350/ft) ... = ₱23,800"
- **Item sub-totals**: "Total Price – ₱ [amount]" at end of grouped items
- **Grand total**: "Total Price of items 1, 2, and 3 – ₱ [amount]" at end of all items

### Pricing Pattern Categories (from FORMAT_ANALYSIS.json)
- **Lump-sum pricing** (147 files, ~43%): Single total for service/item
- **Unit-based pricing** (17 files, ~5%): Per-unit cost multiplied by quantity
- **Additive pricing** (3 files, <1%): Multiple line items summed to total
- **No pricing** (50 files, ~14%): Quotations without total price field (rare)

---

## Anomalies and Exceptions

### Missing Fields (from FORMAT_ANALYSIS.json analysis of 346 files)
- **Attention field**: Missing in 1 file (0.3%)
  - Quotation still valid; replaced with "Sir/Madam," greeting
- **Terms of Payment**: Missing in 5 files (1.4%)
  - Format Class B and C variants (4 UC summary documents)
- **Warranty field**: Missing in 5 files (1.4%)
  - Format Class B and C variants
- **Total Price**: Missing in 50 files (14.5%)
  - Typically summary quotations or consolidated quotes without line items

### Location Grouping
- **Files with location grouping**: 315 (91%)
  - Items organized by department, floor, or physical location
- **Files without location grouping**: 31 (9%)
  - Items listed sequentially without location headers

### Multi-page Layouts
- **1-page quotations**: 35 (10.1%)
- **2-page quotations**: 309 (89.3%)
- **3-page quotations**: 1 (0.3%)
- **7-page quotations**: 1 (0.3%)

### Item Complexity
- **Hierarchy depth distribution**:
  - 1 level (single-tier items): 240 files (69%)
  - 2 levels (items with sub-items): 87 files (25%)
  - 3 levels (deeply nested): 14 files (4%)
- **Item count range**: 0-28 items per quotation (median: 6 items)

---

## Key Formatting Takeaways

1. **Consistency is paramount**: 99% of quotations follow the same structure (Format Class A)
2. **Hierarchical numbering**: Always Arabic numerals, left-aligned, consistent indentation per level
3. **Price placement**: Prices follow descriptions on same line or appear as calculated sub-totals
4. **Summary blocks**: Warranty, Terms of Payment, and Exceptions always appear before closing
5. **Signature block**: Always includes "Conforme:", date line, manager name (J.B Yap Jr.), and quotation number
6. **Page layout**: 2-page standard; items may flow to page 2 with signature block at bottom
7. **Typography**: Professional serif font, minimal styling (bold for headers only), no color
8. **Margins**: Consistent 0.5-0.75 inch margins on all sides
9. **Spacing**: Consistent line breaks between sections (0.5-2 line breaks depending on context)
10. **Special notation**: Always includes exception list (Circuit breaker/Gov't Fees, Power Supply) as risk disclaimer

---

## Sample Quotation Structure (Annotated)

```
[HEADER SECTION]
Cebu Best Value Trading Corp.
__________________________________ Cebu City ____________________________________
Telephone Number: 032-2670573 || Mobile Number: Sun-09325314857 Globe-09154657503
Sales  Installation  Service  Repair
                    Ductworks

[CUSTOMER SECTION]
Date : 10/16/2025
To : Homemaker
     Mandaue City
Attention : [blank or name]

[GREETING/REFERENCE]
Sir/Madam,

This is with reference to your request for quotation for the installation/repair of the
following air-conditioner to be installed at:_________________________________________________

[INTRODUCTION]
We are pleased to quote the following:

Job to be done:

[ITEMS SECTION]
1. Sales Division - One(1) Panasonic Air conditioner 2.5Hp
   1. General cleaning of the entire unit by supplying chemicals – ₱600
      Warranty - None, including compressor + all parts

[PRICING]
Total Price of items 1, 2, and 3 – ₱ 9,050

[SUMMARY SECTION]
Terms of Payment: Full Payment Before Repair + Cleaning
Warranty: Gen. Cleaning - NO Warranty, including compressor and all spare parts
          Repair - Ninety (90) days, excluding compressor and all spare parts
Exception: (1) Circuit breaker and Gov't Fees
           (2) Power Supply

[CLOSING]
Thank you very much for giving us the opportunity to quote and we hope to have the
pleasure of serving you.

Very Truly Yours,

Conforme:______________              J.B Yap Jr.
Date:__________________              Manager Q

#1
```

---

## References

- **Data source**: 346 quotation PDFs from Cebu Best Value Trading Corp. (2023-2025)
- **Extraction method**: OCR text extraction and PDF visual inspection
- **Analysis period**: February 2025
- **Consistency rate**: 98.6% adherence to Format Class A (341 of 346 files)

