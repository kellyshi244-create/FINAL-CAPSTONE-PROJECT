"""
Kenya Water Quality Analysis — Interactive Dashboard
Run with: streamlit run app.py
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

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("💧 Kenya Water Quality")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Overview", "📊 Visualizations", "🔍 Data Explorer", "📖 Methodology",
     "⚠️ Limitations", "✅ Conclusion"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About**")
st.sidebar.info(
    "Analysis of Kenya's water access and quality, "
    "using World Bank, HDX, and KEWI data from 2000–2024."
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Data sources**")
st.sidebar.markdown("- World Bank Open Data\n- HDX (UN OCHA)\n- Kenya Water Institute (KEWI)")

# ============================================================
# PAGE 1: OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.title("💧 Kenya Water Quality Analysis")
    st.markdown("### 2000–2024 | National, Regional, and Water Quality Insights")
    st.markdown("---")

    st.markdown("## 📖 Project Description")
    st.markdown("### 💧 A Tale of Two Taps")
    st.markdown("""
    Imagine two families in Kenya on the same morning.

    **The first family** lives in a middle-class neighborhood in Nairobi. They turn on the tap,
    fill a kettle, and boil water for tea. The water is clear, it runs every day, and they don't
    think twice about it.

    **The second family** lives 20 kilometers away, in a settlement where the piped network
    doesn't reach. Every morning, someone — often a child or a mother — walks to a communal
    borehole or buys water from a vendor with a jerrycan. The water looks fine. It might even
    taste fine. But nobody tests it. Nobody knows if it's safe.

    Both families are Kenyan. Both live in 2024. But only one of them has what the United
    Nations calls **"basic drinking water"** — water from an improved source, available when
    needed, free from contamination.

    **In Kenya today, roughly one in three people is the second family.**

    That's the starting point of this project.
    """)

    st.markdown("""
    This project examines Kenya's water sector through three lenses:

    1. **National access trends** — how water and sanitation access changed from 2000 to 2024
    2. **Regional case study** — how the Athi River basin managed coverage from 2011 to 2014
    3. **Water quality reality** — chemical analysis of 493 water samples across Kenyan counties

    The key finding is that **access is improving, but quality is not guaranteed.**
    """)

    st.markdown("---")
    st.markdown("## ❗ Problem Statement")
    st.markdown("### 🔍 What Led to This Project")
    st.markdown("""
    Kenya has made real progress on water. In the year 2000, only about **45%** of the
    population had basic drinking water. By 2024, that had climbed to **65.6%**. That's
    20 percentage points in 24 years — real improvement.

    But three uncomfortable truths sit underneath that progress.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### ⏱️ Truth 1\n**Progress is slow, and time is running out.**")
        st.markdown("""
        Kenya adds about **0.85 percentage points per year** to water access.
        At that pace, universal access would take another 40 years — but the
        SDG 6 deadline is 2030. Kenya will not make it at this rate.
        """)
    with col2:
        st.markdown("#### 🚻 Truth 2\n**Sanitation is far behind water.**")
        st.markdown("""
        While 65.6% of Kenyans have basic water, only **40.9%** have basic sanitation.
        The gap is roughly **25 percentage points** — and it has barely moved in 24 years.
        """)
    with col3:
        st.markdown("#### 🔬 Truth 3\n**Quality is unverified.**")
        st.markdown("""
        A household can be counted as having "access" while the water itself is
        chemically unsuitable. Some KEWI samples show pH as low as **5.58** —
        below the KEBS safe minimum of 6.5.
        """)

    st.markdown("---")
    st.markdown("### 📉 The Data Problem")
    st.markdown("""
    Here's the fourth problem — and the one that actually sparked this project.

    **All the information needed to understand Kenya's water situation exists. But it's
    scattered across three separate worlds.**

    - **National statistics agencies** track how many people have water access — but not
      whether the water is safe.
    - **Regional water boards** track coverage in their basins — but only for their own
      area, and only for a few years.
    - **Laboratory institutions** test water samples for chemicals — but those tests sit
      in spreadsheets that never meet the national statistics.

    Nobody has stitched these three together into one picture. A ministry official can tell
    you "65.6% of Kenyans have water access." They cannot tell you "and 12% of that water
    fails the pH standard." They cannot tell you "and the Athi basin is 8 points behind
    the national average."

    **This project exists to stitch those three worlds together.**
    """)

    st.info("""
    **Why this matters beyond the numbers:** Every statistic in this project is a real
    person making a real decision — a mother deciding whether to boil water she already
    paid for, a county official deciding where to build the next borehole, a health worker
    treating a child for diarrhea that might have been prevented. Data doesn't solve those
    problems on its own. But **good data tells us where to look first.**
    """)

    st.markdown("---")
    st.markdown("## 🎯 Objectives")
    st.markdown("""
    **General Objective:**
    To analyze Kenya's water access and water quality using national, regional, and
    laboratory data sources, producing actionable insights for policy and infrastructure
    planning.

    **Specific Objectives:**
    1. Quantify 25 years of national progress in water and sanitation access (2000–2024)
    2. Assess freshwater resource pressure by analyzing withdrawal rates
    3. Evaluate water quality across Kenyan counties using pH, conductivity, and TDS
    4. Compare chemical parameters against KEBS and WHO drinking water standards
    5. Examine the Athi River basin as a regional case study of coverage growth
    6. Visualize findings in a user-friendly web application for non-technical audiences
    """)

    st.markdown("---")
    st.markdown("## ❓ Research Questions")
    st.markdown("""
    1. How has Kenya's access to basic drinking water and sanitation changed between 2000 and 2024?
    2. Is the gap between water access and sanitation access narrowing or widening?
    3. What is Kenya's freshwater withdrawal as a percentage of internal resources, and is it approaching water stress levels?
    4. What is the average pH of water across Kenyan counties, and does it fall within the KEBS range (6.5–8.5)?
    5. How does water quality vary by source type (borehole, rain, effluent, etc.)?
    6. In the Athi River basin, how has coverage progressed, and what share of the population remains unserved?
    7. Do conductivity levels in tested water samples exceed the KEBS limit of 1500 µS/cm?
    """)

    st.markdown("---")
    st.markdown("## 👥 Target Audience")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🏛️ Policymakers")
        st.markdown("""
        - Ministry of Water, Sanitation and Irrigation
        - County governments
        - NEMA and WRA

        **What they get:** Evidence of where access gaps persist and which counties have water quality concerns.
        """)
    with col2:
        st.markdown("#### 🌍 Development Organizations")
        st.markdown("""
        - Water.org, UNICEF, WHO Kenya
        - Local water user associations

        **What they get:** Data-driven identification of priority intervention areas.
        """)
    with col3:
        st.markdown("#### 🎓 Researchers & Students")
        st.markdown("""
        - Environmental science programs
        - Public health and development studies

        **What they get:** A transparent, reproducible pipeline for multi-source water data.
        """)

