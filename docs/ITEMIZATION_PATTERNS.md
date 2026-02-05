# Itemization Patterns Analysis

## Summary
- **Total files sampled:** 20
- **Numbering schemes found:** 6 distinct primary patterns
- **Hierarchy depth observed:** 3 levels maximum (primary > secondary > tertiary)
- **Key patterns identified:**
  - Decimal numbering (1., 2.) dominates primary level
  - Alphabetic sub-items (a., b., c.) used for secondary level
  - Roman numerals rare; numeric (1), (2) more common for sub-steps
  - Pricing consistently shown after item description with dash separator
  - Total Price lines appear at section or overall level
  - Location/room groupings create implicit hierarchy even when numbering resets

---

## Numbering Schemes

### Primary Level: Decimal Notation (1., 2., 3., etc.)
**Pattern:** "1. Item description – ₱amount" or "1. Item description\n– ₱amount"

**Files using:**
- BC-1-5_15_2024 ("1. Forty-nine(49) units... – ₱29,400")
- Bible-Baptist-Church-1-12_4_2023 ("1. Two(2) units Daikin... – ₱99,800/unit = ₱199,600")
- Homemaker-Furniture-1-10_26_2023 ("1. One(1) Daikin Wall Mounted...")
- Don-Bosco-Technical-College-1-12_12_2023 ("1. Twenty Two(22) units...")
- Standard-Insurance-1-11_13_2025 ("1. Six(6) units Ceiling Cassette...")
- Jamari-Construction series (all 5 files) ("1. Nursing Station Hall", "1. Forty-nine(49) units...")

**Frequency:** 18/20 files use decimal notation as primary level.

---

### Secondary Level: Alphabetic Notation (a., b., c., etc.)
**Pattern:** "a. Sub-item description – ₱amount"

**Files using:**
- Bible-Baptist-Church-1-12_4_2023 ("a. Installation Only")
- Benedicto+Sons-1-5_9_2024 ("a. Installation Only", "1. One(1) Daikin...", "2. Additional installation costs...")
- Crossworld-Cebu-1-8_5_2024 ("1. Check the Leak portion", "2. Reweld the leak portion"... as steps, not labeled a/b)

**Frequency:** Only 2-3 files explicitly use alphabetic sub-items; most use numeric sub-steps.

---

### Tertiary Level: Numeric Step Lists (1), (2), (3) or direct numbering
**Pattern:** "1. Sub-step description" or "(1) Multi-line descriptor"

**Files using:**
- Exquisite-Pawnshop-1-7_3_25 ("1. Pull down the AHU unit", "2. Supply one(1) lot...", etc.)
- Homemaker-Furniture-1-10_16_2025 ("1. General cleaning...", "2. Supply one(1) lot...", etc.)
- St. Mary Academy files (similar sub-step structure)
- Kinton-Lodging-Inn-1 ("1. Lobby:", "1. One(1) unit Daikin...", "(1) One(1) unit Daikin...")

**Frequency:** 15/20 files use numeric sub-steps for detailed work breakdown.

---

### Location/Room Grouping (Implicit Primary Structure)
**Pattern:** Primary items often group by location with secondary numbering reset
```
1. First Floor: (Installation Only)
   1. Lobby:
      1. One(1) unit Daikin...
   2. Room 1
      1. One(1) unit Daikin...
2. Second Floor: (Installation Only)
   1. Room 1:
      1. One(1) unit Daikin...
```

**Files using:**
- Kinton-Lodging-Inn-1 and Kinton-Lodging-Inn-2
- Jamari-Construction series (all use floor/room grouping)
- North + South Builders

**Frequency:** 8/20 files organize around locations, with numbering resets per location.

---

## Hierarchy & Structure

### Typical Depth: 3 Levels
**Level 1 (Primary):** Decimal numbering (1., 2., 3.) or location label
- Examples: "1. Nursing Station Hall", "1. First Floor", "1. One(1) Daikin Wall-mounted..."

**Level 2 (Secondary):** Sub-item detail (often unnumbered description + numeric sub-steps)
- Examples: "Installation Only", "Additional installation costs...", "1. General cleaning of the entire unit..."

**Level 3 (Tertiary):** Breakdown of work/materials
- Examples: "1. Pull down the AHU unit", "2. Supply welding gas", "3. Vacuuming"

### Indentation
- No explicit tab/space indentation in extracted text (line breaks used instead)
- Hierarchy implied by prefix numbering and context
- Location groupings appear at same level as items but control grouping visually

### Transition Markers
- Dashes (–) separate item description from pricing
- Equals (=) used for unit calculations: "₱600/unit = ₱29,400"
- "Plus:" used for additional charges: "Plus: Installation – ₱19,500"
- "Total Price –" marks section or final total

---

## Pricing Patterns

