"""
Data cleaning for Kenya water quality analysis.
Audits missing values, drops unusable indicators, and produces a clean dataset.
"""

import pandas as pd
import numpy as np
import os

os.makedirs("data/processed", exist_ok=True)

# ============================================================
# 1. LOAD RAW DATA
# ============================================================
print("=" * 60)
print("STEP 1: Loading raw data")
print("=" * 60)

raw = pd.read_csv("data/processed/kenya_water_master.csv")
print(f"Loaded {len(raw)} rows from master file")

# ============================================================
# 2. AUDIT MISSING DATA BY INDICATOR
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Auditing coverage per indicator")
print("=" * 60)

audit = raw.groupby(["source", "indicator_code", "indicator_name"]).agg(
    n_years=("year", "nunique"),
    first_year=("year", "min"),
    last_year=("year", "max"),
    n_rows=("value", "count"),
).reset_index()

audit["coverage_pct"] = (audit["n_years"] / 25 * 100).round(1)

print("\nCoverage audit:")
print(audit.to_string(index=False))

# ============================================================
# 3. DECIDE WHICH INDICATORS TO KEEP
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Filtering indicators")
print("=" * 60)

# Rule: keep indicators with at least 15 years of data (60% coverage)
MIN_YEARS = 15

keep_codes = audit[audit["n_years"] >= MIN_YEARS]["indicator_code"].tolist()
drop_codes = audit[audit["n_years"] < MIN_YEARS]["indicator_code"].tolist()

print(f"\n✅ KEEPING ({len(keep_codes)} indicators with ≥ {MIN_YEARS} years):")
for code in keep_codes:
    name = audit[audit["indicator_code"] == code]["indicator_name"].iloc[0]
    n = audit[audit["indicator_code"] == code]["n_years"].iloc[0]
    print(f"   {code} ({name}): {n} years")

print(f"\n❌ DROPPING ({len(drop_codes)} indicators with < {MIN_YEARS} years):")
for code in drop_codes:
    name = audit[audit["indicator_code"] == code]["indicator_name"].iloc[0]
    n = audit[audit["indicator_code"] == code]["n_years"].iloc[0]
    print(f"   {code} ({name}): only {n} year(s)")

# ============================================================
# 4. DEDUPLICATE WHO ROWS
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Removing WHO duplicates")
print("=" * 60)

# The WHO data has 3 values per year (urban/rural/total) but all labeled "National"
# We'll drop WHO entirely to avoid confusion, keeping World Bank which is clean.
before = len(raw)
clean = raw[raw["source"] == "world_bank"].copy()
print(f"Dropped {before - len(clean)} WHO rows (3 values per year, unlabeled)")

# ============================================================
# 5. FILTER TO KEPT INDICATORS
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Filtering to kept indicators")
print("=" * 60)

before = len(clean)
clean = clean[clean["indicator_code"].isin(keep_codes)].copy()
print(f"Dropped {before - len(clean)} rows from sparse indicators")

# ============================================================
# 6. STANDARDIZE VALUES
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: Standardizing values")
print("=" * 60)

# Round to 2 decimal places
clean["value"] = clean["value"].round(2)

# Ensure year is integer
clean["year"] = clean["year"].astype(int)

# Drop any remaining NaN values (should be none)
before = len(clean)
clean = clean.dropna(subset=["value"])
print(f"Dropped {before - len(clean)} rows with NaN values")

# Sort for readability
clean = clean.sort_values(["indicator_name", "year"]).reset_index(drop=True)

# ============================================================
# 7. CHECK FOR GAPS IN KEPT INDICATORS
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: Checking for gaps in kept indicators")
print("=" * 60)

for code in clean["indicator_code"].unique():
    subset = clean[clean["indicator_code"] == code]
    years = sorted(subset["year"].unique())
    full_range = set(range(min(years), max(years) + 1))
    missing = sorted(full_range - set(years))

    if missing:
        name = subset["indicator_name"].iloc[0]
        print(f"⚠️  {name}: missing years {missing}")
    else:
        print(f"✅ {name}: complete {min(years)}–{max(years)}")

# ============================================================
# 8. SAVE CLEAN DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: Saving cleaned data")
print("=" * 60)

clean.to_csv("data/processed/kenya_water_clean.csv", index=False)
print(f"✅ Saved {len(clean)} rows to data/processed/kenya_water_clean.csv")

# Save the audit report for the README's limitations section
audit.to_csv("data/processed/coverage_audit.csv", index=False)
print(f"✅ Saved coverage audit to data/processed/coverage_audit.csv")

# ============================================================
# 9. FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"Indicators kept:    {clean['indicator_code'].nunique()}")
print(f"Total records:      {len(clean)}")
print(f"Years covered:      {clean['year'].min()} – {clean['year'].max()}")
print(f"\nBreakdown:")
for code in clean["indicator_code"].unique():
    subset = clean[clean["indicator_code"] == code]
    print(f"  {subset['indicator_name'].iloc[0]}: {len(subset)} rows")