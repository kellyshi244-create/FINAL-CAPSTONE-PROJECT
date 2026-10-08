"""
Kenya Water Quality Analysis — Streamlit App
Run: streamlit run app.py
"""

import os
import sqlite3
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Kenya Water Quality Analysis",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("💧 Kenya Water Quality")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Overview", "📊 Visualizations", "🔍 Data Explorer",
     "📖 Methodology", "⚠️ Limitations", "✅ Conclusion"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About**")
st.sidebar.info("Analysis of 493 water samples from the Kenya Water Institute (2011–2012).")
st.sidebar.markdown("---")
st.sidebar.markdown("**Standards used**")
st.sidebar.markdown("- KEBS KS 459-1\n- WHO Guidelines")

# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.title("💧 Kenya Water Quality Analysis")
    st.markdown("### 493 lab samples · 2011–2012")
    st.markdown("---")

    st.markdown("## 📖 Project Description")
    st.markdown("""
    **Clean water is a public health priority in Kenya — yet access does not guarantee safety.**

    A household can be counted as "served" while the water flowing from its tap or borehole
    fails basic chemical standards. This project analyzes **493 water samples** collected by
    the **Kenya Water Institute (KEWI)** in 2011–2012. Each sample was tested for pH,
    conductivity, total dissolved solids (TDS), alkalinity, and colour.

    **Note on time frame:** The dataset spans approximately 6 months (late 2011 to early 2012).
    This is a **cross-sectional snapshot**, not a long-term time series. The strength of this
    dataset is **comparison across geography and sources**, not trend analysis.
    """)

    st.markdown("---")
    st.markdown("## ❗ Problem Statement")
    st.markdown("""
    **Kenya's water safety is unverified at scale.**

    - Only a small fraction of Kenya's 47 counties have continuous water quality monitoring
    - Where water is available, chemical safety is rarely tested
    - Where testing happens, results sit in institutional spreadsheets that never reach policymakers

    Contaminated water causes diarrhoeal disease, heavy-metal poisoning, and long-term health
    damage. The 493 KEWI samples are one of the few available snapshots of Kenya's actual water
    chemistry.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Objectives")
    st.markdown("""
    **General:** To assess water quality across Kenya using laboratory test data.

    **Specific:**
    1. Examine the distribution of each water quality parameter (pH, conductivity, TDS)
    2. Compare water quality across water source types
    3. Identify county-level patterns in water quality
    4. Analyze correlations between parameters
    """)

    st.markdown("---")
    st.markdown("## ❓ Research Questions")
    st.markdown("""
    1. How are pH, conductivity, and TDS distributed across tested samples?
    2. How does water quality vary by source type (borehole, rain, effluent)?
    3. Which counties show unusual patterns in pH or conductivity?
    4. Do water quality parameters correlate — can one predict another?
    """)

    st.markdown("---")
    st.markdown("## 👥 Target Audience")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🏛️ Policymakers")
        st.markdown("""
        - Ministry of Water
        - County governments
        - NEMA, WRA
        """)
    with col2:
        st.markdown("#### 🌍 Development Organizations")
        st.markdown("""
        - UNICEF, WHO
        - Water.org
        - Local WRUAs
        """)
    with col3:
        st.markdown("#### 🎓 Researchers")
        st.markdown("""
        - Environmental science
        - Public health
        - Water chemistry
        """)

# ============================================================
# PAGE 2 — VISUALIZATIONS
# ============================================================
elif page == "📊 Visualizations":
    st.title("📊 Visualizations & Findings")
    st.markdown("The analysis is organized by **aspect of water quality** — not by ranking them. "
                "Each aspect is shown in three views: distribution, by source, by county.")
    st.markdown("---")

    chart_dir = "output/charts"

    # ---------------- SECTION A: pH ----------------
    st.markdown("# 🧪 Section A — pH")
    st.markdown("*pH measures how acidic or alkaline water is. KEBS range: 6.5 – 8.5.*")
    st.markdown("---")

    # Chart 1
    st.markdown("## Chart 1 — pH Distribution")
    path = os.path.join(chart_dir, "01_ph_distribution.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** How many samples fall at each pH value.")
    st.markdown("**Key insight:** Most samples cluster near neutral (pH 7). A few fall outside the KEBS range.")
    st.markdown("**Why:** Geology (limestone raises pH, granite lowers it), industrial effluent, agricultural runoff.")
    st.markdown("---")

    # Chart 2
    st.markdown("## Chart 2 — pH by Water Source Type")
    path = os.path.join(chart_dir, "02_ph_by_source.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** Box plot of pH grouped by source type.")
    st.markdown("""
    **How to read a box plot:**
    - The **box** = the middle 50% of samples
    - The **line inside the box** = median (middle value)
    - The **whiskers** = the full range of most samples
    - **Dots outside** = unusual values (outliers)
    """)
    st.markdown("**Key insight:** Rain and borehole water cluster tightly near neutral. Effluent and river water vary more.")
    st.markdown("**Why:** Rain is naturally distilled and clean. Effluent carries chemicals from treatment processes. Rivers vary with runoff.")
    st.markdown("---")

    # Chart 3
    st.markdown("## Chart 3 — Average pH by County")
    path = os.path.join(chart_dir, "03_ph_by_county.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** Average pH for each county with at least 5 samples.")
    st.markdown("**Key insight:** Most counties cluster near neutral pH. A few outliers sit below or above the KEBS range.")
    st.markdown("""
    **Why Mandera stands out with high pH:** Mandera sits on limestone-rich geological formations
    in Kenya's arid northeast. Water passing through these rocks dissolves alkaline minerals
    (calcium carbonate), raising pH. The dry climate concentrates these minerals further through
    evaporation. This is a **natural, geological cause** — not human pollution.
    """)
    st.markdown("---")

    # ---------------- SECTION B: Conductivity ----------------
    st.markdown("# ⚡ Section B — Conductivity")
    st.markdown("*Conductivity measures dissolved salts and minerals. KEBS limit: ≤2500 µS/cm.*")
    st.markdown("---")

    # Chart 4
    st.markdown("## Chart 4 — Conductivity Distribution")
    path = os.path.join(chart_dir, "04_conductivity_distribution.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** How many samples fall at each conductivity level.")
    st.markdown("**Key insight:** Most samples sit well below the KEBS limit.")
    st.markdown("**Why:** Lower conductivity = fewer dissolved minerals = cleaner water.")
    st.markdown("---")

    # Chart 5
    st.markdown("## Chart 5 — Conductivity by Water Source Type")
    path = os.path.join(chart_dir, "05_conductivity_by_source.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** Average conductivity for each source type.")
    st.markdown("**What is effluent?** Treated wastewater released from sewage treatment plants or factories — the 'end of pipe' after processing.")
    st.markdown("**Key insight:** Effluent has the highest conductivity. Rain water has the lowest.")
    st.markdown("**Why:** Effluent collects dissolved chemicals from homes and industry. Rain is naturally low in dissolved ions.")
    st.markdown("---")

    # Chart 6
    st.markdown("## Chart 6 — Average Conductivity by County")
    path = os.path.join(chart_dir, "06_conductivity_by_county.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** Average conductivity for each county with at least 5 samples.")
    st.markdown("""
    **Why arid and semi-arid counties stand out:**
    - **Evaporation** — Dry heat concentrates salts in groundwater
    - **Low rainfall** — Less dilution of dissolved minerals
    - **Geology** — Machakos and Kajiado sit on metamorphic rock belts rich in soluble ions
    - **Long residence time** — Water stays in aquifers longer, dissolving more minerals

    **Does this affect water quality?** Yes, negatively. High conductivity means:
    - Salty or metallic taste
    - Possible long-term health effects (hypertension)
    - Requires treatment (reverse osmosis) before drinking
    """)
    st.markdown("---")

    # ---------------- SECTION C: TDS ----------------
    st.markdown("# 💧 Section C — Total Dissolved Solids (TDS)")
    st.markdown("*TDS measures the total weight of everything dissolved in water — salts, minerals, metals. KEBS limit: ≤1000 mg/L.*")
    st.markdown("---")

    # Chart 7
    st.markdown("## Chart 7 — TDS Distribution")
    path = os.path.join(chart_dir, "07_tds_distribution.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** How many samples fall at each TDS level.")
    st.markdown("""
    **How to read TDS levels:**
    - **< 300 mg/L** → Excellent — clean, fresh-tasting
    - **300 – 600** → Good — typical drinking water
    - **600 – 900** → Fair — noticeable mineral taste
    - **> 1000** → Fails KEBS standard
    """)
    st.markdown("**Key insight:** Most samples fall below the KEBS limit, indicating acceptable mineral content.")
    st.markdown("**Why:** Low rainfall (less dilution), long water-rock contact time, and industrial/agricultural runoff all raise TDS.")
    st.markdown("---")

    # ---------------- SECTION D: Relationships ----------------
    st.markdown("# 🔗 Section D — Relationships Between Parameters")
    st.markdown("---")

    # Chart 8
    st.markdown("## Chart 8 — Correlation Between Parameters")
    path = os.path.join(chart_dir, "08_correlation_heatmap.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    st.markdown("**What it shows:** How strongly each parameter is related to the others.")
    st.markdown("""
    **How to read it:**
    - **+1.0** = perfect positive relationship (both go up together)
    - **0.0** = no relationship
    - **−1.0** = perfect negative relationship (one goes up, other goes down)
    """)
    st.markdown("**Key insight:** Conductivity and TDS show a strong positive correlation — they measure essentially the same thing (dissolved ion content).")
    st.markdown("""
    **What does this mean for water quality?**
    - Strong correlation means: **if you measure one, you know the other.** Testing becomes cheaper.
    - Weak correlation between other pairs means: **each parameter must be tested separately.** You cannot predict pH from conductivity.
    """)

# ============================================================
# PAGE 3 — DATA EXPLORER
# ============================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("Explore the 493 KEWI water samples. Empty cells mean the test was "
                "**not performed on that sample** — not a data error.")

    conn = sqlite3.connect("data/processed/kenya_water.db")
    df = pd.read_sql_query("SELECT * FROM kewi_water_tests", conn)
    conn.close()

    st.markdown(f"**{len(df)} rows · {len(df.columns)} columns**")

    df_display = df.copy().fillna("Not Tested")
    n_rows = st.slider("Rows to display:", 10, 493, 50, 10)
    st.dataframe(df_display.head(n_rows), use_container_width=True)

    st.info("""
    💡 **Why 'Not Tested'?** KEWI ran different test panels on different samples.
    A sample tested only for pH will show 'Not Tested' in conductivity, TDS, and alkalinity.
    These nulls are preserved and not filled with zeros — that would distort every average.
    """)

# ============================================================
# PAGE 4 — METHODOLOGY
# ============================================================
elif page == "📖 Methodology":
    st.title("📖 Methodology")

    st.markdown("""
    ### Phase 1 — Data Loading
    - Loaded 493 samples from `kenya_water.db` → `kewi_water_tests`

    ### Phase 2 — Cleaning
    - Converted text-stored numbers to numeric
    - Standardized county names — mapped to Kenya's 47 official counties
    - Removed non-Kenyan entries and old provincial names
    - Preserved nulls — they mean "test not performed", not zero

    ### Phase 3 — Analysis
    - Examined distribution of each parameter (pH, conductivity, TDS)
    - Compared values across source types
    - Grouped by county (n ≥ 5 samples for statistical reliability)
    - Ran correlation analysis between parameters

    ### Phase 4 — Visualization
    - Generated 8 charts organized by aspect
    - Deployed as this Streamlit app
    """)

    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - **Python 3.12** — core language
    - **pandas / numpy** — data processing
    - **SQLite** — database storage
    - **matplotlib / seaborn** — charts
    - **Streamlit** — web deployment
    - **Git / GitHub** — version control
    """)

