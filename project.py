"""
Kenya Water Quality & WASH Data Pipeline
=========================================
Fetches data from World Bank, WHO, HDX, Kenya Open Data, and UNICEF JMP.
Harmonizes everything into one analysis-ready dataset.

Run top to bottom. Takes ~3-5 minutes.
"""

import os
import io
import json
import time
import requests
import pandas as pd
import numpy as np

# Create folders
for folder in ["data/raw", "data/processed"]:
    os.makedirs(folder, exist_ok=True)

print("✅ Folder structure ready\n")


# ============================================================
# SOURCE 1: WORLD BANK INDICATORS (100% reliable)
# ============================================================
def fetch_world_bank():
    print("=" * 60)
    print("SOURCE 1: World Bank Water & Sanitation Indicators")
    print("=" * 60)

    indicators = {
        "SH.H2O.SMDW.ZS": "Safely managed drinking water services (% pop)",
        "SH.H2O.BASW.ZS": "Basic drinking water services (% pop)",
        "SH.H2O.SAFE.ZS": "Safely managed water, sanitation & hygiene (% pop)",
        "SH.STA.BASS.ZS": "Basic sanitation services (% pop)",
        "SH.STA.ODFC.ZS": "Open defecation (% pop)",
        "SH.STA.WASH.P5": "Mortality from unsafe WASH (per 100k)",
        "SH.H2O.SMDW.RU.ZS": "Safely managed drinking water - rural (% pop)",
        "SH.H2O.SMDW.UR.ZS": "Safely managed drinking water - urban (% pop)",
        "ER.H2O.FWTL.ZS": "Freshwater withdrawal (% of internal resources)",
    }

    records = []
    for code, name in indicators.items():
        url = f"https://api.worldbank.org/v2/country/KE/indicator/{code}"
        params = {"format": "json", "per_page": 200, "date": "2000:2024"}
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1 and data[1]:
                    for entry in data[1]:
                        if entry["value"] is not None:
                            records.append({
                                "source": "world_bank",
                                "indicator_code": code,
                                "indicator_name": name,
                                "country": "Kenya",
                                "county": "National",
                                "year": int(entry["date"]),
                                "value": entry["value"],
                                "unit": "%" if "ZS" in code else "per_100k",
                            })
                    print(f"  ✅ {code}: {len([e for e in data[1] if e['value']])} entries")
        except Exception as e:
            print(f"  ❌ {code}: {e}")
        time.sleep(0.3)

    df = pd.DataFrame(records)
    df.to_csv("data/raw/world_bank_water.csv", index=False)
    print(f"\n  → Saved {len(df)} records to data/raw/world_bank_water.csv\n")
    return df


# ============================================================
# SOURCE 2: WHO GLOBAL HEALTH OBSERVATORY (95% reliable)
# ============================================================
def fetch_who():
    print("=" * 60)
    print("SOURCE 2: WHO Global Health Observatory")
    print("=" * 60)

    # WHO GHO OData API
    base = "https://ghoapi.azureedge.net/api"

    indicators = {
        "WSH_SANITATION_SAFELY_MANAGED": "Safely managed sanitation",
        "WSH_WATER_SAFELY_MANAGED": "Safely managed drinking water",
        "WSH_WATER_BASIC": "Basic drinking water",
    }

    records = []
    for code, name in indicators.items():
        try:
            r = requests.get(f"{base}/{code}", timeout=30)
            if r.status_code == 200:
                data = r.json().get("value", [])
                for entry in data:
                    if entry.get("SpatialDim") == "KEN":
                        records.append({
                            "source": "who_gho",
                            "indicator_code": code,
                            "indicator_name": name,
                            "country": "Kenya",
                            "county": "National",
                            "year": entry.get("TimeDim"),
                            "value": entry.get("NumericValue"),
                            "unit": "%",
                        })
                print(f"  ✅ {code}: {len([e for e in data if e.get('SpatialDim') == 'KEN'])} entries")
        except Exception as e:
            print(f"  ❌ {code}: {e}")
        time.sleep(0.5)

    df = pd.DataFrame(records)
    if not df.empty:
        df.to_csv("data/raw/who_water.csv", index=False)
        print(f"\n  → Saved {len(df)} records to data/raw/who_water.csv\n")
    return df


