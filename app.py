import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f5f7fa; }

    /* Metric card styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e4ea;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.82rem !important;
        color: #5a6475 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700;
        color: #1a2133 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 0.82rem !important;
    }

    /* Section header */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a2133;
        margin-top: 0.5rem;
        margin-bottom: 0.6rem;
        padding-bottom: 6px;
        border-bottom: 2px solid #4f8ef7;
        display: inline-block;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a2133;
    }
    [data-testid="stSidebar"] * { color: #d1d9e6 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }

    /* Table styling */
    div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

    /* Tab styling */
    button[data-baseweb="tab"] { font-size: 0.92rem; font-weight: 600; }

    /* Divider */
    hr { border: none; border-top: 1px solid #e0e4ea; margin: 1.2rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Step 1 · Load Data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("SuperMarket Analysis.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    # ── Step 2 · Data Quality ──────────────────────────────────────────────
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Unit price", "Quantity"], inplace=True)

    # Coerce numeric columns
    for col in ["Unit price", "Quantity", "Tax 5%", "Sales", "cogs",
                "gross income", "Rating"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ── Step 3 · Computed Sales ────────────────────────────────────────────
    df["Computed Sales"] = df["Quantity"] * df["Unit price"]
    df["Total Sales (incl. tax)"] = df["Computed Sales"] * 1.05  # 5 % tax

    # Date / time
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.strftime("%b %Y")
    df["Month_num"] = df["Date"].dt.to_period("M").astype(str)
    df["Day of Week"] = df["Date"].dt.day_name()
    df["Hour"] = pd.to_datetime(df["Time"], format="%I:%M:%S %p", errors="coerce").dt.hour

    return df


df = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Supermarket\nSales Analytics")
    st.markdown("---")

    st.markdown("### 🔍 Filters")

    branches = ["All"] + sorted(df["Branch"].dropna().unique().tolist())
    sel_branch = st.selectbox("Branch", branches)

    cities = ["All"] + sorted(df["City"].dropna().unique().tolist())
    sel_city = st.selectbox("City", cities)

    product_lines = ["All"] + sorted(df["Product line"].dropna().unique().tolist())
    sel_product = st.selectbox("Product Line", product_lines)

    genders = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    sel_gender = st.selectbox("Gender", genders)

    customer_types = ["All"] + sorted(df["Customer type"].dropna().unique().tolist())
    sel_ctype = st.selectbox("Customer Type", customer_types)

    payments = ["All"] + sorted(df["Payment"].dropna().unique().tolist())
    sel_payment = st.selectbox("Payment Method", payments)

    st.markdown("---")
    st.markdown("### 📅 Date Range")
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input("Select range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

    st.markdown("---")
    st.caption("📁 Dataset: SuperMarket Analysis.csv")
    st.caption(f"📊 Total Records: {len(df):,}")


# ─── Apply Filters ────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_branch != "All":
    fdf = fdf[fdf["Branch"] == sel_branch]
if sel_city != "All":
    fdf = fdf[fdf["City"] == sel_city]
if sel_product != "All":
    fdf = fdf[fdf["Product line"] == sel_product]
if sel_gender != "All":
    fdf = fdf[fdf["Gender"] == sel_gender]
if sel_ctype != "All":
    fdf = fdf[fdf["Customer type"] == sel_ctype]
if sel_payment != "All":
    fdf = fdf[fdf["Payment"] == sel_payment]
if len(date_range) == 2:
    fdf = fdf[
        (fdf["Date"].dt.date >= date_range[0]) &
        (fdf["Date"].dt.date <= date_range[1])
    ]

# ─── Title ────────────────────────────────────────────────────────────────────
st.markdown("# 🛒 Supermarket Sales Analysis Dashboard")
st.markdown(
    "An end-to-end analytics view covering data quality, computed sales, "
    "groupings, and actionable business insights."
)

if fdf.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview",
    "🔎 Data Quality",
    "💰 Sales Analysis",
    "📦 Product & Branch",
    "👥 Customer Insights",
    "💡 Business Decisions",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">Key Performance Indicators</p>', unsafe_allow_html=True)

    total_sales    = fdf["Total Sales (incl. tax)"].sum()
    total_orders   = len(fdf)
    avg_order      = fdf["Total Sales (incl. tax)"].mean()
    total_qty      = fdf["Quantity"].sum()
    avg_rating     = fdf["Rating"].mean()
    total_tax      = fdf["Tax 5%"].sum()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("💵 Total Revenue",    f"${total_sales:,.2f}")
    c2.metric("🧾 Total Orders",     f"{total_orders:,}")
    c3.metric("🛍️ Avg Order Value",  f"${avg_order:,.2f}")
    c4.metric("📦 Units Sold",       f"{total_qty:,}")
    c5.metric("⭐ Avg Rating",       f"{avg_rating:.2f} / 10")
    c6.metric("🏦 Total Tax (5%)",   f"${total_tax:,.2f}")

    st.markdown("---")

    # Monthly sales trend
    st.markdown('<p class="section-header">Monthly Revenue Trend</p>', unsafe_allow_html=True)
    monthly = (
        fdf.groupby("Month_num", as_index=False)["Total Sales (incl. tax)"]
        .sum()
        .sort_values("Month_num")
    )
    monthly.rename(columns={"Month_num": "Month", "Total Sales (incl. tax)": "Revenue"}, inplace=True)
    fig_trend = px.area(
        monthly, x="Month", y="Revenue",
        markers=True, template="plotly_white",
        color_discrete_sequence=["#4f8ef7"],
        labels={"Revenue": "Revenue ($)"},
    )
    fig_trend.update_traces(line_width=2.5)
    fig_trend.update_layout(margin=dict(t=10, b=10), height=320,
                             yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<p class="section-header">Sales by Branch</p>', unsafe_allow_html=True)
        branch_sales = fdf.groupby("Branch")["Total Sales (incl. tax)"].sum().reset_index()
        fig_b = px.bar(branch_sales, x="Branch", y="Total Sales (incl. tax)",
                       color="Branch", template="plotly_white",
                       color_discrete_sequence=px.colors.qualitative.Set2,
                       labels={"Total Sales (incl. tax)": "Revenue ($)"})
        fig_b.update_layout(margin=dict(t=10, b=10), height=300,
                             yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                             showlegend=False)
        st.plotly_chart(fig_b, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-header">Revenue by Payment Method</p>', unsafe_allow_html=True)
        pay_sales = fdf.groupby("Payment")["Total Sales (incl. tax)"].sum().reset_index()
        fig_p = px.pie(pay_sales, names="Payment", values="Total Sales (incl. tax)",
                       template="plotly_white", hole=0.45,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_p.update_layout(margin=dict(t=10, b=10), height=300)
        fig_p.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_p, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · DATA QUALITY
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-header">Step 2 — Data Quality Check</p>', unsafe_allow_html=True)

    original = pd.read_csv("SuperMarket Analysis.csv", encoding="utf-8-sig")
    original.columns = original.columns.str.strip()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📌 Dataset Shape")
        st.info(f"**{original.shape[0]:,} rows × {original.shape[1]} columns**")

        st.markdown("##### 🔢 Data Types")
        dtype_df = original.dtypes.reset_index()
        dtype_df.columns = ["Column", "Data Type"]
        dtype_df["Data Type"] = dtype_df["Data Type"].astype(str)
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("##### ❓ Missing Values per Column")
        missing = original.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing Count"]
        missing["Missing %"] = (missing["Missing Count"] / len(original) * 100).round(2)
        missing["Status"] = missing["Missing Count"].apply(
            lambda x: "✅ No Missing" if x == 0 else "⚠️ Has Missing"
        )
        st.dataframe(missing, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown("##### 🔁 Duplicate Rows")
    dupes = original.duplicated().sum()
    if dupes == 0:
        st.success(f"✅ No duplicate rows found.")
    else:
        st.warning(f"⚠️ {dupes} duplicate rows found and removed during load.")

    st.markdown("---")
    st.markdown("##### 📊 Descriptive Statistics")
    num_cols = ["Unit price", "Quantity", "Tax 5%", "Sales", "cogs", "gross income", "Rating"]
    available_cols = [c for c in num_cols if c in fdf.columns]
    stats = fdf[available_cols].describe().T.round(3)
    stats.index.name = "Column"
    st.dataframe(stats.reset_index(), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 📄 Raw Data Preview (first 20 rows)")
    st.dataframe(fdf.head(20), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · SALES ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-header">Step 3 & 4 — Computed Sales & Aggregations</p>', unsafe_allow_html=True)

    st.markdown(
        "Sales are computed as **Quantity × Unit Price**, plus a 5% tax. "
        "Aggregations below show totals, counts, and averages grouped by various dimensions."
    )

    # Computed Sales sample
    st.markdown("##### 🧮 Computed Sales Sample")
    sample_cols = ["Invoice ID", "Unit price", "Quantity", "Computed Sales",
                   "Total Sales (incl. tax)", "Tax 5%"]
    st.dataframe(fdf[sample_cols].head(10).round(2), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Aggregation tables ──────────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("##### 📊 Sales Summary by Branch")
        branch_agg = fdf.groupby("Branch").agg(
            Orders=("Invoice ID", "count"),
            Total_Revenue=("Total Sales (incl. tax)", "sum"),
            Avg_Order_Value=("Total Sales (incl. tax)", "mean"),
            Total_Qty=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        ).reset_index().round(2)
        branch_agg.rename(columns={
            "Total_Revenue": "Revenue ($)",
            "Avg_Order_Value": "Avg Order ($)",
            "Total_Qty": "Units Sold",
            "Avg_Rating": "Avg Rating",
        }, inplace=True)
        st.dataframe(branch_agg, use_container_width=True, hide_index=True)

        st.markdown("##### 📊 Sales Summary by Product Line")
        prod_agg = fdf.groupby("Product line").agg(
            Orders=("Invoice ID", "count"),
            Revenue=("Total Sales (incl. tax)", "sum"),
            Avg_Revenue=("Total Sales (incl. tax)", "mean"),
            Units_Sold=("Quantity", "sum"),
        ).reset_index().round(2)
        prod_agg.rename(columns={
            "Revenue": "Revenue ($)",
            "Avg_Revenue": "Avg Order ($)",
            "Units_Sold": "Units Sold",
        }, inplace=True)
        prod_agg_sorted = prod_agg.sort_values("Revenue ($)", ascending=False)
        st.dataframe(prod_agg_sorted, use_container_width=True, hide_index=True)

    with col_r:
        st.markdown("##### 📊 Sales Summary by City")
        city_agg = fdf.groupby("City").agg(
            Orders=("Invoice ID", "count"),
            Revenue=("Total Sales (incl. tax)", "sum"),
            Avg_Order=("Total Sales (incl. tax)", "mean"),
        ).reset_index().round(2)
        city_agg.rename(columns={
            "Revenue": "Revenue ($)",
            "Avg_Order": "Avg Order ($)",
        }, inplace=True)
        st.dataframe(city_agg, use_container_width=True, hide_index=True)

        st.markdown("##### 📊 Sales Summary by Payment Method")
        pay_agg = fdf.groupby("Payment").agg(
            Orders=("Invoice ID", "count"),
            Revenue=("Total Sales (incl. tax)", "sum"),
            Avg_Order=("Total Sales (incl. tax)", "mean"),
        ).reset_index().round(2)
        pay_agg.rename(columns={
            "Revenue": "Revenue ($)",
            "Avg_Order": "Avg Order ($)",
        }, inplace=True)
        st.dataframe(pay_agg, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Sales by hour heatmap ────────────────────────────────────────────────
    st.markdown('<p class="section-header">Hourly Sales Heatmap (Day of Week × Hour)</p>', unsafe_allow_html=True)
    heat_data = fdf.groupby(["Day of Week", "Hour"])["Total Sales (incl. tax)"].sum().reset_index()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_data["Day of Week"] = pd.Categorical(heat_data["Day of Week"], categories=day_order, ordered=True)
    heat_pivot = heat_data.pivot(index="Day of Week", columns="Hour", values="Total Sales (incl. tax)").fillna(0)
    fig_heat = px.imshow(
        heat_pivot,
        color_continuous_scale="Blues",
        template="plotly_white",
        labels={"x": "Hour of Day", "y": "Day of Week", "color": "Revenue ($)"},
        aspect="auto",
    )
    fig_heat.update_layout(margin=dict(t=10, b=10), height=300)
    st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · PRODUCT & BRANCH
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-header">Step 5 — Charts: Product Line & Branch Comparison</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📦 Revenue by Product Line")
        prod_rev = fdf.groupby("Product line")["Total Sales (incl. tax)"].sum().reset_index()
        prod_rev.sort_values("Total Sales (incl. tax)", ascending=True, inplace=True)
        fig_prod = px.bar(
            prod_rev, x="Total Sales (incl. tax)", y="Product line",
            orientation="h", template="plotly_white",
            color="Total Sales (incl. tax)",
            color_continuous_scale="Blues",
            labels={"Total Sales (incl. tax)": "Revenue ($)", "Product line": ""},
        )
        fig_prod.update_layout(margin=dict(t=10, b=10), height=340,
                                xaxis_tickprefix="$", xaxis_tickformat=",.0f",
                                coloraxis_showscale=False)
        st.plotly_chart(fig_prod, use_container_width=True)

    with col2:
        st.markdown("##### 📦 Units Sold by Product Line")
        prod_qty = fdf.groupby("Product line")["Quantity"].sum().reset_index()
        fig_qty = px.pie(
            prod_qty, names="Product line", values="Quantity",
            template="plotly_white", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_qty.update_traces(textinfo="percent+label")
        fig_qty.update_layout(margin=dict(t=10, b=10), height=340)
        st.plotly_chart(fig_qty, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### 🏪 Branch × Product Line Revenue")
        branch_prod = fdf.groupby(["Branch", "Product line"])["Total Sales (incl. tax)"].sum().reset_index()
        fig_bp = px.bar(
            branch_prod, x="Branch", y="Total Sales (incl. tax)",
            color="Product line", barmode="group",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"Total Sales (incl. tax)": "Revenue ($)"},
        )
        fig_bp.update_layout(margin=dict(t=10, b=10), height=360,
                              yaxis_tickprefix="$", yaxis_tickformat=",.0f")
        st.plotly_chart(fig_bp, use_container_width=True)

    with col4:
        st.markdown("##### ⭐ Avg Rating by Product Line")
        rating_prod = fdf.groupby("Product line")["Rating"].mean().reset_index().round(2)
        rating_prod.sort_values("Rating", ascending=False, inplace=True)
        fig_rat = px.bar(
            rating_prod, x="Rating", y="Product line",
            orientation="h", template="plotly_white",
            color="Rating", color_continuous_scale="RdYlGn",
            range_x=[0, 10],
            labels={"Product line": ""},
        )
        fig_rat.update_layout(margin=dict(t=10, b=10), height=360,
                               coloraxis_showscale=False)
        st.plotly_chart(fig_rat, use_container_width=True)

    st.markdown("---")

    st.markdown("##### 📅 Weekly Sales Pattern")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_sales = fdf.groupby("Day of Week")["Total Sales (incl. tax)"].sum().reset_index()
    dow_sales["Day of Week"] = pd.Categorical(dow_sales["Day of Week"],
                                               categories=day_order, ordered=True)
    dow_sales.sort_values("Day of Week", inplace=True)
    fig_dow = px.bar(
        dow_sales, x="Day of Week", y="Total Sales (incl. tax)",
        template="plotly_white", color="Total Sales (incl. tax)",
        color_continuous_scale="Teal",
        labels={"Total Sales (incl. tax)": "Revenue ($)", "Day of Week": ""},
    )
    fig_dow.update_layout(margin=dict(t=10, b=10), height=300,
                           yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                           coloraxis_showscale=False)
    st.plotly_chart(fig_dow, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · CUSTOMER INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-header">Customer Demographics & Behaviour</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 👤 Revenue: Member vs Normal")
        ctype_rev = fdf.groupby("Customer type")["Total Sales (incl. tax)"].sum().reset_index()
        fig_ct = px.pie(
            ctype_rev, names="Customer type", values="Total Sales (incl. tax)",
            template="plotly_white", hole=0.45,
            color_discrete_sequence=["#4f8ef7", "#f7a74f"],
        )
        fig_ct.update_traces(textinfo="percent+label")
        fig_ct.update_layout(margin=dict(t=10, b=10), height=300)
        st.plotly_chart(fig_ct, use_container_width=True)

    with col2:
        st.markdown("##### 🚻 Revenue by Gender")
        gender_rev = fdf.groupby("Gender")["Total Sales (incl. tax)"].sum().reset_index()
        fig_g = px.bar(
            gender_rev, x="Gender", y="Total Sales (incl. tax)",
            color="Gender", template="plotly_white",
            color_discrete_sequence=["#a78bfa", "#34d399"],
            labels={"Total Sales (incl. tax)": "Revenue ($)"},
        )
        fig_g.update_layout(margin=dict(t=10, b=10), height=300,
                             yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                             showlegend=False)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### 🛍️ Gender × Product Line Preference")
        gen_prod = fdf.groupby(["Gender", "Product line"])["Quantity"].sum().reset_index()
        fig_gp = px.bar(
            gen_prod, x="Quantity", y="Product line",
            color="Gender", barmode="group",
            orientation="h", template="plotly_white",
            color_discrete_sequence=["#a78bfa", "#34d399"],
            labels={"Product line": "", "Quantity": "Units Sold"},
        )
        fig_gp.update_layout(margin=dict(t=10, b=10), height=340)
        st.plotly_chart(fig_gp, use_container_width=True)

    with col4:
        st.markdown("##### 💳 Payment Method Split by Customer Type")
        pay_ct = fdf.groupby(["Customer type", "Payment"])["Invoice ID"].count().reset_index()
        pay_ct.rename(columns={"Invoice ID": "Count"}, inplace=True)
        fig_pct = px.bar(
            pay_ct, x="Customer type", y="Count",
            color="Payment", barmode="stack",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_pct.update_layout(margin=dict(t=10, b=10), height=340)
        st.plotly_chart(fig_pct, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 📈 Rating Distribution")
    fig_rat_hist = px.histogram(
        fdf, x="Rating", nbins=20,
        template="plotly_white",
        color_discrete_sequence=["#4f8ef7"],
        labels={"Rating": "Customer Rating", "count": "Frequency"},
    )
    fig_rat_hist.update_layout(margin=dict(t=10, b=10), height=280,
                                bargap=0.08)
    st.plotly_chart(fig_rat_hist, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 🔁 Gross Income by Customer Type & Product Line")
    gi_table = fdf.groupby(["Customer type", "Product line"]).agg(
        Total_Gross_Income=("gross income", "sum"),
        Avg_Gross_Income=("gross income", "mean"),
        Orders=("Invoice ID", "count"),
    ).reset_index().round(2)
    gi_table.rename(columns={
        "Total_Gross_Income": "Total Gross Income ($)",
        "Avg_Gross_Income": "Avg Gross Income ($)",
    }, inplace=True)
    st.dataframe(gi_table, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 · BUSINESS DECISIONS
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown('<p class="section-header">Step 6 — Data-Driven Business Decisions</p>', unsafe_allow_html=True)

    # ── Derive insights ──────────────────────────────────────────────────────
    top_product   = fdf.groupby("Product line")["Total Sales (incl. tax)"].sum().idxmax()
    low_product   = fdf.groupby("Product line")["Total Sales (incl. tax)"].sum().idxmin()
    top_branch    = fdf.groupby("Branch")["Total Sales (incl. tax)"].sum().idxmax()
    top_city      = fdf.groupby("City")["Total Sales (incl. tax)"].sum().idxmax()
    top_payment   = fdf.groupby("Payment")["Invoice ID"].count().idxmax()
    best_day      = (
        fdf.groupby("Day of Week")["Total Sales (incl. tax)"].sum()
        .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        .idxmax()
    )
    peak_hour_s   = fdf.groupby("Hour")["Total Sales (incl. tax)"].sum()
    peak_hour     = int(peak_hour_s.idxmax())
    top_gender    = fdf.groupby("Gender")["Total Sales (incl. tax)"].sum().idxmax()
    member_rev    = fdf[fdf["Customer type"] == "Member"]["Total Sales (incl. tax)"].sum()
    normal_rev    = fdf[fdf["Customer type"] == "Normal"]["Total Sales (incl. tax)"].sum()
    member_pct    = member_rev / (member_rev + normal_rev) * 100 if (member_rev + normal_rev) > 0 else 0
    avg_rat_prod  = fdf.groupby("Product line")["Rating"].mean()
    top_rated_p   = avg_rat_prod.idxmax()
    low_rated_p   = avg_rat_prod.idxmin()

    insights = [
        {
            "icon": "🏆",
            "title": "Top-Performing Product Line",
            "finding": f"**{top_product}** generates the highest revenue.",
            "action": f"Increase inventory and promote **{top_product}** through targeted campaigns. "
                      f"Consider bundling with **{low_product}** to uplift its sales.",
        },
        {
            "icon": "🏪",
            "title": "Best Performing Branch & City",
            "finding": f"Branch **{top_branch}** in **{top_city}** leads in total revenue.",
            "action": "Replicate successful practices (staffing, layout, promotions) from "
                      f"**{top_branch}** to underperforming branches.",
        },
        {
            "icon": "💳",
            "title": "Preferred Payment Method",
            "finding": f"**{top_payment}** is the most used payment method.",
            "action": f"Offer exclusive cashback or loyalty points for **{top_payment}** transactions "
                      "to further incentivise the preferred channel.",
        },
        {
            "icon": "📅",
            "title": "Peak Shopping Day & Hour",
            "finding": f"**{best_day}** is the busiest day; peak hour is **{peak_hour}:00–{peak_hour+1}:00**.",
            "action": "Schedule additional staff and flash sales during peak periods. "
                      "Run promotions on slow days to even out foot traffic.",
        },
        {
            "icon": "👥",
            "title": "Customer Loyalty Programme",
            "finding": f"Members account for **{member_pct:.1f}%** of revenue.",
            "action": "Launch a membership drive targeting Normal customers with sign-up discounts. "
                      "Reward existing Members with tier upgrades to boost retention.",
        },
        {
            "icon": "⭐",
            "title": "Customer Satisfaction",
            "finding": f"**{top_rated_p}** is the highest-rated product line; "
                       f"**{low_rated_p}** has the lowest average rating.",
            "action": f"Investigate service quality issues in **{low_rated_p}** — "
                      "gather customer feedback and retrain staff for those aisles.",
        },
        {
            "icon": "🚻",
            "title": "Gender-Based Marketing",
            "finding": f"**{top_gender}** customers contribute slightly more to total revenue.",
            "action": "Tailor promotions to each gender segment's top product preferences "
                      "(visible from the Product line preference chart).",
        },
        {
            "icon": "📦",
            "title": "Low-Performing Product Line",
            "finding": f"**{low_product}** has the lowest revenue contribution.",
            "action": f"Run targeted discount campaigns or cross-promotions for **{low_product}**. "
                      "Analyse whether pricing, placement, or stock availability is the root cause.",
        },
    ]

    for ins in insights:
        with st.expander(f"{ins['icon']} {ins['title']}", expanded=True):
            st.markdown(f"**📌 Finding:** {ins['finding']}")
            st.markdown(f"**✅ Recommended Action:** {ins['action']}")

    st.markdown("---")

    # ── Summary comparison chart ─────────────────────────────────────────────
    st.markdown('<p class="section-header">Revenue Share by All Dimensions</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### Product Line vs Branch Revenue")
        fig_sum = px.sunburst(
            fdf, path=["Branch", "Product line"],
            values="Total Sales (incl. tax)",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_sum.update_layout(margin=dict(t=10, b=10), height=400)
        st.plotly_chart(fig_sum, use_container_width=True)

    with col_b:
        st.markdown("##### Revenue by City, Gender & Payment")
        fig_sun2 = px.sunburst(
            fdf, path=["City", "Gender", "Payment"],
            values="Total Sales (incl. tax)",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_sun2.update_layout(margin=dict(t=10, b=10), height=400)
        st.plotly_chart(fig_sun2, use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        <div style="background:#f0f4ff;padding:16px 20px;border-radius:10px;
                    border-left:4px solid #4f8ef7;font-size:0.93rem;color:#1a2133;">
        <strong>📋 Summary:</strong> This analysis covered 6 analytical steps —
        data collection &amp; loading, data quality verification, sales computation,
        grouped aggregations, visual comparisons, and business decision making.
        All insights are dynamically derived from the filtered dataset and update
        automatically when sidebar filters change.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#8a94a6;font-size:0.8rem;'>"
    "🛒 Supermarket Sales Analytics Dashboard &nbsp;|&nbsp; Built with Streamlit &amp; Plotly"
    "</p>",
    unsafe_allow_html=True,
)