### Primary Pricing Format
**Rate × Unit Format:**
- Pattern: "₱[unit_price]/unit – ₱[total_price]" or "₱[unit_price]/unit = ₱[total_price]"
- Example: "₱600/unit – ₱29,400" (BC-1-5_15_2024)
- Example: "₱99,800/unit = ₱ 199,600" (Bible-Baptist-Church-1-12_4_2023)

**Frequency:** 12/20 files use unit-based pricing

### Lump Sum Pricing
**Pattern:** "– ₱[amount]" directly after item
- Example: "Total Price of the unit plus installation... – ₱ 51,500" (Homemaker-Furniture-1-10_26_2023)
- Example: "One(1) unit Daikin... – ₱8,500" (Kinton-Lodging-Inn-1)

**Frequency:** 8/20 files use direct lump-sum pricing

### Additive Pricing with "Plus:" or "Additional:"
**Pattern:** Main price + additional line items
- Example:
  ```
  – ₱143,100
  Plus: Installation – ₱19,500
  Total Price – ₱162,600
  ```
  (Homemaker-Furniture-2-8_22_2024)

**Example:**
  ```
  One(1) unit Daikin Wall Mounted Airconditioner 2hp (Inverter) at a maximum distance of 10ft only – ₱8,500
  Additional installation costs in excess of 10ft (₱350/ft)
  [calculation shown]
  Total Price – ₱ 13,250
  ```
  (Kinton-Lodging-Inn-1)

**Frequency:** 10/20 files use additional/excess-cost model

### Discount/Net Calculation
**Pattern:** "Less discount – ₱[amount]" followed by "Net Price = ₱[final]"
- Example:
  ```
  Total Price – ₱ 6,500
  Less discount – ₱ 550
  Net Price = ₱ 5,950
  ```
  (Crossworld-Cebu-1-8_5_2024)

**Frequency:** 1/20 files explicitly use discount notation

### Total Price Line Format
**Standard footer:** "Total Price – ₱ [amount]" or "Total Price = ₱ [amount]"
- Example: "Total Price – ₱ 58,400" (BC-1-5_15_2024)
- Example: "Total Price = ₱ 8,800" (Standard-Insurance-1-5_15_2025)
- Example: "Total Price of Items 1-5 = ₱ 72,250" (Jamari-Construction-1)
- Example: "Items 1, 2, and 3 Total Price – ₱ 35,900" (St. Mary Academy-6_24_2025)

**Frequency:** 20/20 files include "Total Price" line, using either dash (–) or equals (=)

---

## Special Cases & Anomalies

### Multi-Quote Alternatives
**Pattern:** Sequential items with "Alternative Offer" label
- Example (Homemaker-Furniture-2-8_22_2024):
  ```
  1. One(1) unit Daikin Floor-mounted Air Conditioner 6Hp-(3p) (Inverter) R32
  – ₱143,100
  Plus: Installation – ₱19,500
  Total Price – ₱162,600

  Alternative Offer
  2. One(1) unit Daikin Floor-mounted Air Conditioner 6Hp-(3p) (Non-Inverter) R410A
  – ₱99,700
  Plus: Installation – ₱19,500
  Total Price – ₱119,200
  ```

### Grouped Items with Per-Unit Pricing in Parentheses
**Pattern:** Multiple units with per-unit rate shown in calculation
- Example (Jamari-Construction-2):
  ```
  4. Ward 1
  Two(2) units of Wall-mounted Air Conditioner 2Hp (Inverter) at maximum distance of 10ft only – ₱8,000/unit = ₱16,000
  ```

### Complex Work Breakdowns (Repair/Service)
**Pattern:** Numbered sub-steps within single item, no unit pricing
- Example (Exquisite-Pawnshop-1-7_3_25):
  ```
  1. One(1) unit Media Wall-mounted Air conditioner (Inverter)
  1. Pull down the AHU unit
  2. Supply one(1) lot of welding gas, Silver rod
  3. Check the Leak portion
  4. Reweld the leak portion
  5. Vacuuming
  6. Reprocessing of the entire system
  7. Recharging of refrigerant
  8. Labor
  Total Price – ₱ 5,950
  ```

### Mixed Service and Equipment
**Pattern:** Combining product sale with installation/labor
- Example (Homemaker-Furniture-1-10_16_2025):
  ```
  1. Sales Division - One(1) Panasonic Air conditioner 2.5Hp
  1. General cleaning of the entire unit by supplying chemicals – ₱600
  ```
  (Note: Missing equipment price, cleaning price only)

### Calculation Breakdown (Distance-Based Charges)
**Pattern:** Base installation + excess distance surcharge shown inline
- Example (Jamari-Construction-1):
  ```
  One(1) unit Wall-mounted Air Conditioner 2Hp (Inverter) at maximum distance of 10ft only – ₱8,000
  Additional installation costs in excess of 10ft (₱350/ft)
  32 ft - 10 ft = 22 ft (excess) x (₱350/ft) = ₱7,700
  Total Price – ₱ 15,700
  ```

**Frequency:** 9/20 files use distance-based surcharge breakdowns

---

## Example Item Blocks (Raw Text)