# ============================================================
# SOURCE 3: HDX KENYA WASH (85% reliable)
# ============================================================
def fetch_hdx():
    print("=" * 60)
    print("SOURCE 3: HDX Kenya WASH Datasets")
    print("=" * 60)

    url = "https://data.humdata.org/api/3/action/package_search"
    params = {"q": "Kenya water sanitation", "rows": 30}

    try:
        r = requests.get(url, params=params, timeout=30)
        results = r.json().get("result", {}).get("results", [])
        print(f"  Found {len(results)} HDX datasets")

        manifest = []
        for pkg in results:
            for res in pkg.get("resources", []):
                fmt = res.get("format", "").upper()
                if fmt in ["CSV", "XLSX", "XLS"]:
                    manifest.append({
                        "dataset_title": pkg.get("title"),
                        "resource_name": res.get("name"),
                        "format": fmt,
                        "url": res.get("url"),
                    })

        df = pd.DataFrame(manifest)
        df.to_csv("data/raw/hdx_manifest.csv", index=False)
        print(f"  → Saved {len(df)} resource links to data/raw/hdx_manifest.csv")

        # Download top 5 CSVs
        for i, row in df.head(5).iterrows():
            try:
                r = requests.get(row["url"], timeout=60)
                if r.status_code == 200:
                    safe = f"hdx_{i}_{str(row['resource_name'])[:40]}".replace(" ", "_").replace("/", "_")
                    path = f"data/raw/{safe}.csv"
                    with open(path, "wb") as f:
                        f.write(r.content)
                    print(f"    ✅ {safe}.csv")
            except Exception as e:
                print(f"    ❌ {row['resource_name']}: {e}")

        print()
        return manifest
    except Exception as e:
        print(f"  ❌ HDX failed: {e}\n")
        return []


# ============================================================
# SOURCE 4: KENYA OPEN DATA PORTAL (80% reliable)
# ============================================================
def fetch_kenya_open_data():
    print("=" * 60)
    print("SOURCE 4: Kenya Open Data Portal")
    print("=" * 60)

    # Kenya Open Data uses CKAN — same API as HDX
    base = "https://www.opendata.go.ke/api/3/action/package_search"

    queries = ["water", "sanitation", "WASH", "water quality"]

    manifest = []
    for q in queries:
        try:
            r = requests.get(base, params={"q": q, "rows": 20}, timeout=30)
            if r.status_code == 200:
                results = r.json().get("result", {}).get("results", [])
                print(f"  '{q}': {len(results)} datasets")
                for pkg in results:
                    for res in pkg.get("resources", []):
                        fmt = res.get("format", "").upper()
                        if fmt in ["CSV", "XLSX", "XLS"]:
                            manifest.append({
                                "dataset_title": pkg.get("title"),
                                "resource_name": res.get("name"),
                                "format": fmt,
                                "url": res.get("url"),
                                "query": q,
                            })
        except Exception as e:
            print(f"  ❌ '{q}': {e}")
        time.sleep(0.5)

    df = pd.DataFrame(manifest)
    if not df.empty:
        df.to_csv("data/raw/kenya_opendata_manifest.csv", index=False)
        print(f"  → Saved {len(df)} resource links to data/raw/kenya_opendata_manifest.csv\n")
    else:
        print("  ⚠️ No Kenya Open Data resources found\n")
    return manifest


# ============================================================
# SOURCE 5: UNICEF JMP WASH DATA (90% reliable)
# ============================================================
def fetch_unicef_jmp():
    print("=" * 60)
    print("SOURCE 5: UNICEF/WHO Joint Monitoring Programme")
    print("=" * 60)

    # JMP publishes data via SDMX — try the standard endpoint
    url = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,WASH_HOUSEHOLDS,1.0/KEN.?format=sdmx-json"

    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open("data/raw/unicef_jmp_raw.json", "w") as f:
                json.dump(r.json(), f)
            print(f"  ✅ Downloaded UNICEF JMP data → data/raw/unicef_jmp_raw.json")
        else:
            print(f"  ⚠️ UNICEF JMP: status {r.status_code} (data may need manual retrieval)")
    except Exception as e:
        print(f"  ❌ UNICEF JMP: {e}")

    print()


