"""
clean_and_load.py
=================
All-in-one pipeline:
  1. Clean national indicators (drop sparse, remove WHO duplicates)
  2. Clean Athi River coverage table
  3. Inspect and clean KEWI water tests table
  4. Reload all three clean tables into MySQL

Run: python clean_and_load.py
"""

import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine, text

# ============================================================
# CONFIG — UPDATE THESE WITH YOUR MYSQL CREDENTIALS
# ============================================================
MYSQL_USER     = "root"
MYSQL_PASSWORD = "your_password_here"
MYSQL_HOST     = "localhost"      # or cloud host
MYSQL_PORT     = 3306
MYSQL_DATABASE = "kenya_water"


# ============================================================
# HELPERS
# ============================================================
def header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def audit_nulls(df, name):
    print(f"\nNull counts in {name}:")
    nulls = df.isnull().sum()
    found = False
    for col, count in nulls.items():
        if count > 0:
            pct = count / len(df) * 100
            print(f"   {col}: {count} nulls ({pct:.1f}%)")
            found = True
    if not found:
        print("   ✅ No nulls found")


def clean_column_names(df):
    """Convert column names to MySQL-friendly snake_case."""
    df.columns = [
        str(c).strip()
        .replace(" ", "_")
        .replace("%", "pct")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace("-", "_")
        for c in df.columns
    ]
    return df


# ============================================================
# PART 1: CLEAN NATIONAL INDICATORS
# ============================================================
def clean_national():
    header("PART 1: CLEANING NATIONAL INDICATORS")

    raw = pd.read_csv("data/processed/kenya_water_master.csv")
    print(f"Loaded {len(raw)} rows")

    audit = raw.groupby(["source", "indicator_code", "indicator_name"]).agg(
        n_years=("year", "nunique"),
        first_year=("year", "min"),
        last_year=("year", "max"),
    ).reset_index()

    print("\nCoverage audit:")
    print(audit.to_string(index=False))

    MIN_YEARS = 15
    keep = audit[audit["n_years"] >= MIN_YEARS]["indicator_code"].tolist()
    drop = audit[audit["n_years"] < MIN_YEARS]["indicator_code"].tolist()

    print(f"\n✅ Keeping {len(keep)} indicators: {keep}")
    print(f"❌ Dropping {len(drop)} indicators: {drop}")

    # Keep only World Bank (WHO has 3 unlabeled values per year)
    clean = raw[raw["source"] == "world_bank"].copy()
    clean = clean[clean["indicator_code"].isin(keep)]
    clean = clean.dropna(subset=["value"])
    clean["value"] = clean["value"].round(2)
    clean["year"] = clean["year"].astype(int)
    clean = clean.sort_values(["indicator_name", "year"]).reset_index(drop=True)

    clean.to_csv("data/processed/kenya_water_clean.csv", index=False)
    audit.to_csv("data/processed/coverage_audit.csv", index=False)

    print(f"\n✅ Saved {len(clean)} rows → data/processed/kenya_water_clean.csv")
    return clean


# ============================================================
# PART 2: CLEAN ATHI RIVER
# ============================================================
def clean_athi():
    header("PART 2: CLEANING ATHI RIVER TABLE")

    try:
        df = pd.read_csv("data/raw/fixed/athi_river_coverage.csv")
    except FileNotFoundError:
        print("⚠️ Athi file not found — skipping")
        return None

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    audit_nulls(df, "Athi River")

    df = clean_column_names(df)

    # Drop rows missing critical fields
    critical = [c for c in ["Type_of_Coverage", "Served_Pop"] if c in df.columns]
    if critical:
        before = len(df)
        df = df.dropna(subset=critical)
        print(f"\nDropped {before - len(df)} rows missing critical fields")

    # Coerce numeric columns
    for col in df.columns:
        if any(k in col.lower() for k in ["pop", "pct", "coverage", "growth"]):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.to_csv("data/processed/athi_clean.csv", index=False)
    print(f"\n✅ Saved {len(df)} rows → data/processed/athi_clean.csv")
    return df


# ============================================================
# PART 3: INSPECT + CLEAN KEWI (adaptive)
# ============================================================
def clean_kewi():
    header("PART 3: INSPECTING & CLEANING KEWI")

    try:
        df = pd.read_csv("data/raw/fixed/kewi_water_tests.csv")
    except FileNotFoundError:
        print("⚠️ KEWI file not found — skipping")
        return None

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    audit_nulls(df, "KEWI")

    print(f"\nFirst 5 rows:")
    print(df.head().to_string())

    print(f"\nColumn value diversity:")
    for col in df.columns:
        n_unique = df[col].nunique()
        samples = list(df[col].dropna().unique()[:5])
        print(f"   {col}: {n_unique} unique | samples: {samples}")

    df = clean_column_names(df)

    # Drop fully-empty rows
    before = len(df)
    df = df.dropna(how="all")
    print(f"\nDropped {before - len(df)} fully-empty rows")

    # Drop rows missing the result value
    result_cols = [
        c for c in df.columns
        if any(k in c.lower() for k in ["result", "value", "measurement", "concentration"])
    ]
    if result_cols:
        before = len(df)
        df = df.dropna(subset=result_cols[:1])
        print(f"Dropped {before - len(df)} rows missing result values (column: {result_cols[0]})")
    else:
        print("⚠️ Could not identify a 'result' column — no rows dropped")

    # Strip whitespace in text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    df.to_csv("data/processed/kewi_clean.csv", index=False)
    print(f"\n✅ Saved {len(df)} rows → data/processed/kewi_clean.csv")
    return df


# ============================================================
# PART 4: RELOAD ALL THREE INTO MYSQL
# ============================================================
def load_to_mysql():
    header("PART 4: RELOADING MYSQL")

    base_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"

    try:
        base_engine = create_engine(base_url)
        with base_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
            conn.commit()
        print(f"✅ Database '{MYSQL_DATABASE}' ready")
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("   Check your credentials at the top of this script.")
        return

    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    tables = {
        "national_indicators": "data/processed/kenya_water_clean.csv",
        "athi_river_coverage": "data/processed/athi_clean.csv",
        "kewi_water_tests":    "data/processed/kewi_clean.csv",
    }

    for name, path in tables.items():
        if not os.path.exists(path):
            print(f"⚠️  {name}: {path} not found — skipping")
            continue
        try:
            df = pd.read_csv(path)
            df.to_sql(name, engine, if_exists="replace", index=False)
            print(f"✅ {name}: {len(df)} rows loaded")
        except Exception as e:
            print(f"❌ {name}: {e}")

    print("\nVerification:")
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        for row in result:
            table = row[0]
            count = conn.execute(text(f"SELECT COUNT(*) FROM `{table}`")).fetchone()[0]
            print(f"   {table}: {count} rows")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("COMPLETE CLEAN & LOAD PIPELINE")
    print("=" * 60)

    clean_national()
    clean_athi()
    clean_kewi()
    load_to_mysql()

    print("\n" + "=" * 60)
    print("✅ DONE")
    print("=" * 60)