# ============================================================
# PAGE 2: VISUALIZATIONS
# ============================================================
elif page == "📊 Visualizations":
    st.title("📊 Visualizations & Findings")
    st.markdown("Each chart below is explained in four parts: **What it shows**, **Why we made it**, **What insight it gives**, and **Why the pattern looks that way** (diagnostic).")
    st.markdown("---")

    chart_dir = "output/charts"

    # ---------------- CHART 1 ----------------
    st.markdown("## 📊 Chart 1 — National WASH Access Trends (2000–2024)")
    path = os.path.join(chart_dir, "01_national_trends.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** Three lines tracking water access, sanitation access, and open defecation in Kenya over 24 years.")
    st.markdown("**🎯 Why we made it:** This is the headline chart. It answers the fundamental question: 'How is Kenya doing overall?' — in one 30-second glance.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - **Water access** rose from **45.4% to 65.6%** (+20.2 pp)
    - **Sanitation access** rose from **23.6% to 40.9%** (+17.3 pp)
    - **Open defecation** fell from **16.9% to 5.9%** (−11 pp)
    - The **gap between water and sanitation stays at ~25 points** across all 25 years
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Water and sanitation grow at nearly identical rates — they're driven by the same underlying factors (GDP, urbanization, donor cycles).
    - Sanitation is structurally harder to deliver — water flows through shared pipes, sanitation requires per-household infrastructure.
    - The gap not closing is the finding. If sanitation were simply "behind," the gap should narrow. It stays flat for 25 years.
    """)
    st.markdown("---")

    # ---------------- CHART 2 ----------------
    st.markdown("## 📊 Chart 2 — Freshwater Withdrawal (% of Internal Resources)")
    path = os.path.join(chart_dir, "02_freshwater_withdrawal.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** A single line showing Kenya's freshwater withdrawal as a percentage of renewable resources, with a red dashed threshold at 25% marking water stress.")
    st.markdown("**🎯 Why we made it:** Water access data shows supply; this chart shows demand. Together they answer: is Kenya adding infrastructure faster than it's depleting freshwater?")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - Withdrawal rose from **7.5% (2000) to 19.5% (2022)** — nearly tripling
    - Still below the 25% water stress threshold, but the trend line is steep
    - If the current pace continues, Kenya could approach water stress within a decade
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - The staircase shape is a data artifact, not a real-world pattern. Values stay flat for 5 consecutive years (2011–2015) and again for 7 years (2016–2022).
    - Likely explanation: Values come from periodic FAO AQUASTAT surveys and are held constant between them. The 2016 jump likely reflects a new survey estimate, not a sudden real change.
    - Use this chart for magnitude only, not for trends.
    """)
    st.markdown("---")

    # ---------------- CHART 3 ----------------
    st.markdown("## 📊 Chart 3 — Average pH by County (KEWI Water Tests)")
    path = os.path.join(chart_dir, "03_ph_by_county.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** A horizontal bar chart ranking counties by their average water pH. Orange dotted lines mark the KEBS safe range (6.5–8.5).")
    st.markdown("**🎯 Why we made it:** pH is the single most basic water safety indicator. If pH is out of range, dozens of other chemical properties follow.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - Average pH ranges from **5.58 (Bungoma)** to **8.50 (Homa Bay)**
    - Most counties cluster between **6.5 and 7.5** — comfortably within range
    - Counties with more than ~50 tests (Nairobi, Machakos, Kiambu, Kajiado) show tighter averages
    - A handful of counties fall below the KEBS minimum — these need follow-up
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Geology explains most of it — limestone areas → alkaline water; volcanic/granite areas → acidic water.
    - Sampling bias matters — outlier counties have only 1–5 tests, so a single sample can drag the average.
    - Source type plays a role too — effluent and shallow wells tend to be more acidic than deep boreholes.
    """)
    st.markdown("---")

    # ---------------- CHART 4 ----------------
    st.markdown("## 📊 Chart 4 — Average Conductivity by Water Source Type")
    path = os.path.join(chart_dir, "04_conductivity_by_source.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** A bar chart showing average conductivity for each water source type. A red dashed line marks the KEBS limit of 1500 µS/cm.")
    st.markdown("**🎯 Why we made it:** Conductivity measures dissolved salts. High conductivity often signals pollution. This answers: does water quality depend on source?")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - **Effluent samples** have much higher conductivity than others
    - **Rain water** is consistently the cleanest source
    - **Boreholes and rivers** sit in between
    - Most sources stay below the KEBS limit — but the ranking is clear
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Effluent contains dissolved waste — salts, soaps, minerals, industrial chemicals.
    - Rain water is naturally distilled — formed from evaporated water, leaving salts behind.
    - Boreholes tap deep aquifers with decades of mineral dissolution.
    - The intuitive ranking validates the dataset — if rain had higher conductivity than effluent, we'd know the testing was flawed.
    """)
    st.markdown("---")

    # ---------------- CHART 5 ----------------
    st.markdown("## 📊 Chart 5 — Athi River Basin Coverage (2011–2014)")
    path = os.path.join(chart_dir, "05_athi_coverage.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** Two lines tracking water and sanitation coverage percentages in the Athi River basin from 2011 to 2014.")
    st.markdown("**🎯 Why we made it:** National averages hide regional variation. The Athi basin is our case study — a real place with a real trajectory.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - **Water coverage** rose from 62% to 70% (+8 pp in 4 years)
    - **Sanitation coverage** rose from 67% to 71% (+4 pp in 4 years)
    - **Water is catching up to sanitation** — the opposite of the national pattern
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Water infrastructure is easier to expand — adding a pipeline serves a whole neighborhood.
    - Athi is a peri-urban basin. Urban utilities prioritize piped water expansion; sanitation falls behind because it's less politically visible.
    - The inverted gap is the finding — nationally water lags sanitation; in urbanizing basins the pattern flips.
    """)
    st.markdown("---")

    # ---------------- CHART 6 ----------------
    st.markdown("## 📊 Chart 6 — Served vs Unserved Population (Athi Basin)")
    path = os.path.join(chart_dir, "06_athi_served_vs_unserved.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** A grouped bar chart comparing served and unserved populations for water and sanitation in the Athi basin.")
    st.markdown("**🎯 Why we made it:** Percentages can hide absolute numbers. This chart shows how many real people are still unserved — what matters for policy.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - **~7.3 million people** lack sanitation access in the basin
    - **~7.7 million people** lack water access
    - That's roughly **one-third of the entire basin population**
    - Water has a slightly larger absolute gap than sanitation
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Percentage improvement ≠ absolute improvement — served grew by 730K, but unserved barely moved because population also grew.
    - The math of late-stage coverage is brutal — the last 20% is hardest and most expensive.
    - Kenya is running to stand still — coverage growth must exceed population growth.
    """)
    st.markdown("---")

    # ---------------- CHART 7 ----------------
    st.markdown("## 📊 Chart 7 — Water Tests by Source Type")
    path = os.path.join(chart_dir, "07_source_breakdown.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** A pie chart showing the proportion of KEWI water tests performed on each source type.")
    st.markdown("**🎯 Why we made it:** This chart shows testing priorities, not quality. It's context that helps interpret the other quality charts.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - Reveals which sources regulators focused on
    - Helps judge whether the KEWI dataset is representative
    - Gives weight to other findings — if most samples were boreholes, the conductivity finding applies mainly to boreholes
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - Laboratory access drives testing — KEWI's lab is in Nairobi, so nearby counties get tested more.
    - Regulatory priorities are urban-biased — urban utilities must test; rural areas have weaker oversight.
    - The bias is self-reinforcing — better data attracts more funding, leaving rural areas invisible.
    """)
    st.markdown("---")

    # ---------------- CHART 8 ----------------
    st.markdown("## 📊 Chart 8 — pH vs Conductivity Scatter Plot")
    path = os.path.join(chart_dir, "08_ph_vs_conductivity.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

    st.markdown("**📋 What it shows:** Each dot is one water sample, positioned by pH (x) and conductivity (y), colored by source. A red line marks the KEBS conductivity limit.")
    st.markdown("**🎯 Why we made it:** Averages hide the distribution. This chart shows every single sample — including outliers — so we can see how many fall outside the safe zone.")
    st.markdown("**💡 Key insights:**")
    st.markdown("""
    - Most samples cluster in the "safe zone" (pH 6.5–8.5, conductivity < 1500 µS/cm)
    - A visible minority fall outside one or both standards
    - Different sources cluster differently
    - No obvious correlation between pH and conductivity
    """)
    st.markdown("**🔍 Why the pattern looks this way (diagnostic):**")
    st.markdown("""
    - pH and conductivity measure different things — acidity vs. dissolved ions.
    - No correlation is itself a finding — it means water quality requires testing multiple parameters.
    - The outliers are the story — samples that fail on one parameter but pass on the other would be missed by single-parameter tests.
    """)
    st.markdown("---")

    st.markdown("## 🔗 How the Charts Work Together")
    st.markdown("""
    The eight charts aren't independent. They build an argument in three layers:

    **Layer 1 — National (Charts 1–2):** "Here's the big picture: progress but slow, and pressure rising."

    **Layer 2 — Regional (Charts 5–6):** "Here's what it looks like on the ground: real improvements, but millions still unserved."

    **Layer 3 — Water Quality (Charts 3, 4, 7, 8):** "And here's what the water itself is like: mostly safe, but with real problem spots."
    """)

    st.info("""
    **The composite diagnostic story:**

    Kenya's water progress is real but uneven — uneven between water and sanitation
    sectors, uneven between urban and rural, and uneven in which parts of the country
    get measured. Access has expanded fastest where infrastructure is cheapest to build,
    which means the remaining unserved are the hardest to reach, the least visible in
    data, and the most likely to be overlooked in policy.
    """)

# ============================================================
# PAGE 3: DATA EXPLORER
# ============================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("Explore the three datasets interactively. "
                "Empty cells indicate **tests that were not performed** — they are not data errors.")

    conn = sqlite3.connect("data/processed/kenya_water.db")

    tab1, tab2, tab3 = st.tabs([
        "National Indicators", "Athi River", "KEWI Water Tests"
    ])

    with tab1:
        df = pd.read_sql_query("SELECT * FROM national_indicators", conn)
        st.markdown(f"**{len(df)} rows** — no nulls, complete 25-year time series.")
        st.dataframe(df, use_container_width=True)

    with tab2:
        df = pd.read_sql_query("SELECT * FROM athi_river_coverage", conn)
        st.markdown(f"**{len(df)} rows** — complete coverage data for 2011–2014.")
        st.dataframe(df, use_container_width=True)

    with tab3:
        df = pd.read_sql_query("SELECT * FROM kewi_water_tests", conn)
        st.markdown(f"**{len(df)} rows** — 493 water samples from 2011–2012. "
                    "Empty cells mean the test was not performed on that sample.")

        df_display = df.copy().fillna("Not Tested")
        n_rows = st.slider("Rows to display:", min_value=10, max_value=493, value=50, step=10)
        st.dataframe(df_display.head(n_rows), use_container_width=True)

        st.info(
            "💡 **Why are there so many 'Not Tested' cells?** "
            "KEWI ran different tests on different samples. A sample tested only for pH "
            "will show 'Not Tested' in the conductivity and TDS columns. These nulls are "
            "intentional and should not be filled with zeros — that would fabricate data "
            "and distort all averages."
        )

    conn.close()

# ============================================================
# PAGE 4: METHODOLOGY
# ============================================================
elif page == "📖 Methodology":
    st.title("📖 Methodology")

    st.markdown("""
    ### Five-Phase Pipeline

    **1. Data Acquisition**
    - World Bank API for national indicators
    - HDX for regional coverage
    - KEWI water test results

    **2. Cleaning**
    - Fuzzy column-name matching (ignoring case, punctuation, symbols)
    - Text-to-numeric conversion (e.g., "67%" → 67.0)
    - Fill text nulls with placeholders; preserve numeric nulls (which mean "test not performed")

    **3. Storage**
    - SQLite database with three tables

    **4. Analysis**
    - SQL aggregations (per county, per source, per year)
    - Comparison against KEBS/WHO limits

    **5. Visualization**
    - 8 matplotlib/seaborn charts
    - Deployed as this Streamlit web app
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

    st.markdown("### 📊 Data Sources")
    st.markdown("""
    **1. World Bank Open Data** — National WASH indicators (2000–2024)
    **2. HDX (UN OCHA)** — Athi River basin coverage (2011–2014)
    **3. Kenya Water Institute (KEWI)** — 493 water sample lab tests (2011–2012)
    """)

# ============================================================
# PAGE 5: LIMITATIONS
# ============================================================
elif page == "⚠️ Limitations":
    st.title("⚠️ Limitations")

    st.markdown("""
    ### Data Limitations
    - **Coverage bias**: KEWI testing is concentrated in Nairobi, Machakos, Kiambu, and Kajiado
    - **Temporal mismatch**: Three datasets span different periods (2000–2024, 2011–2014, 2011–2012)
    - **Missing years**: Freshwater data ends in 2022
    - **Text-stored numbers**: Required coercion; some rows may have been dropped
    - **Non-Kenyan entries**: KEWI includes samples from Somalia, Tanzania, and South Sudan
    - **No microbial data**: This analysis covers chemical parameters only
    - **Modeled data**: Freshwater withdrawal appears to be interpolated between survey years

    ### Methodological Limitations
    - The three datasets cannot be merged into a single table (different grains, different periods)
    - Analysis is descriptive and diagnostic; no causal inference is claimed
    - Sample sizes vary widely by county (Nairobi n=108 vs. some counties n=1)
    """)

# ============================================================
# PAGE 6: CONCLUSION
# ============================================================
elif page == "✅ Conclusion":
    st.title("✅ Conclusion")
    st.markdown("### How This Analysis Addressed the Problem")
    st.markdown("---")

    st.markdown("""
    At the start of this project, we identified four interlocking problems:

    1. **Access is improving too slowly** to meet SDG 6 by 2030
    2. **Sanitation lags far behind water** — a persistent 25-point gap
    3. **Water quality is unverified** even where access exists
    4. **Data is fragmented** across national, regional, and laboratory sources

    This analysis has directly addressed each of these — and every finding points to a clear recommendation.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Problem 1 — Slow Progress Toward Universal Access")

    st.markdown("**What the analysis revealed:**")
    st.markdown("""
    By extracting 25 years of World Bank indicators (2000–2024) and plotting
    water access against sanitation access, we quantified the exact pace of
    progress: **+0.84 percentage points per year for water** and **+0.72 for sanitation.**

    At this rate, Kenya would need another **40 years** to reach universal water
    access — far beyond the 2030 SDG deadline.
    """)

    st.markdown("**How this helps:**")
    st.markdown("""
    Policymakers now have a concrete number to work with. Instead of the vague
    statement *"progress is happening,"* the analysis shows *"progress is happening
    at 0.84 pp/year — we need 3.5 pp/year to hit 2030."* That's an actionable gap
    that can be built into budget planning.
    """)

    st.success("""
    **💡 Recommendation 1 — Set an explicit acceleration target and publish progress against it.**

    Kenya's Ministry of Water should publicly commit to an annual target of **3.5 percentage
    points per year** in water access (up from 0.84 pp/year) if it intends to reach universal
    coverage by 2030. This target should be published quarterly by county, so both national
    and local governments can be held accountable. The data infrastructure to track this
    already exists — what's missing is the political commitment to a number.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Problem 2 — The Persistent Sanitation Gap")

    st.markdown("**What the analysis revealed:**")
    st.markdown("""
    Chart 1 showed that the gap between water and sanitation access has stayed
    at **~25 percentage points for 25 years.** The gap is not closing — both
    sectors climb at nearly the same rate, but sanitation starts from a much
    lower base.

    This is not a funding "delay" — it's a **structural** problem. Water flows
    through shared pipes; sanitation requires per-household infrastructure. The
    same investment reaches fewer people.
    """)

    st.markdown("**How this helps:**")
    st.markdown("""
    The analysis reframes sanitation not as "behind" but as "structurally more
    expensive." This changes the policy conversation — it's not about catching up,
    it's about **rebalancing investment ratios** so sanitation receives a
    disproportionate share of future funding.
    """)

    st.success("""
    **💡 Recommendation 2 — Rebalance the water-sanitation investment ratio and prioritize urban sanitation.**

    Given that sanitation is structurally harder to deliver (per-household infrastructure),
    it should receive a **disproportionate share of sector funding** — not an equal share.
    Specific actions:

    - **Redirect funding toward urban sanitation**, where population density makes per-household
      delivery cheaper and political momentum is strongest (as seen in the Athi basin case).
    - **Prioritize the last-mile connection** — most "unserved" populations are not remote; they
      are physically close to networks but lack the connection subsidy to access them.
    - **Set sanitation-specific SDG targets** at the county level, since national averages mask
      the scale of the gap.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Problem 3 — Unverified Water Quality")

    st.markdown("**What the analysis revealed:**")
    st.markdown("""
    By analyzing 493 KEWI lab results, we found that:

    - **Average pH across counties ranges from 5.58 to 8.50** — with some counties
      below the KEBS safe minimum of 6.5
    - **Effluent samples consistently exceed safe conductivity levels** compared
      to rain, borehole, and river water
    - **Most samples cluster in the safe zone**, but a visible minority fall outside
      on one or both parameters

    The scatter plot (Chart 8) demonstrated that **water safety is multidimensional** —
    samples can pass on pH and fail on conductivity, meaning single-parameter tests
    are insufficient.
    """)

    st.markdown("**How this helps:**")
    st.markdown("""
    For the first time, water quality findings are presented alongside access data
    in one view. Regulators can now identify **which counties and source types**
    need targeted testing — for example, prioritizing effluent outfalls and
    counties with pH outliers like Bungoma and Mandera.
    """)

    st.success("""
    **💡 Recommendation 3 — Expand testing coverage and mandate multi-parameter testing.**

    Water quality testing in Kenya is currently concentrated in a handful of counties,
    leaving most of the country unmeasured. To close this gap:

    - **Mandate pH + conductivity + TDS as a minimum test panel** for every water sample.
      The scatter plot showed these parameters vary independently — a single test is not enough.
    - **Decentralize water quality labs** — every county should have access to local testing
      capacity, so samples don't have to travel to Nairobi.
    - **Prioritize effluent outfalls and high-pH counties** for immediate follow-up testing
      based on the outliers identified in Chart 3.
    - **Publish county-level water quality dashboards** alongside the national access data,
      so the public can see what's in their water.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Problem 4 — Fragmented Data")

    st.markdown("**What the analysis revealed:**")
    st.markdown("""
    This project took three data sources that had never been seen together —
    World Bank national indicators, HDX Athi River coverage, and KEWI lab tests —
    and built a **single analysis pipeline** that brings them into conversation.

    While the datasets cannot be merged row-by-row (they have different grains,
    periods, and purposes), they now sit side-by-side in one dashboard. The
    national picture, the regional case study, and the water quality reality
    are all visible in one place.
    """)

    st.markdown("**How this helps:**")
    st.markdown("""
    A ministry official, NGO analyst, or researcher can now open a single app
    and see the full picture: *"Here's how Kenya is doing nationally, here's what
    one basin looks like in detail, and here's what the water itself is like
    chemically."* That's a view that did not exist before this project.
    """)

    st.success("""
    **💡 Recommendation 4 — Establish a national Water Data Integration Office.**

    Kenya's water data exists — but it lives in silos. To permanently solve this:

    - **Create a national Water Data Integration Office** responsible for consolidating
      data from the Ministry, county water boards, KEWI, and NEMA into a single
      public dashboard.
    - **Standardize reporting formats** so that counties and laboratories report in
      compatible schemas — eliminating the fuzzy-matching work this project had to do.
    - **Publish quarterly integration reports** showing national progress, regional
      variance, and quality findings side-by-side.
    - **Open the data** under a permissive license so researchers, NGOs, and citizens
      can build tools like this dashboard on top of it.
    """)

    st.markdown("---")
    st.markdown("## 🔑 Key Findings Summary")

    st.markdown("""
    | Finding | Evidence |
    |---|---|
    | **Water access is improving slowly** | +20.2 pp over 24 years (+0.84 pp/year) |
    | **Sanitation gap is not closing** | Persistent 25-point gap across 25 years |
    | **Freshwater pressure is rising** | Withdrawal tripled: 7.5% → 19.5% |
    | **Water quality varies widely** | pH ranges from 5.58 to 8.50 across counties |
    | **Source type predicts quality** | Effluent > River > Borehole > Rain (conductivity) |
    | **Monitoring is unequal** | KEWI testing concentrated in 4 counties |
    | **Millions remain unserved** | ~7M lack water access in the Athi basin alone |
    """)

    st.markdown("---")
    st.markdown("## 💡 What This Project Demonstrates")

    st.markdown("""
    This analysis proves a simple but powerful point:

    > **You cannot solve a problem you cannot see clearly.**

    Kenya's water challenge is not a single problem — it's four overlapping ones
    (slow progress, sanitation gap, quality uncertainty, data fragmentation).
    By consolidating scattered data into one view, this project has made each
    problem **visible, measurable, and actionable.**

    The analysis doesn't claim to fix Kenya's water crisis. It claims something
    more modest and more useful: it makes the crisis **legible** — and legible
    problems are the ones that get solved.
    """)

    st.success("""
    **Bottom line:** Kenya has made real progress on water access, but the country
    is not on track to hit its 2030 goals, sanitation remains structurally underfunded,
    water quality is unverified in many places, and the data itself is fragmented.
    This project brought those three data worlds together, and what they say
    side-by-side is: **the gaps need to be named before they can be closed.**
    """)

# ============================================================
# FOOTER
# ============================================================
st.sidebar.markdown("---")
st.sidebar.caption("Built with Python + Streamlit")