# ============================================================
# PAGE 5 — LIMITATIONS
# ============================================================
elif page == "⚠️ Limitations":
    st.title("⚠️ Limitations")

    st.markdown("""
    ### Data Limitations
    - **Snapshot, not time series** — Only 6 months of data (late 2011 to early 2012).
    - **Concentrated coverage** — Testing concentrated in a few counties.
    - **Partial test panels** — Conductivity, TDS, and alkalinity tested on only ~25% of samples.
    - **No microbial data** — E. coli and coliform not measured.
    - **No heavy metals** — Lead, arsenic, and chromium not in dataset.
    - **Historical** — 2011–2012 data may not reflect current conditions.

    ### Methodological Limitations
    - Small county sample sizes reduce statistical reliability.
    - Correlations are described, not proven causal.
    - Counties with fewer than 5 samples are excluded from county-level charts.
    """)

# ============================================================
# PAGE 6 — CONCLUSION
# ============================================================
elif page == "✅ Conclusion":
    st.title("✅ Conclusion")
    st.markdown("---")

    st.markdown("""
    ### What This Analysis Reveals

    The 493 KEWI samples show that Kenya's water quality is **mixed**.

    - **pH** — Most samples are within the KEBS safe range (6.5–8.5). A minority fall outside.
    - **Conductivity** — Most samples are well below the KEBS limit. Some arid-zone counties
      show higher values due to geology and evaporation.
    - **TDS** — Most samples fall below the 1000 mg/L limit.
    - **Sources matter** — Effluent and river samples are consistently more variable than rain
      and borehole samples.
    - **Conductivity and TDS are linked** — measuring one tells you the other.

    ### What Remains Uncertain

    - Sample sizes vary widely by county. Some counties have only a handful of tests.
    - The dataset is 12+ years old.
    - Microbial safety (E. coli, coliform) is not measured.
    - Heavy metals (lead, arsenic) are not tested.
    """)

    st.markdown("---")
    st.markdown("## 💡 Recommendations")

    st.success("""
    **1 — Expand testing coverage.**
    Testing is concentrated in a few counties. Every county should have at least annual water
    quality testing to build a national picture.
    """)

    st.success("""
    **2 — Standardize test panels.**
    Every sample should be tested for at least pH, conductivity, TDS, and colour. The current
    dataset shows inconsistent panels, making comparisons difficult.
    """)

    st.success("""
    **3 — Add microbial and heavy-metal testing.**
    Chemical parameters alone do not tell the full safety story. E. coli and heavy metals are
    critical for public health assessment.
    """)

    st.success("""
    **4 — Publish water quality data openly.**
    Institutions like KEWI collect valuable data. Publishing it in a standard, accessible format
    would let researchers, policymakers, and the public see the same picture.
    """)

    st.markdown("---")
    st.markdown("""
    ### Final Thought

    This project does not solve Kenya's water crisis. It shows how one snapshot of data
    can be analyzed to reveal what is known — and, just as importantly, what is not.
    """)

# ============================================================
# FOOTER
# ============================================================
st.sidebar.markdown("---")
st.sidebar.caption("Built with Python + Streamlit")