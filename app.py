"""
Kenya Water Quality Analysis — Streamlit App
Run: streamlit run app.py
"""

import os
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    ["🏠 Overview", "🚨 Step 1: Risk Assessment", "🔍 Step 2: Root Cause Analysis", 
     "📈 Correlations", "💡 Recommendations", "🔍 Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About**")
st.sidebar.info("Analysis of 493 water samples from the Kenya Water Institute (2011–2012).")
st.sidebar.markdown("---")
st.sidebar.markdown("**Standards used**")
st.sidebar.markdown("- KEBS KS 459-1\n- WHO Guidelines")

# ============================================================
# Cached data loader & Helper Functions
# ============================================================
DB_PATH = "data/processed/kenya_water.db"

@st.cache_data
def load_water_df():
    conn = sqlite3.connect(DB_PATH)
    d = pd.read_sql_query("SELECT * FROM kewi_water_tests", conn)
    conn.close()
    d.columns = [c.strip().lower().replace(" ", "_") for c in d.columns]
    
    # Filter out non-Kenyan locations
    non_kenyan = ["somalia", "mogadishu", "moshitanzania", "iringa"]
    d = d[~d["county"].astype(str).str.lower().str.strip().isin(non_kenyan)]
    return d

def clean_source(s):
    s = str(s).lower().strip()
    if "bore" in s or "b/hole" in s: return "Borehole"
    elif "river" in s or "stream" in s or "surface" in s: return "River/Stream"
    elif "shallow" in s or "well" in s: return "Shallow Well"
    elif "pipe" in s or "tap" in s or "treated" in s or "domestic" in s: return "Piped/Treated"
    elif "rain" in s or "roof" in s: return "Rainwater"
    elif "effluent" in s or "waste" in s or "sewage" in s or "influent" in s: return "Effluent"
    else: return None

# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.title("💧 Kenya Water Quality Analysis")
    st.markdown("### 493 lab samples · 2011–2012")
    st.markdown("---")

    st.markdown("## 📖 Project Overview")
    st.markdown("""

    In Kenya, having access to a water source doesn't always mean the water is safe. A household might be connected to a piped system or have a borehole nearby, but the water itself could contain dangerous levels of salts, minerals, or be too acidic. 

    This project dives deep into **493 water samples** collected by the **Kenya Water Institute (KEWI)** across the country between 2011 and 2012. We tested these samples against the national safety limits set by the **Kenya Bureau of Standards (KEBS)** to see exactly what is in the water. 

    ### 📏 The National Safety Rules (KEBS Standards)
    *   **pH:** Must be between **6.50 and 8.50**. (If it's too low, the water is acidic and can corrode pipes; if it's too high, it's bitter).
    *   **Conductivity:** Must be **≤ 2500.00 µS/cm**. (Measures how much salt is dissolved in it).
    *   **Total Dissolved Solids (TDS):** Must be **≤ 1000.00 mg/L**. (The weight of all microscopic minerals floating in the water).
    """)

    st.markdown("---")
    st.markdown("## ❗ Problem Statement")
    st.markdown("""
    **The problem? We are drinking water blindly.**

    *   **Invisible Threats:** Contaminated water doesn't look dirty. You can't see high salt levels or dangerous acidity with the naked eye.
    *   **The Testing Gap:** Only a tiny fraction of Kenya's 47 counties are continuously testing their water. Where testing does happen, the data is often locked away in spreadsheets.
    *   **Real-World Consequences:** Drinking water with excessive salts can lead to long-term health issues like hypertension, while corrosive water damages the pipes meant to deliver it.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Objectives")
    st.markdown("""
    **General:** To assess water quality across Kenya using laboratory test data.
    
    **Specific:**
    1. Examine the distribution of each water quality parameter (pH, conductivity, TDS).
    2. Compare water quality across different water source types (boreholes, rivers, etc.).
    3. Identify county-level patterns in water quality.
    4. Analyze correlations between parameters to see if testing one can predict another.
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
        st.markdown("- Ministry of Water\n- County governments\n- NEMA, WRA")
    with col2:
        st.markdown("#### 🌍 Development Orgs")
        st.markdown("- UNICEF, WHO\n- Water.org\n- Local WRUAs")
    with col3:
        st.markdown("#### 🎓 Researchers")
        st.markdown("- Environmental science\n- Public health\n- Water chemistry")

# ============================================================
# STEP 1 — RISK ASSESSMENT
# ============================================================
elif page == "🚨 Step 1: Risk Assessment":
    st.title("🚨 Step 1: Risk Assessment")
    st.markdown("""
    **What we do:** Evaluate how many samples in each county violate KEBS/WHO standards.
    **Goal:** Rank counties from Highest Risk to Lowest Risk across all three factors.
    """)
    
    st.info("""
    **KEBS Standards:** pH (6.50 – 8.50) | Conductivity (≤ 2500) | TDS (≤ 1000)
    """)
    st.markdown("---")

    df = load_water_df()
    ph_col, cond_col, tds_col, county_col = "ph", "conductivity?s/cm", "total_dissolved_solids", "county"

    for c in [ph_col, cond_col, tds_col]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    agg = df.dropna(subset=[county_col]).groupby(county_col).agg(
        n_samples=(ph_col, "count"),
        ph_fail=(ph_col, lambda x: ((x < 6.5) | (x > 8.5)).sum()),
        cond_fail=(cond_col, lambda x: (x > 2500).sum()),
        tds_fail=(tds_col, lambda x: (x > 1000).sum())
    )
    
    agg = agg[agg["n_samples"] >= 5].copy()
    agg["pH Violation %"] = (agg["ph_fail"] / agg["n_samples"] * 100).fillna(0).round(2)
    agg["Cond Violation %"] = (agg["cond_fail"] / agg["n_samples"] * 100).fillna(0).round(2)
    agg["TDS Violation %"] = (agg["tds_fail"] / agg["n_samples"] * 100).fillna(0).round(2)
    agg["Overall Fail %"] = (agg["pH Violation %"] + agg["Cond Violation %"] + agg["TDS Violation %"]) / 3
    
    agg_sorted = agg.sort_values("Overall Fail %", ascending=False).reset_index()

    st.markdown("### 🚨 1. pH Risk by County")
    ph_chart_data = agg_sorted[agg_sorted["pH Violation %"] > 0].sort_values("pH Violation %", ascending=False)
    fig_ph = px.bar(ph_chart_data, x=county_col, y="pH Violation %", template="plotly_white", color="pH Violation %", color_continuous_scale="Reds")
    fig_ph.update_layout(xaxis_tickangle=-45, height=350, coloraxis_showscale=False)
    st.plotly_chart(fig_ph, use_container_width=True)

    st.markdown("### 🚨 2. Conductivity Risk by County")
    cond_chart_data = agg_sorted[agg_sorted["Cond Violation %"] > 0].sort_values("Cond Violation %", ascending=False)
    fig_cond = px.bar(cond_chart_data, x=county_col, y="Cond Violation %", template="plotly_white", color="Cond Violation %", color_continuous_scale="Reds")
    fig_cond.update_layout(xaxis_tickangle=-45, height=350, coloraxis_showscale=False)
    st.plotly_chart(fig_cond, use_container_width=True)

    st.markdown("### 🚨 3. TDS Risk by County")
    tds_chart_data = agg_sorted[agg_sorted["TDS Violation %"] > 0].sort_values("TDS Violation %", ascending=False)
    fig_tds = px.bar(tds_chart_data, x=county_col, y="TDS Violation %", template="plotly_white", color="TDS Violation %", color_continuous_scale="Reds")
    fig_tds.update_layout(xaxis_tickangle=-45, height=350, coloraxis_showscale=False)
    st.plotly_chart(fig_tds, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Overall Highest Risk Counties")
    valid_counties = set(ph_chart_data[county_col]) | set(cond_chart_data[county_col]) | set(tds_chart_data[county_col])
    table_data = agg_sorted[agg_sorted[county_col].isin(valid_counties)].copy()
    
    st.dataframe(
        table_data.head(10)[[county_col, "n_samples", "pH Violation %", "Cond Violation %", "TDS Violation %", "Overall Fail %"]]
        .rename(columns={county_col: "County", "n_samples": "Total Samples", "Overall Fail %": "Avg Risk %"}),
        use_container_width=True
    )

# ============================================================
# STEP 2 — ROOT CAUSE ANALYSIS
# ============================================================
elif page == "🔍 Step 2: Root Cause Analysis":
    st.title("🔍 Step 2: Root Cause Analysis")
    st.markdown("""
    **What we do:** Zoom into the Top 5 worst counties identified in Step 1.
    **Goal:** See which specific water sources are driving the high risk.
    """)
    st.markdown("---")

    df = load_water_df()
    ph_col, cond_col, tds_col, county_col, src_col = "ph", "conductivity?s/cm", "total_dissolved_solids", "county", "type_of_h2o"
    
    for c in [ph_col, cond_col, tds_col]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df[src_col] = df[src_col].apply(clean_source)
    df_clean = df.dropna(subset=[src_col]).copy()

    # DYNAMICALLY GET TOP 5 WORST COUNTIES BASED ON OVERALL RISK
    fail_agg = df_clean.dropna(subset=[county_col]).groupby(county_col).agg(
        n_samples=(ph_col, "count"),
        ph_fail=(ph_col, lambda x: ((x < 6.5) | (x > 8.5)).sum()),
        cond_fail=(cond_col, lambda x: (x > 2500).sum()),
        tds_fail=(tds_col, lambda x: (x > 1000).sum())
    )
    fail_agg = fail_agg[fail_agg["n_samples"] >= 5].copy()
    fail_agg["ph_rate"] = (fail_agg["ph_fail"] / fail_agg["n_samples"] * 100).fillna(0)
    fail_agg["cond_rate"] = (fail_agg["cond_fail"] / fail_agg["n_samples"] * 100).fillna(0)
    fail_agg["tds_rate"] = (fail_agg["tds_fail"] / fail_agg["n_samples"] * 100).fillna(0)
    fail_agg["overall_rate"] = (fail_agg["ph_rate"] + fail_agg["cond_rate"] + fail_agg["tds_rate"]) / 3
    
    worst_counties = fail_agg.sort_values("overall_rate", ascending=False).head(5).index.tolist()

    st.markdown(f"### 🗺️ Main Water Sources in Top 5 High-Risk Counties")
    st.markdown(f"The top 5 worst counties overall are: **{', '.join(worst_counties)}**")
    
    source_county_data = df_clean[df_clean[county_col].isin(worst_counties)]
    fig_src = px.histogram(source_county_data, y=county_col, color=src_col, orientation="h", template="plotly_white", barmode="stack")
    fig_src.update_layout(height=400, legend_title_text="Source Type", margin=dict(l=100))
    st.plotly_chart(fig_src, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔬 Detailed Source Analysis")
    
    target_county = st.selectbox("Select one of the Top 5 Counties to investigate:", worst_counties)
    county_data = df_clean[df_clean[county_col].str.contains(target_county, case=False, na=False)].copy()
    
    if len(county_data) > 0:
        src_stats = county_data.groupby(src_col).agg(
            Avg_pH=(ph_col, "mean"),
            Avg_Cond=(cond_col, "mean"),
            Avg_TDS=(tds_col, "mean")
        ).reset_index()

        st.markdown(f"#### 1. Conductivity in {target_county}")
        fig_cond = px.bar(src_stats, x=src_col, y="Avg_Cond", color=src_col, text_auto=".2f", template="plotly_white")
        fig_cond.add_hline(y=2500, line_dash="dash", line_color="red", annotation_text="KEBS Limit")
        fig_cond.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_cond, use_container_width=True)

        st.markdown(f"#### 2. TDS in {target_county}")
        fig_tds = px.bar(src_stats, x=src_col, y="Avg_TDS", color=src_col, text_auto=".2f", template="plotly_white")
        fig_tds.add_hline(y=1000, line_dash="dash", line_color="red", annotation_text="KEBS Limit")
        fig_tds.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_tds, use_container_width=True)

        st.markdown(f"#### 3. pH in {target_county}")
        fig_ph = px.bar(src_stats, x=src_col, y="Avg_pH", color=src_col, text_auto=".2f", template="plotly_white")
        fig_ph.add_hline(y=6.5, line_dash="dash", line_color="red", annotation_text="KEBS Min")
        fig_ph.add_hline(y=8.5, line_dash="dash", line_color="red", annotation_text="KEBS Max")
        fig_ph.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_ph, use_container_width=True)

        worst_source = src_stats.sort_values("Avg_Cond", ascending=False).iloc[0]
        
        st.markdown(f"""
        ### 🔍 Conclusion for {target_county}
        In {target_county}, **{worst_source[src_col]}** is the primary driver of risk, with an average Conductivity of **{worst_source['Avg_Cond']:.2f} µS/cm**. Targeted treatment (like RO) must be deployed specifically for this source.
        """)