### Example 1: Simple Multi-Unit Cleaning Service
**Source:** BC-1-5_15_2024
```
Job to be done :
General cleaning ONLY every Two(2) months for the FF Air conditioners
1. Forty-nine(49) units of Wall Mounted Air conditioners – ₱600/unit – ₱29,400
2. Sixty-eight(68) units of Window Air conditioners – ₱400/unit – ₱27,200
3. Two(2) units of Floor Mounted Air conditioners – ₱900/unit – ₱1,800
Total Price – ₱ 58,400
```

### Example 2: Hierarchical Location Grouping with Distance-Based Pricing
**Source:** Jamari-Construction-1
```
Job to be done :
5th Floor - Installation Only (Daikin | Matrix) Brand
1. Nursing Station Hall
One(1) unit Wall-mounted Air Conditioner 2Hp (Inverter) at maximum distance of 10ft only
– ₱8,000
Additional installation costs in excess of 10ft (₱350/ft)
32 ft - 10 ft = 22 ft (excess) x (₱350/ft) = ₱7,700
Total Price – ₱ 15,700
2. Supervisor Room
One(1) unit Wall-mounted Air Conditioner 1Hp (Inverter) at maximum distance of 10ft only
– ₱7,500
Additional installation costs in excess of 10ft (₱350/ft)
15 ft - 10 ft = 5 ft (excess) x (₱350/ft) = ₱1,750
Total Price – ₱ 9,250
...
Total Price of Items 1-5 = ₱ 72,250
```

### Example 3: Detailed Sub-Steps for Repair Work
**Source:** St. Mary Academy-1-6_24_2025
```
Job to be done:
1. DEPT - AVR Room
(1) Two(2) Koppel Ceiling-mounted Air conditioner 3Trs (Non-Inverter)
1. General cleaning of the entire unit by supplying chemicals
2. Pull down AHU units
3. Supply Two(2) pcs. Universal Remote Control
4. Reprocessing of the entire system
5. Supply one(1) lot of welding gas, Silver rod
6. Vacuuming
7. Recharging of refrigerant
8. Labor Total Price – ₱ 10,500/unit = ₱ 21,000
```

### Example 4: Alternative Offerings with Equipment Pricing
**Source:** Homemaker-Furniture-2-8_22_2024
```
Job to be done :
1. One(1) unit Daikin Floor-mounted Air Conditioner 6Hp-(3p) (Inverter) R32
– ₱ 143,100
Plus: Installation – ₱ 19,500
Total Price – ₱ 162,600
Alternative Offer
2. One(1) unit Daikin Floor-mounted Air Conditioner 6Hp-(3p) (Non-Inverter) R410A
– ₱ 99,700
Plus: Installation – ₱ 19,500
Total Price – ₱ 119,200
```

### Example 5: Complex Nested Location and Sub-Item Structure
**Source:** Kinton-Lodging-Inn-1
```
Job to be done :
1. First Floor: (Installation Only)
1. Lobby:
1. One(1) unit Daikin Wall Mounted Airconditioner 2hp (Inverter) at a maximum
distance of 10ft only – ₱8,500
2. Room 1
1. One(1) unit Daikin Wall Mounted Airconditioner 1 ½ hp (Inverter) at a maximum
distance of 10ft only – ₱8,000
Additional installation costs in excess of 10ft (₱350/ft)
25ft - 10ft - 15ft (excess) x (₱350/ft) = ₱5,250
Total Price – ₱ 13,250
2. Second Floor: (Installation Only)
1. Room 1:
1. One(1) unit Daikin Wall Mounted Airconditioner 1.5hp at a maximum distance of 10ft
only – ₱8,000
Additional installation costs in excess of 10ft (₱350/ft)
40ft - 10ft - 30ft (excess) x (₱350/ft) = ₱10,500
Total Price – ₱ 18,500
Total Price of First floor + Second Floor = ₱ 84,250
```

---

## Summary Statistics

| Pattern | Count | Percentage |
|---------|-------|-----------|
| Primary decimal (1., 2., 3.) | 18 | 90% |
| Secondary alphabetic (a., b.) | 2 | 10% |
| Numeric sub-steps (1), (2) | 15 | 75% |
| Location grouping | 8 | 40% |
| Unit-based pricing (X/unit = Y) | 12 | 60% |
| Distance-based surcharges | 9 | 45% |
| Lump-sum pricing | 8 | 40% |
| Plus/Additional pricing | 10 | 50% |
| Alternative offers | 1 | 5% |
| Discount notation | 1 | 5% |

---

**Analysis completed:** 20 files sampled across diverse clients (University, Insurance, Furniture, Construction, Church, Pawnshop, Lodging).

**Key Takeaway:** The standard quotation format prioritizes clarity through decimal numbering at primary level, flexible secondary structure (alphabetic or numeric sub-items), distance-based surcharge calculations, and consistent "Total Price" footer. Pricing formats vary but all maintain unit breakdowns or lump-sum amounts with supporting calculations.