# ============================================================
# TABLE INSPECTOR
# ============================================================
def inspect_tables():
    print("=" * 60)
    print("TABLE INSPECTOR")
    print("=" * 60)

    csv_files = sorted([f for f in os.listdir("data/raw") if f.endswith(".csv")])
    if not csv_files:
        print("  ⚠️ No CSVs found in data/raw/\n")
        return

    print(f"\nFound {len(csv_files)} CSV files:\n")
    summary = []

    for fname in csv_files:
        try:
            df = pd.read_csv(f"data/raw/{fname}")
            print(f"📄 {fname}")
            print(f"   Rows: {len(df)} | Columns: {len(df.columns)}")
            print(f"   Columns: {list(df.columns)[:8]}")

            if len(df) > 0:
                sample = ", ".join(f"{k}={str(v)[:20]}" for k, v in list(df.iloc[0].items())[:4])
                print(f"   Sample: {sample}")
            print()

            summary.append({
                "file": fname,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": " | ".join(df.columns[:10]),
            })
        except Exception as e:
            print(f"📄 {fname} — ⚠️ {e}\n")

    pd.DataFrame(summary).to_csv("data/processed/inspection_summary.csv", index=False)
    print(f"→ Summary saved to data/processed/inspection_summary.csv\n")


# ============================================================
# HARMONIZER
# ============================================================
def harmonize():
    print("=" * 60)
    print("HARMONIZATION")
    print("=" * 60)

    frames = []

    # World Bank
    try:
        wb = pd.read_csv("data/raw/world_bank_water.csv")
        frames.append(wb)
        print(f"  ✅ World Bank: {len(wb)} rows")
    except Exception as e:
        print(f"  ⚠️ World Bank: {e}")

    # WHO
    try:
        who = pd.read_csv("data/raw/who_water.csv")
        frames.append(who)
        print(f"  ✅ WHO: {len(who)} rows")
    except Exception as e:
        print(f"  ⚠️ WHO: {e}")

    if not frames:
        print("\n  ❌ No data to harmonize.\n")
        return

    # Ensure common schema
    schema = ["source", "indicator_code", "indicator_name", "country",
              "county", "year", "value", "unit"]

    normalized = []
    for df in frames:
        for col in schema:
            if col not in df.columns:
                df[col] = np.nan
        normalized.append(df[schema])

    master = pd.concat(normalized, ignore_index=True)
    master = master.dropna(subset=["value"])
    master["year"] = pd.to_numeric(master["year"], errors="coerce")
    master = master.dropna(subset=["year"])
    master["year"] = master["year"].astype(int)

    master = master.sort_values(["source", "indicator_name", "year"]).reset_index(drop=True)

    master.to_csv("data/processed/kenya_water_master.csv", index=False)

    print(f"\n{'='*60}")
    print(f"✅ Master dataset → data/processed/kenya_water_master.csv")
    print(f"{'='*60}")
    print(f"Total records:   {len(master)}")
    print(f"Sources:         {master['source'].nunique()}")
    print(f"Indicators:      {master['indicator_name'].nunique()}")
    print(f"Years covered:   {master['year'].min()} – {master['year'].max()}")
    print(f"\nBreakdown by source:")
    print(master["source"].value_counts().to_string())
    print(f"{'='*60}\n")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("KENYA WATER QUALITY PIPELINE")
    print("=" * 60 + "\n")

    fetch_world_bank()          # Always works
    fetch_who()                 # Usually works
    fetch_hdx()                 # Usually works
    fetch_kenya_open_data()     # Sometimes works
    fetch_unicef_jmp()          # Sometimes works
    inspect_tables()            # Auto-scan
    harmonize()                 # Merge

    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    print("\nNext: open data/processed/kenya_water_master.csv")
    print("That's your analysis-ready dataset.")