# ============================================================
# CORRELATIONS
# ============================================================
elif page == "📈 Correlations":
    st.title("📈 Parameter Correlations")
    st.markdown("""
    **What we do:** Analyze how pH, Conductivity, and TDS relate to one another mathematically.
    **Goal:** Prove whether measuring one parameter can predict another.
    """)
    st.markdown("---")

    df = load_water_df()
    ph_col, cond_col, tds_col = "ph", "conductivity?s/cm", "total_dissolved_solids"
    
    for c in [ph_col, cond_col, tds_col]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    corr_df = df[[ph_col, cond_col, tds_col]].dropna(how="all")
    corr = corr_df.corr(numeric_only=True)
    
    labels = ["pH", "Conductivity", "TDS"]
    corr.columns = labels
    corr.index = labels

    st.markdown("### 🔥 Correlation Heatmap")
    fig_heat = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1, aspect="equal", template="plotly_white")
    fig_heat.update_layout(height=500)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    ### 🔍 Findings
    *   **Conductivity and TDS:** You will see a correlation near **+1.0**. This is a perfect positive correlation. It proves that Conductivity and TDS measure the exact same thing (dissolved salts). The government does not need to test both; testing Conductivity alone is sufficient and cheaper.
    *   **pH vs. Salts:** You will see a near-zero correlation between pH and the other two. This means knowing the salinity of water tells you absolutely nothing about its pH. They must be tested separately.
    """)

# ============================================================
# RECOMMENDATIONS (User-Friendly)
# ============================================================
elif page == "💡 Recommendations":
    st.title("💡 Recommendations & Future Goals")
    st.markdown("Based on the data analysis from Step 1, Step 2, and the Correlations, here are the actionable recommendations for the Ministry of Water and the government.")
    st.markdown("---")

    st.markdown("## 🎯 Actionable Recommendations")

    st.success("""
    **1. Build Desalination Plants in the North (Reverse Osmosis)**
    **What we found:** The water in Mandera, Wajir, and Garissa is incredibly salty (Conductivity is way above 2500 µS/cm). 
    **What to do:** Instead of just digging more boreholes, the Ministry needs to install Reverse Osmosis (RO) machines that strip the salt out of the water before people drink it. 
    """)

    st.success("""
    **2. Fix the pH in Limestone Areas**
    **What we found:** Places like Kajiado and Machakos have water that is too alkaline (pH above 8.5) because of the rocks underground.
    **What to do:** Water treatment plants in these areas need to add safe, food-grade acids to balance the water. If they don't, the water will taste bitter and ruin people's plumbing.
    """)

    st.success("""
    **3. Stop Factories from Dumping Wastewater**
    **What we found:** When we looked at the different water sources, "Effluent" (wastewater from factories and sewers) was by far the most dangerous, with extreme salt levels.
    **What to do:** The government (NEMA) needs to heavily fine factories and sewage plants that dump untreated water into rivers or boreholes that local communities rely on.
    """)

    st.success("""
    **4. Make Testing Consistent Nationwide**
    **What we found:** Many counties had missing data (like no TDS results). 
    **What to do:** The Ministry should create one strict rule: every county must test for the exact same things (pH, Conductivity, TDS, and bacteria) every few months and upload it to one central system.
    """)

    st.markdown("---")
    st.markdown("## 🚀 Future Goals & Further Analysis")

    st.info("""
    While this project focuses on chemical parameters (pH, Conductivity, TDS), a complete water safety profile requires expanding the scope. Future goals include:
    
    **1. Incorporate External Biological & Chemical Factors:**
    *   **Heavy Metals (e.g., Lead & Arsenic):** Analyzing heavy metals is crucial. Unlike salts, heavy metals are highly toxic even in microscopic amounts and cause irreversible neurological damage. Water in regions with mining or industrial runoff should be urgently tested for these.
    *   **Microbial Pathogens (e.g., E. coli & Coliform):** Chemical tests don't show if sewage is in the water. Testing for microbial contamination is the most direct way to measure immediate health risks and prevent waterborne diseases like cholera.
    *   **Fluoride:** Certain geological regions in Kenya (like the Rift Valley) have dangerously high natural fluoride levels. This should be mapped to prevent dental and skeletal fluorosis.
    *   **Turbidity:** High turbidity (cloudiness) can shield bacteria from chlorine disinfection and should be analyzed alongside biological factors.
    
    **2. Infrastructure and Socioeconomic Analysis:**
    *   Map the distance from water sources to the nearest treatment plants.
    *   Analyze the economic capacity of different counties to afford and maintain advanced filtration systems.
    """)

# ============================================================
# DATA EXPLORER
# ============================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM kewi_water_tests", conn)
    conn.close()
    st.dataframe(df.fillna("Not Tested").head(100), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Python + Streamlit")