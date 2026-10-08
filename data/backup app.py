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
#SECOND BACKUP
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

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("💧 Kenya Water Quality")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Overview", "📊 Visualizations", "🔍 Data Explorer",
     "📖 Methodology", "⚠️ Limitations", "✅ Conclusion"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About**")
st.sidebar.info("Deep analysis of 493 water samples from the Kenya Water Institute (2011–2012).")
st.sidebar.markdown("---")
st.sidebar.markdown("**Standards used**")
st.sidebar.markdown("- KEBS KS 459-1\n- WHO Guidelines")

# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.title("💧 Kenya Water Quality Analysis")
    st.markdown("### 493 lab samples · 47 counties · 2011–2012")
    st.markdown("---")

    st.markdown("## 📖 Project Description")
    st.markdown("""
    **Clean water is a public health priority in Kenya — yet access does not guarantee safety.**

    A household can be counted as "served" while the water flowing from its tap or borehole
    fails basic chemical standards. This project analyzes **493 water samples** collected by
    the **Kenya Water Institute (KEWI)** in 2011–2012. Each sample was tested for pH,
    conductivity, total dissolved solids (TDS), alkalinity, and colour.

    By comparing results against **KEBS and WHO guidelines**, the analysis identifies:
    - Which parameters most often fail standards
    - Which water sources are riskiest
    - Which counties have the poorest water quality
    - Whether the causes are **natural (geology)** or **human-driven (industry, agriculture)**

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

    The consequences are direct: contaminated water causes diarrhoeal disease, heavy-metal
    poisoning, and long-term health damage. The 493 KEWI samples are one of the few available
    snapshots of Kenya's actual water chemistry. This project uses them to answer:
    **Where does Kenya's water fail, why, and what should be done about it?**
    """)

    st.markdown("---")
    st.markdown("## 🎯 Objectives")
    st.markdown("""
    **General:** To assess water quality compliance across Kenya using laboratory test data,
    and to identify the sources, counties, and causes of contamination.

    **Specific:**
    1. Measure compliance rates for pH, conductivity, TDS, alkalinity, and colour
    2. Compare water quality across source types (borehole, rain, effluent, river)
    3. Identify counties with the poorest water quality
    4. Analyze correlations between quality parameters
    5. Determine whether failures are natural or anthropogenic
    6. Recommend priority interventions
    """)

    st.markdown("---")
    st.markdown("## ❓ Research Questions")
    st.markdown("""
    1. What percentage of samples fail KEBS standards for pH, conductivity, and TDS?
    2. Which water source types are safest, and which are riskiest?
    3. Which counties show the highest rates of non-compliance?
    4. Do quality parameters correlate — can one predict another?
    5. How many samples fail on multiple parameters?
    6. Which failures are caused by geology, and which by human activity?
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

        Evidence of where quality gaps persist.
        """)
    with col2:
        st.markdown("#### 🌍 Development Organizations")
        st.markdown("""
        - UNICEF, WHO
        - Water.org
        - Local WRUAs

        Priority counties for intervention.
        """)
    with col3:
        st.markdown("#### 🎓 Researchers")
        st.markdown("""
        - Environmental science
        - Public health
        - Water chemistry

        A reproducible analysis pipeline.
        """)

