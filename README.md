# 💧 Kenya Water Quality Analysis (2000–2024)

A comprehensive data analysis project evaluating Kenya's national water access, regional sanitation coverage, and **chemical water quality** using World Bank, HDX, and KEWI datasets.

---

## 📖 Project Overview


In Kenya, having access to a water source doesn't always mean the water is safe. A household might be connected to a piped system or have a borehole nearby, but the water itself could contain dangerous levels of salts, minerals, or be too acidic. 

This project dives deep into **493 water samples** collected by the **Kenya Water Institute (KEWI)** across the country between 2011 and 2012. The samples were tested against the national safety limits set by the **Kenya Bureau of Standards (KEBS)** to see exactly what is in the water. 

The main finding: **Access is improving nationwide, but the chemical quality of the water is highly variable and geographically uneven.**

### 📏 The National Safety Rules (KEBS Standards)
To judge if water is safe, we compare it against these three main chemical rules:ph, Conductivity and Total Dissolved Solids
*   **pH:** This is basically the measure of acidity or alkalinity of water on a scale of 1 to 14 ie:
1-6=acidic water
7=netral water
8-14=basic/alkaline water
*   **pH:** Must be between **6.50 and 8.50**. (If it's too low, the water is 
acidic and can corrode pipes; if it's too high, it's bitter).

*   **Conductivity:**
Water conductivity measures how easily electricity flows through water. Water conductivity increases with increase in the amount of minerals and salts in water therefore pure water has poor water conductivity.
*   **Conductivity:** Must be **≤ 2500.00 µS/cm**. (Measures how much salt is dissolved in it).

*   **Total Dissolved Solids (TDS)** 
Total Dissolved solids is the total amount of tiny bits of minerals, salts, and metals dissolved in the water
*   **Total Dissolved Solids (TDS):** Must be **≤ 1000.00 mg/L**. (The weight of all microscopic minerals floating in the water).

---

## ❗ Problem Statement

*   **Invisible Threats:** Contaminated water doesn't look dirty. You can't see high salt levels or dangerous acidity with the naked eye.
*   **The Testing Gap:** Only a tiny fraction of Kenya's 47 counties are continuously testing their water. 
*   **Health Distress:** Drinking water with excessive salts can lead to long-term health issues like hypertension, while corrosive water damages the pipes meant to deliver it. 

---

## 🎯 Objectives

**General:** To assess water quality across Kenya using laboratory test data and identify actionable solutions for regional infrastructure.

**Specific:**
1. Examine the distribution of each water quality parameter (pH, conductivity, TDS).
2. Compare water quality across different water source types (boreholes, rivers, etc.).
3. Identify county-level patterns in water quality.
4. Analyze correlations between parameters to see if testing one can predict another.

---

## ❓ Research Questions

1. How are pH, conductivity, and TDS distributed across tested samples?
2. How does water quality vary by source type (borehole, rain, effluent)?
3. Which counties show unusual patterns in pH, conductivity, or TDS?
4. Do water quality parameters correlate — can one predict another?

---

## 👥 Target Audience

| Audience | Why This Matters to Them |
|---|---|
| **🏛️ Policymakers** | Ministry of Water, County governments, NEMA, WRA need to know where to prioritize funding for Reverse Osmosis and pH adjustment. |
| **🌍 Development Organizations** | UNICEF, WHO, Water.org, and local WRUAs need data to target interventions in the worst-performing counties. |
| **🎓 Researchers** | Environmental scientists and public health officials can build upon this data to investigate external factors like heavy metals and bacteria. |

---

## 📊 Data Sources

| Source | What It Provides | Coverage | Contribution |
|---|---|---|---|
| **Kenya Water Institute (KEWI)** | 493 water sample lab tests (pH, conductivity, TDS) | 2011–2012 | Water quality analysis |

---

## 🛠️ Technology Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Data processing and analysis |
| **pandas / numpy** | Data cleaning and transformation |
| **SQLite** | Database storage |
| **Plotly Express / Graph Objects** | Interactive chart generation |
| **Streamlit** | Interactive web application framework |
| **Git & GitHub** | Version control and hosting |

## 🔬 Methodology

**Phase 1 — Data Collection**
- Pulled data from World Bank API, HDX, and KEWI sources.

**Phase 2 — Cleaning & Standardization**
- Standardized column names.
- Converted text numbers to numeric (e.g., `"67%"` → `67.0`).
- **Filtered Data:** Explicitly removed rows from non-Kenyan locations (e.g., Somalia, Mogadishu) to ensure accuracy.
- **Source Standardization:** Used keyword matching to clean and unify messy water source names (grouping typos like "Bore Hole" and "b/hole" into a single "Borehole" category).

**Phase 3 — Storage**
- Loaded all datasets into `data/processed/kenya_water.db` (SQLite).

**Phase 4 — Analysis**
- Calculated the percentage of samples violating KEBS standards per county.
- Grouped data by water source to find the primary drivers of risk.
- Ran Pearson correlation matrices.

**Phase 5 — Visualization**
- Generated interactive Plotly charts and deployed the entire analysis as a Streamlit app.
