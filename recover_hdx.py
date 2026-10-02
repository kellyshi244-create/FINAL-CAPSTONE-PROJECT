"""
Recovers HDX files that failed due to encoding/delimiter issues.
"""
import pandas as pd
import os

os.makedirs("data/raw/fixed", exist_ok=True)

# --- File 1: Athi River coverage (already readable) ---
try:
    df = pd.read_csv("data/raw/hdx_0_Water_Sanitation_Coverage_of_the_Athi_Ri.csv")
    df.to_csv("data/raw/fixed/athi_river_coverage.csv", index=False)
    print(f"✅ Athi River: {len(df)} rows, columns = {list(df.columns)}")
    print(df.head(3).to_string())
except Exception as e:
    print(f"❌ Athi River: {e}")

print()

# --- File 2: KEWI water test results (the important one) ---
try:
    # Try multiple delimiters and encodings
    attempts = [
        {"sep": ",", "encoding": "latin-1", "on_bad_lines": "skip"},
        {"sep": "\t", "encoding": "latin-1", "on_bad_lines": "skip"},
        {"sep": None, "engine": "python", "encoding": "latin-1", "on_bad_lines": "skip"},
        {"sep": ";", "encoding": "latin-1", "on_bad_lines": "skip"},
    ]
    for i, kwargs in enumerate(attempts):
        try:
            df = pd.read_csv("data/raw/hdx_2_KEWI_water_test_and_results.csv.csv", **kwargs)
            if len(df.columns) > 1:
                df.to_csv("data/raw/fixed/kewi_water_tests.csv", index=False)
                print(f"✅ KEWI (attempt {i+1}): {len(df)} rows, columns = {list(df.columns)[:8]}")
                print(df.head(3).to_string())
                break
        except Exception:
            continue
except Exception as e:
    print(f"❌ KEWI: {e}")

print()

# --- File 3: Indicators.xlsx.csv ---
try:
    df = pd.read_csv("data/raw/hdx_1_Indicators.xlsx.csv", encoding="latin-1", on_bad_lines="skip")
    df.to_csv("data/raw/fixed/indicators.csv", index=False)
    print(f"✅ Indicators: {len(df)} rows, columns = {list(df.columns)[:8]}")
    print(df.head(2).to_string())
except Exception as e:
    print(f"❌ Indicators: {e}")

print()

# --- File 4 & 5: Performance and Ranking ---
for src, dst in [
    ("hdx_3_Overall_Performance_of_the_Water_Service.csv", "water_service_performance.csv"),
    ("hdx_4_Overall_Ranking_and_Ranking_by_Category_.csv", "ranking_by_category.csv"),
]:
    try:
        df = pd.read_csv(f"data/raw/{src}", encoding="latin-1", on_bad_lines="skip")
        df.to_csv(f"data/raw/fixed/{dst}", index=False)
        print(f"✅ {dst}: {len(df)} rows, columns = {list(df.columns)[:8]}")
    except Exception as e:
        print(f"❌ {src}: {e}")