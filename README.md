# 💧 Kenya Water Quality Analysis (2000–2024)

A comprehensive data analysis project evaluating Kenya's national water access, regional sanitation coverage, and **chemical water quality** using World Bank, HDX, and KEWI datasets.

---

## 📖 Project Overview


In Kenya, having access to a water source doesn't always mean the water is safe. A household might be connected to a piped system or have a borehole nearby, but the water itself could contain dangerous levels of salts, minerals, or be too acidic. 

This project dives deep into **493 water samples** collected by the **Kenya Water Institute (KEWI)** across the country between 2011 and 2012. We tested these samples against the national safety limits set by the **Kenya Bureau of Standards (KEBS)** to see exactly what is in the water. 

The main finding: **Access is improving nationwide, but the chemical quality of the water is highly variable and geographically uneven.**

### 📏 The National Safety Rules (KEBS Standards)
To judge if water is safe, we compare it against these three main chemical rules:
*   **pH:** Must be between **6.50 and 8.50**. (If it's too low, the water is acidic and can corrode pipes; if it's too high, it's bitter).
*   **Conductivity:** Must be **≤ 2500.00 µS/cm**. (Measures how much salt is dissolved in it).
*   **Total Dissolved Solids (TDS):** Must be **≤ 1000.00 mg/L**. (The weight of all microscopic minerals floating in the water).

---

## ❗ Problem Statement

**The problem? We are drinking water blindly.**

*   **Invisible Threats:** Contaminated water doesn't look dirty. You can't see high salt levels or dangerous acidity with the naked eye.
*   **The Testing Gap:** Only a tiny fraction of Kenya's 47 counties are continuously testing their water. Where testing does happen, the data is often locked away in spreadsheets and not accessible to the public.
*   **Real-World Consequences:** Drinking water with excessive salts can lead to long-term health issues like hypertension, while corrosive water damages the pipes meant to deliver it. 

This app is designed to take the mystery out of Kenya's water. We transform KEWI's raw lab data into interactive charts so policymakers, researchers, and the public can finally see the truth: **Exactly which counties have dangerous water, and why.**

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
| **World Bank Open Data** | National water, sanitation, and freshwater indicators | 2000–2024 | National baseline trends |
| **HDX (UN OCHA)** | Athi River basin coverage (population, served, unserved) | 2011–2014 | Regional case study |
| **Kenya Water Institute (KEWI)** | 493 water sample lab tests (pH, conductivity, TDS) | 2011–2012 | Water quality analysis |

*Note: The datasets are analyzed separately due to differing granularities (national vs. regional vs. per-sample) and combined in the final conclusions.*

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

---

## 📱 App Structure (Streamlit)

The interactive app is broken down into 5 main sections to guide the user through the analysis:

1.  **🏠 Overview:** Defines the problem, KEBS standards, and the objectives of the research.
2.  **🚨 Step 1: Risk Assessment:** Ranks all 47 counties based on the percentage of water samples that fail KEBS standards. Counties are ranked from highest risk to lowest risk.
3.  **🔍 Step 2: Root Cause Analysis:** Investigates the Top 5 worst-performing counties. It breaks down their water sources (boreholes, rivers, etc.) to prove exactly which source is driving the high risk.
4.  **📈 Correlations:** A heatmap proving that Conductivity and TDS are perfectly correlated (measuring the same thing), while pH is completely independent.
5.  **💡 Recommendations:** User-friendly, actionable steps for the government, including building RO plants in the North, fixing pH in limestone areas, and stopping factory wastewater dumping. It also outlines future goals for analyzing heavy metals and bacteria.

---

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

---

## 🚀 Future Goals

While this project focuses on chemical parameters (pH, Conductivity, TDS), a complete water safety profile requires expanding the scope. Future goals include:
*   **Heavy Metals:** Testing for Lead, Arsenic, and Mercury (critical for regions with mining or industrial runoff).
*   **Microbial Pathogens:** Testing for E. coli and Coliform to measure immediate biological health risks.
*   **Fluoride:** Mapping natural fluoride levels, which are dangerously high in parts of the Rift Valley.
*   **Infrastructure Analysis:** Mapping the distance from water sources to the nearest treatment plants and analyzing county economic capacities to maintain them.

---

## 🏃‍♂️ How to Run the App Locally

1. Clone this repository.
2. Install the required packages: `pip install streamlit pandas plotly`
3. Ensure the database is located at `data/processed/kenya_water.db`.
4. Run the app: `streamlit run app.py`