# ============================================================
# PAGE 2 — VISUALIZATIONS
# ============================================================
elif page == "📊 Visualizations":
    st.title("📊 Visualizations & Findings")
    st.markdown("Each chart is explained below: **What it shows**, **Why we made it**, "
                "**Key insight**, and **What causes the pattern**.")
    st.markdown("---")

    chart_dir = "output/charts"

    charts = [
        ("01_ph_distribution.png",
         "Chart 1 — pH Distribution",
         "Histogram of pH values across all samples with KEBS range marked (6.5–8.5).",
         "Shows how many samples fall inside vs. outside the safe range.",
         "Most samples cluster near neutral (pH 7), but a visible minority fall outside the KEBS band.",
         "Natural causes: geology (limestone raises pH; granite lowers it) and dissolved CO₂. "
         "Anthropogenic causes: industrial effluent, mining drainage, agricultural runoff."),

        ("02_conductivity_distribution.png",
         "Chart 2 — Conductivity Distribution",
         "Histogram of conductivity values with the KEBS limit (2500 µS/cm) marked.",
         "Shows the spread of dissolved salts across samples.",
         "Most samples sit well below the KEBS limit, but outliers reach high conductivity.",
         "Natural: rock weathering (biotite gneisses, volcanic rock), evaporation in dry seasons. "
         "Anthropogenic: industrial discharge, sewage infiltration."),

        ("03_tds_distribution.png",
         "Chart 3 — Total Dissolved Solids (TDS) Distribution",
         "Histogram of TDS values with the KEBS limit (1000 mg/L) marked. "
         "**TDS = total weight of everything dissolved in water** (salts, minerals, metals).",
         "TDS indicates the total mineral load in water.",
         "Most samples sit below the KEBS limit; a minority exceed it.",
         "Low rainfall (less dilution), long water-rock contact time, agricultural runoff, "
         "and industrial waste all raise TDS."),

        ("04_compliance_rates.png",
         "Chart 4 — Compliance Rate by Parameter",
         "Horizontal bar chart showing the % of samples meeting KEBS standards for each parameter.",
         "Answers: which parameter is the most common failure point?",
         "Compliance varies by parameter — the weakest link defines Kenya's water safety.",
         "Failures cluster where testing panels were limited, or where geology and industry raise risks."),

        ("05_ph_by_source.png",
         "Chart 5 — pH by Water Source Type",
         "Box plot of pH values grouped by source type (borehole, rain, effluent, river).",
         "Compares pH distribution across sources — a proxy for water risk.",
         "Rain water is typically neutral and tight; effluent and river water show wider spread.",
         "Rain water is naturally clean (distilled). Effluent carries chemicals. River water varies "
         "with runoff and upstream discharge."),

        ("06_conductivity_by_source.png",
         "Chart 6 — Conductivity by Water Source Type",
         "Bar chart of average conductivity per source type.",
         "Reveals which sources carry the highest mineral load.",
         "Effluent has the highest conductivity; rain water has the lowest.",
         "Effluent collects dissolved waste. Rain is naturally low in ions. Boreholes accumulate "
         "minerals from rock over decades."),

        ("07_ph_by_county.png",
         "Chart 7 — Average pH by County",
         "Horizontal bar chart ranking counties by average pH. "
         "Red = outside KEBS range; green = within range.",
         "Identifies counties with pH issues.",
         "Most counties cluster near neutral pH. A few fall below the KEBS minimum.",
         "Geology explains most variation. Counties near volcanic or granite formations show "
         "more acidic water; limestone areas show alkaline water."),

        ("08_conductivity_by_county.png",
         "Chart 8 — Average Conductivity by County",
         "Horizontal bar chart ranking counties by average conductivity. Red = exceeds KEBS limit.",
         "Highlights counties with mineral-rich or saline water.",
         "Some counties show significantly higher conductivity than others.",
         "Machakos and Kajiado sit on metamorphic rock belts rich in biotite and basalt — "
         "weathering releases ions into groundwater. Dry climate concentrates salts."),

        ("09_ph_vs_conductivity.png",
         "Chart 9 — pH vs Conductivity Scatter",
         "Scatter plot with pH on x-axis and conductivity on y-axis, colored by source.",
         "Tests whether pH predicts conductivity.",
         "Points scatter widely — no clear line. The parameters vary independently.",
         "pH is driven by CO₂ and mineral acids. Conductivity is driven by dissolved ions. "
         "They respond to different physical and chemical processes."),

        ("10_correlation_heatmap.png",
         "Chart 10 — Correlation Matrix",
         "Heatmap showing correlation between all parameters.",
         "Answers: does one parameter predict another?",
         "Strong correlation between conductivity and TDS. Others vary.",
         "Conductivity and TDS both measure dissolved ions — they move together. "
         "pH and alkalinity are chemically linked but not always linearly."),

        ("11_source_distribution.png",
         "Chart 11 — Samples by Source Type",
         "Pie chart showing what fraction of samples came from each source type.",
         "Reveals whether the dataset is representative across sources.",
         "Boreholes dominate — conclusions skew toward groundwater quality.",
         "Regulators test boreholes most because they are the primary drinking source in most counties."),

        ("12_pass_fail_by_source.png",
         "Chart 12 — pH Pass/Fail by Source Type",
         "Stacked bar chart showing compliant vs. non-compliant counts per source.",
         "Quantifies risk by source.",
         "Some sources have visibly higher failure rates.",
         "Effluent and river samples fail more often because they carry chemicals and runoff. "
         "Boreholes cluster closer to compliance."),

        ("13_parameter_coverage.png",
         "Chart 13 — Test Coverage per Parameter",
         "Bar chart of what % of samples were tested for each parameter.",
         "Shows which parameters have full vs. partial coverage.",
         "pH tested on ~90% of samples. Conductivity, TDS, alkalinity on ~25%.",
         "KEWI ran different test panels on different samples. Not every sample received every "
         "test — this is a **data coverage** finding, not a quality finding."),

        ("14_monthly_samples.png",
         "Chart 14 — Sample Volume by Month",
         "Bar chart showing how many samples were collected each month.",
         "Shows the time distribution of sample collection.",
         "Sampling was uneven across months — one period dominates.",
         "Field campaigns, funding cycles, and seasonal accessibility affect when samples are "
         "collected. This context matters for interpreting the data."),
    ]

    for filename, title, what, why, insight, cause in charts:
        st.markdown(f"## {title}")
        path = os.path.join(chart_dir, filename)
        if os.path.exists(path):
            st.image(Image.open(path), use_container_width=True)
        else:
            st.warning(f"Chart not found: {path}")

        st.markdown(f"**📋 What it shows:** {what}")
        st.markdown(f"**🎯 Why we made it:** {why}")
        st.markdown(f"**💡 Key insight:** {insight}")
        st.markdown(f"**🔍 What causes this pattern:** {cause}")
        st.markdown("---")

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
    - Converted text-stored numbers (conductivity, TDS, alkalinity) to numeric
    - Standardized county names — mapped 53 raw values down to Kenya's 47 official counties
    - Removed non-Kenyan entries (Somalia, Tanzania, South Sudan) and old provincial names
    - Preserved nulls — they mean "test not performed", not zero

    ### Phase 3 — Compliance Classification
    - Compared each sample against KEBS/WHO limits:
      - pH: 6.5 – 8.5
      - Conductivity: ≤2500 µS/cm
      - TDS: ≤1000 mg/L
      - Colour: ≤15 mgPt/l
    - Marked each sample Pass or Fail per parameter

    ### Phase 4 — Analysis
    - Aggregated compliance by parameter, source, and county
    - Ran correlation analysis between parameters
    - Cross-referenced findings with geological and industrial research

    ### Phase 5 — Visualization
    - Generated 14 charts
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
      No long-term trend analysis is possible.
    - **Concentrated coverage** — 4 counties account for the majority of samples.
    - **Partial test panels** — Conductivity, TDS, and alkalinity were tested on only ~25% of samples.
    - **No microbial data** — E. coli and coliform were not measured.
    - **No heavy metals** — Lead, arsenic, and chromium are not in this dataset.
    - **Historical** — 2011–2012 data may not reflect current conditions.

    ### Methodological Limitations
    - Small county sample sizes (1–5 samples) reduce statistical reliability for those counties.
    - Correlations are described, not proven causal.
    - Non-Kenyan entries were removed, reducing the effective dataset.
    """)

# ============================================================
# PAGE 6 — CONCLUSION
# ============================================================
elif page == "✅ Conclusion":
    st.title("✅ Conclusion")
    st.markdown("### The Main Problem and What Should Change")
    st.markdown("---")

    st.markdown("""
    ### The Main Problem

    Kenya's water safety is **not measured at scale**. The 493 KEWI samples reveal real quality
    problems — pH outliers, high conductivity in certain counties, and clear differences between
    sources. But they also reveal a deeper issue: **the country does not have a system for tracking
    water quality continuously or evenly across its 47 counties.**

    Four specific problems emerge:

    1. **Compliance varies by parameter.** Some parameters pass almost universally; others fail
       regularly. The weakest link determines safety.
    2. **Source type predicts quality.** Effluent and river samples are consistently worse than
       rain and borehole samples.
    3. **Counties differ sharply.** Some counties show pH or conductivity well beyond safe limits —
       driven by geology or human activity.
    4. **Data is fragmented and unequal.** Testing is concentrated in four counties, leaving the
       rest of the country unmeasured.
    """)

    st.markdown("---")
    st.markdown("## 🎯 Recommendations")

    st.success("""
    **1 — Mandate a minimum test panel for every water sample.**

    Every sample should be tested for at least pH, conductivity, TDS, and colour. The data shows
    pH was tested on ~90% of samples, but conductivity and TDS on only ~25%. A fixed minimum panel
    closes that gap.
    """)

    st.success("""
    **2 — Decentralize testing so every county has local lab access.**

    Testing today is concentrated in a few counties. County-level labs would make coverage more
    even and detect problems where they occur — instead of requiring samples to travel hundreds
    of kilometers to Nairobi.
    """)

    st.success("""
    **3 — Prioritize follow-up testing in counties with pH or conductivity outliers.**

    The analysis identifies counties with values outside safe limits. These should be retested
    with a full panel to confirm the finding and separate **natural causes (geology)** from
    **human causes (industry, agriculture, mining)**.
    """)

    st.success("""
    **4 — Establish a national Water Quality Data Integration Office.**

    Kenya's water data is fragmented across institutions and never consolidated. A national office
    responsible for collecting, standardizing, and publishing water quality data quarterly would
    allow everyone — policymakers, researchers, and the public — to see the same picture.
    """)

    st.markdown("---")
    st.markdown("## 💡 What This Project Demonstrates")

    st.markdown("""
    Water quality is not a single problem — it is a set of overlapping issues that vary by
    parameter, source, and location. Some are caused by geology and cannot be fixed. Others are
    caused by human activity and can be.

    This analysis does not solve Kenya's water crisis. It makes the crisis **legible** — and
    legible problems are the ones that get solved.
    """)

# ============================================================
# FOOTER
# ============================================================
st.sidebar.markdown("---")
st.sidebar.caption("Built with Python + Streamlit")