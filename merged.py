import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("data/processed/kenya_water.db")

# --- Table 1: National indicators (clean World Bank data) ---
master = pd.read_csv("data/processed/kenya_water_master.csv")
national = master[master["source"] == "world_bank"].copy()
national["value"] = national["value"].round(2)
national.to_sql("national_indicators", conn, if_exists="replace", index=False)
print(f"✅ national_indicators: {len(national)} rows")

# --- Table 2: Athi River coverage ---
if os.path.exists("data/raw/fixed/athi_river_coverage.csv"):
    athi = pd.read_csv("data/raw/fixed/athi_river_coverage.csv")
    athi.to_sql("athi_river_coverage", conn, if_exists="replace", index=False)
    print(f"✅ athi_river_coverage: {len(athi)} rows, columns = {list(athi.columns)}")

# --- Table 3: KEWI water tests (if recoverable) ---
if os.path.exists("data/raw/fixed/kewi_water_tests.csv"):
    kewi = pd.read_csv("data/raw/fixed/kewi_water_tests.csv")
    kewi.to_sql("kewi_water_tests", conn, if_exists="replace", index=False)
    print(f"✅ kewi_water_tests: {len(kewi)} rows, columns = {list(kewi.columns)}")

# --- Verify all tables ---
print("\n📊 Tables in database:")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for (name,) in cursor.fetchall():
    cursor.execute(f"SELECT COUNT(*) FROM {name}")
    count = cursor.fetchone()[0]
    print(f"   {name}: {count} rows")

conn.close()
print("\n✅ Database ready: data/processed/kenya_water.db")