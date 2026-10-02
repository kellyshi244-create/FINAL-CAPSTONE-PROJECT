"""
Loads Kenya water quality CSVs into MySQL.
Run once to populate the database.
"""

import pandas as pd
from sqlalchemy import create_engine, text

# ============================================================
# UPDATE THESE WITH YOUR MYSQL CREDENTIALS
# ============================================================
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password_here"
MYSQL_HOST = "localhost"          # or cloud host
MYSQL_PORT = 3306
MYSQL_DATABASE = "kenya_water"

# ============================================================
# 1. Connect to MySQL (create DB if it doesn't exist)
# ============================================================
# First connect without specifying a database
base_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"

try:
    base_engine = create_engine(base_url)
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
        conn.commit()
    print(f"✅ Database '{MYSQL_DATABASE}' ready")
except Exception as e:
    print(f"❌ Could not connect to MySQL: {e}")
    print("   Check your username, password, host, and port.")
    raise

# Now connect to that database
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ============================================================
# 2. Load each CSV into its own table
# ============================================================

tables = {
    "national_indicators": "data/processed/kenya_water_clean.csv",
    "athi_river_coverage": "data/raw/fixed/athi_river_coverage.csv",
    "kewi_water_tests":    "data/raw/fixed/kewi_water_tests.csv",
}

for table_name, csv_path in tables.items():
    try:
        df = pd.read_csv(csv_path)

        # Clean column names for MySQL (no spaces, no special chars)
        df.columns = [
            c.strip().replace(" ", "_").replace("%", "pct")
             .replace("(", "").replace(")", "").replace("/", "_")
            for c in df.columns
        ]

        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"✅ {table_name}: {len(df)} rows loaded")
    except FileNotFoundError:
        print(f"⚠️  {table_name}: file not found at {csv_path} (skipping)")
    except Exception as e:
        print(f"❌ {table_name}: {e}")

# ============================================================
# 3. Verify
# ============================================================
with engine.connect() as conn:
    result = conn.execute(text("SHOW TABLES"))
    print("\n📊 Tables in MySQL:")
    for row in result:
        table = row[0]
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
        print(f"   {table}: {count} rows")

print(f"\n✅ All data loaded into MySQL database: {MYSQL_DATABASE}")