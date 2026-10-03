# 💧 Kenya Water Quality Analysis (2000–2024)

A data analysis project on Kenya's water access, sanitation coverage, and water quality, using World Bank, HDX, and KEWI data.

---

## 📖 Project Overview

This project examines Kenya's water sector through :

1. **National access trends** — how water and sanitation access changed from 2000 to 2024
2. **Regional case study** — how the Athi River basin performed from 2011 to 2014
3. **Water quality** — chemical analysis of 493 water samples from Kenyan counties

The main finding: **access is improving, but quality is not guaranteed.**



---

## ❗ Problem Statement

Kenya has made progress on water access — from 45% in 2000 to 65.6% in 2024. But three problems remain:

1. **Progress is too slow.** Kenya adds about 0.85 percentage points per year. At this rate, universal access would take another 40 years — but the SDG 6 deadline is 2030.

2. **Sanitation lags far behind water.** Only 40.9% of Kenyans have basic sanitation, compared to 65.6% for water — a 25-point gap that has not narrowed in 24 years.

3. **Water quality is unverified.** Some water samples show pH as low as 5.58, below the KEBS safe minimum of 6.5. Being counted as "having access" does not mean the water is safe.


---

## 🎯 Objectives

**General:** To analyze Kenya's water access and quality using national, regional, and laboratory data, producing insights for policy and planning.

**Specific:**
1. Quantify 25 years of national progress in water and sanitation access
2. Assess freshwater resource pressure
3. Evaluate water quality across counties using pH, conductivity, and TDS
4. Compare results against KEBS and WHO drinking water standards
5. Examine the Athi River basin as a regional case study

---

## ❓ Research Questions

1. How has Kenya's water and sanitation access changed between 2000 and 2024?
2. Is the gap between water and sanitation access narrowing?
3. Is Kenya's freshwater withdrawal approaching water stress levels?
4. What is the average pH of water across Kenyan counties?
5. How does water quality vary by source type (borehole, rain, effluent)?
6. How has coverage progressed in the Athi River basin?
7. Do conductivity levels exceed the KEBS limit of 1500 µS/cm?

---

## 📊 Data Sources

| Source | What It Provides | Coverage | Contribution |
|---|---|---|---|
| **World Bank Open Data** | National water, sanitation, and freshwater indicators | 2000–2024 | National baseline trends |
| **HDX (UN OCHA)** | Athi River basin coverage (population, served, unserved) | 2011–2014 | Regional case study |
| **Kenya Water Institute (KEWI)** | 493 water sample lab tests (pH, conductivity, TDS) | 2011–2012 | Water quality analysis |

The three datasets cannot be merged into one table because they have different grains (national vs. regional vs. per-sample). They are analyzed separately and combined in the final conclusions.

---

## 🛠️ Technology Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Data processing and analysis |
| **pandas / numpy** | Data cleaning and transformation |
| **SQLite** | Database storage |
| **matplotlib / seaborn** | Chart generation |
| **Streamlit** | Interactive web application |
| **Git & GitHub** | Version control and hosting |

---

## 🔬 Methodology

**Phase 1 — Data Collection**
- Pulled data from World Bank API, HDX, and KEWI sources

**Phase 2 — Cleaning**
- Standardized column names
- Converted text numbers to numeric (e.g., `"67%"` → `67.0`)
- Kept numeric nulls as-is (they mean "test not performed")

**Phase 3 — Storage**
- Loaded all three datasets into `kenya_water.db` (SQLite)

**Phase 4 — Analysis**
- Queried the database for averages by county, source, and year
- Compared results against KEBS and WHO limits

**Phase 5 — Visualization**
- Generated 8 charts and wrapped everything in a Streamlit app

---

