# 🛒 Supermarket Sales Analysis Dashboard

> An interactive, end-to-end data analytics dashboard built with **Python**, **Streamlit**, and **Plotly** that transforms raw supermarket transaction data into actionable business intelligence through dynamic visualisations, KPI cards, and auto-generated insights.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Objectives](#project-objectives)
3. [Key Features](#key-features)
4. [Analysis Workflow](#analysis-workflow)
5. [Dataset](#dataset)
6. [Technology Stack](#technology-stack)
7. [Project Structure](#project-structure)
8. [Dashboard Interface](#dashboard-interface)
9. [KPI Metrics](#kpi-metrics)
10. [Visualisations](#visualisations)
11. [Data Quality Process](#data-quality-process)
12. [Business Insights](#business-insights)
13. [Installation and Setup](#installation-and-setup)
14. [Running the Application](#running-the-application)
15. [Complete End-to-End Guide](#complete-end-to-end-guide)
16. [Troubleshooting](#troubleshooting)
17. [Data Analysis Methodology](#data-analysis-methodology)
18. [Dataset Results (Verified)](#dataset-results-verified)
19. [Screenshots](#screenshots)
20. [Future Enhancements](#future-enhancements)
21. [Learning Outcomes](#learning-outcomes)
22. [License](#license)

---

## Project Overview

This project performs a complete data analytics cycle on a supermarket sales dataset covering **1,000 transactions** across three branches and six product categories. The pipeline spans every stage of the analytics workflow — from raw CSV ingestion and data quality validation through computed sales metrics, grouped aggregations, interactive charts, and auto-derived business recommendations.

The deliverable is a **Streamlit web dashboard** that runs locally in a browser. Business users can apply real-time filters (branch, city, product line, gender, customer type, payment method, date range) and the entire dashboard — every KPI card, chart, aggregation table, and insight — updates instantly without reloading.

**Why this project?**  
Retail businesses generate large volumes of transactional data that is difficult to interpret in raw form. This dashboard makes that data immediately readable, allowing non-technical stakeholders to answer questions like: *Which product line drives the most revenue? Which branch needs attention? When are peak shopping hours?* — without writing a single line of SQL or Python.

---

## Project Objectives

1. Load and process `SuperMarket Analysis.csv` into a clean analytical pipeline.
2. Validate data quality — detect missing values, duplicate records, and type inconsistencies.
3. Compute sales using the formula:
   ```
   Computed Sales = Quantity × Unit Price
   Total Sales (incl. tax) = Computed Sales × 1.05
   ```
4. Perform grouped statistical aggregations (totals, counts, averages) across multiple dimensions.
5. Build interactive Plotly visualisations covering trends, distributions, and comparisons.
6. Deliver an interactive Streamlit dashboard with sidebar filters.
7. Auto-generate data-driven business recommendations from the filtered dataset.

---

## Key Features

| Feature | Description |
|---|---|
| **6-Tab Dashboard** | Overview, Data Quality, Sales Analysis, Product & Branch, Customer Insights, Business Decisions |
| **7 Sidebar Filters** | Branch, City, Product Line, Gender, Customer Type, Payment Method, Date Range |
| **6 KPI Cards** | Total Revenue, Total Orders, Avg Order Value, Units Sold, Avg Rating, Total Tax |
| **Real-Time Filtering** | All charts, tables and KPIs update instantly on filter change |
| **Sales Computation** | `Quantity × Unit Price` computed and displayed with 5% tax |
| **Data Quality Tab** | Missing value report, duplicate check, data type table, descriptive statistics |
| **Aggregation Tables** | Branch, City, Product Line, Payment — with totals, averages and counts |
| **Hourly Heatmap** | Day-of-week × hour revenue heatmap identifying peak trading windows |
| **Product Analysis** | Revenue bar, units-sold pie, grouped branch cross-tab, rating bar |
| **Customer Analysis** | Member vs Normal donut, gender bar, product preference, payment split, rating histogram |
| **Business Insights** | 8 auto-computed findings each with a recommended action |
| **Sunburst Charts** | Hierarchical drill-down: Branch → Product Line; City → Gender → Payment |
| **Raw Data Preview** | First 20 rows of the filtered dataset in Data Quality tab |
| **Responsive Layout** | Wide layout with dark sidebar and custom CSS metric cards |

---

## Analysis Workflow

### Step 1 — Data Collection and Loading

`SuperMarket Analysis.csv` is loaded via `pandas.read_csv()` with `encoding="utf-8-sig"` to handle the UTF-8 Byte Order Mark. Column names are stripped of whitespace. Results are cached with `@st.cache_data` so the file is only read once per session.

```python
df = pd.read_csv("SuperMarket Analysis.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
```

### Step 2 — Data Validation and Cleaning

The following checks are applied automatically at load time:

- **Duplicate rows** — removed with `df.drop_duplicates()`
- **Missing values** — rows missing `Unit price` or `Quantity` are dropped
- **Type coercion** — `Unit price`, `Quantity`, `Tax 5%`, `Sales`, `cogs`, `gross income`, and `Rating` are converted to numeric with `pd.to_numeric(errors="coerce")`
- **Date parsing** — `Date` column parsed to `datetime` with `pd.to_datetime(errors="coerce")`
- **Time parsing** — `Time` column parsed to extract the `Hour` integer for heatmap analysis

The **Data Quality tab** surfaces the pre-cleaning state of the original file (shape, dtypes, missing counts, duplicate count) so users can see what the raw data looked like before processing.

### Step 3 — Sales Calculation

Two computed columns are added:

```python
df["Computed Sales"]            = df["Quantity"] * df["Unit price"]
df["Total Sales (incl. tax)"]   = df["Computed Sales"] * 1.05
```

`Computed Sales` represents pre-tax unit economics. `Total Sales (incl. tax)` is the final billable amount used as the primary revenue metric throughout all charts and aggregations.

### Step 4 — Data Aggregation

Data is grouped across six dimensions producing totals, order counts, and averages:

| Dimension | Metrics |
|---|---|
| Branch | Revenue, Orders, Units Sold, Avg Order Value, Avg Rating |
| City | Revenue, Orders, Avg Order Value |
| Product Line | Revenue, Orders, Units Sold, Avg Order Value |
| Payment Method | Revenue, Orders, Avg Order Value |
| Day of Week | Revenue total |
| Hour × Day | Revenue total (heatmap) |

### Step 5 — Visualisation

Twelve interactive Plotly charts render within the dashboard tabs. Each chart supports hover tooltips, zoom, and pan. All charts respond to sidebar filters.

### Step 6 — Business Insights

Eight insights are computed dynamically from the filtered dataset. Each identifies the top/bottom performer on a specific dimension and pairs it with a concrete recommended action. Insight text updates automatically when filters change.

---

## Dataset

**File:** `SuperMarket Analysis.csv`  
**Records:** 1,000 transactions  
**Period:** January 2019 – March 2019  
**Branches:** Alex, Cairo, Giza (one per city)

### Column Reference

| Column | Data Type | Description |
|---|---|---|
| `Invoice ID` | String | Unique transaction identifier |
| `Branch` | String | Branch code — Alex, Cairo, or Giza |
| `City` | String | City of the branch (Yangon, Mandalay, Naypyitaw) |
| `Customer type` | String | `Member` (loyalty card holder) or `Normal` |
| `Gender` | String | Customer gender — `Male` or `Female` |
| `Product line` | String | One of six product categories |
| `Unit price` | Float | Price per unit in USD |
| `Quantity` | Integer | Number of units purchased (1–10) |
| `Tax 5%` | Float | 5% tax on the cost of goods |
| `Sales` | Float | Total amount paid including tax (from source) |
| `Date` | Date | Date of purchase (M/D/YYYY) |
| `Time` | Time | Time of purchase (H:MM:SS AM/PM) |
| `Payment` | String | `Cash`, `Ewallet`, or `Credit card` |
| `cogs` | Float | Cost of goods sold |
| `gross margin percentage` | Float | Fixed at 4.761904762% for all rows |
| `gross income` | Float | Gross profit per transaction |
| `Rating` | Float | Customer satisfaction score (1.0–10.0) |

**Computed columns added by the application:**

| Column | Formula |
|---|---|
| `Computed Sales` | `Quantity × Unit price` |
| `Total Sales (incl. tax)` | `Computed Sales × 1.05` |
| `Month` | Formatted as `"Jan 2019"` etc. |
| `Month_num` | ISO period string `"2019-01"` for sorting |
| `Day of Week` | Weekday name derived from `Date` |
| `Hour` | Integer hour extracted from `Time` |

**Product line categories:**

- Electronic accessories
- Fashion accessories
- Food and beverages
- Health and beauty
- Home and lifestyle
- Sports and travel

---

## Technology Stack

| Technology | Version | Role |
|---|---|---|
| **Python** | 3.11+ | Core language |
| **Streamlit** | ≥ 1.32.0 | Web dashboard framework |
| **Pandas** | ≥ 2.0.0 | Data loading, cleaning, aggregation |
| **Plotly** | ≥ 5.18.0 | Interactive charts (Express + Graph Objects) |

> **Note:** NumPy, Matplotlib, and Seaborn are **not** used in this project. Only the three libraries above are required (see `requirements.txt`).

---

## Project Structure

```text
supermarket-sales-analysis/
│
├── app.py                              # Main Streamlit application (single file)
├── SuperMarket Analysis.csv            # Source dataset — must be in project root
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
│
├── assets/
│   └── screenshots/                    # Dashboard screenshots (referenced in README)
│       ├── 01_overview_kpis.png
│       ├── 02_data_quality.png
│       ├── 03_sales_top.png
│       ├── 04_product_top.png
│       ├── 05_customer_top.png
│       ├── 06_biz_top.png
│       ├── 07_sidebar.png
│       └── 08_full_dashboard.png
│
├── Supermarket_Sales_Analysis_Report.docx   # Formal project report
├── capture_screenshots.py              # Developer utility — screenshot automation
└── inject_screenshots.py               # Developer utility — report image injection
```

**File purposes:**

- **`app.py`** — The entire application. Contains data loading, cleaning, computed columns, sidebar, six tabs with all charts and tables, and auto-generated business insights. ~730 lines.
- **`SuperMarket Analysis.csv`** — Must be present in the same directory as `app.py`. The application reads it at startup.
- **`requirements.txt`** — Three dependencies: `streamlit`, `pandas`, `plotly`.

---

## Dashboard Interface

The dashboard uses Streamlit's wide layout with a dark navy sidebar (`#1a2133`) and a light grey main area (`#f5f7fa`). Custom CSS styles the metric cards with rounded borders and shadows.

### Sidebar — Real-Time Filters

The sidebar contains seven independent filters. Selecting any value instantly recomputes every KPI, chart, and table on the current tab.

| Filter | Options |
|---|---|
| Branch | All, Alex, Cairo, Giza |
| City | All, Mandalay, Naypyitaw, Yangon |
| Product Line | All + 6 categories |
| Gender | All, Female, Male |
| Customer Type | All, Member, Normal |
| Payment Method | All, Cash, Credit card, Ewallet |
| Date Range | Date picker — defaults to full dataset range |

### Tab 1 — Overview (`📋 Overview`)

Entry point of the dashboard. Shows the six KPI cards, a monthly revenue area chart, a branch revenue bar chart, and a payment method donut chart.

### Tab 2 — Data Quality (`🔎 Data Quality`)

Displays: dataset shape, column data types, missing value counts per column with status flags, duplicate row count, descriptive statistics table (count/mean/std/min/max/quartiles), and a raw data preview (first 20 rows of the filtered dataset).

### Tab 3 — Sales Analysis (`💰 Sales Analysis`)

Shows: computed sales sample table (Invoice ID, Unit price, Quantity, Computed Sales, Total Sales incl. tax), four aggregation tables (by Branch, Product Line, City, Payment Method), and an hourly sales heatmap (day-of-week × hour).

### Tab 4 — Product & Branch (`📦 Product & Branch`)

Contains: horizontal revenue bar chart by product line, units-sold donut chart, Branch × Product Line grouped bar chart, average rating bar chart (Red-Yellow-Green colour scale), and a weekly sales pattern bar chart.

### Tab 5 — Customer Insights (`👥 Customer Insights`)

Contains: Member vs Normal revenue donut, gender revenue bar chart, Gender × Product Line preference grouped bar, Payment Method stacked bar by customer type, rating distribution histogram, and a Gross Income cross-table by Customer Type × Product Line.

### Tab 6 — Business Decisions (`💡 Business Decisions`)

Contains: 8 expandable insight cards (each auto-computed from the filtered data with a finding and recommended action), two Plotly sunburst charts (Branch → Product Line; City → Gender → Payment), and a methodology summary callout.

---

## KPI Metrics

All six KPI cards are calculated from the **filtered** dataset and update whenever a sidebar filter changes.

| KPI | Calculation |
|---|---|
| **Total Revenue** | `sum(Quantity × Unit price × 1.05)` |
| **Total Orders** | `count(Invoice ID)` |
| **Avg Order Value** | `mean(Total Sales incl. tax)` |
| **Units Sold** | `sum(Quantity)` |
| **Avg Rating** | `mean(Rating)` |
| **Total Tax (5%)** | `sum(Tax 5%)` |

---

## Visualisations

| # | Chart | Type | Tab | What It Shows |
|---|---|---|---|---|
| 1 | Monthly Revenue Trend | Area chart | Overview | Revenue per calendar month with markers |
| 2 | Sales by Branch | Bar chart | Overview | Total revenue per branch, colour-coded |
| 3 | Revenue by Payment Method | Donut pie | Overview | Revenue share by Cash / Ewallet / Credit card |
| 4 | Revenue by Product Line | Horizontal bar (Blues scale) | Product & Branch | Revenue per category sorted ascending |
| 5 | Units Sold by Product Line | Donut pie | Product & Branch | Unit volume share per category |
| 6 | Branch × Product Line Revenue | Grouped bar | Product & Branch | Cross-tab: each branch's revenue per category |
| 7 | Avg Rating by Product Line | Horizontal bar (RdYlGn) | Product & Branch | Mean customer rating per category |
| 8 | Weekly Sales Pattern | Bar chart (Teal scale) | Product & Branch | Revenue per day of week Mon–Sun |
| 9 | Hourly Sales Heatmap | Heatmap (imshow) | Sales Analysis | Revenue intensity by hour of day × day of week |
| 10 | Revenue by Gender | Bar chart | Customer Insights | Male vs Female total revenue |
| 11 | Revenue: Member vs Normal | Donut pie | Customer Insights | Customer type revenue split |
| 12 | Gender × Product Line Preference | Grouped horizontal bar | Customer Insights | Units sold per category split by gender |
| 13 | Payment Split by Customer Type | Stacked bar | Customer Insights | Payment method distribution for Members vs Normals |
| 14 | Rating Distribution | Histogram (20 bins) | Customer Insights | Frequency distribution of customer ratings |
| 15 | Sunburst — Branch → Product | Sunburst | Business Decisions | Hierarchical revenue: branch contains product lines |
| 16 | Sunburst — City → Gender → Payment | Sunburst | Business Decisions | Hierarchical revenue: city → gender → payment method |

---

## Data Quality Process

The application performs the following checks at load time and surfaces results in the Data Quality tab:

| Check | Method | Result on this dataset |
|---|---|---|
| Missing values | `df.isnull().sum()` | **0 missing** in all 17 columns |
| Duplicate rows | `df.duplicated().sum()` | **0 duplicates** found |
| Numeric type validation | `pd.to_numeric(errors="coerce")` | All 7 numeric columns valid |
| Date parsing | `pd.to_datetime(errors="coerce")` | All 1,000 dates parsed successfully |
| Time parsing | `pd.to_datetime(format="%I:%M:%S %p")` | All times parsed to integer hours |

The dataset is clean in its original form. All cleaning operations are applied defensively and would handle real-world data issues should the dataset be replaced or updated.

---

## Business Insights

The Business Decisions tab auto-computes eight insights from the **currently filtered** data. Below are the verified results for the full unfiltered dataset:

| Insight | Finding | Recommended Action |
|---|---|---|
| **Top Product Line** | Food and Beverages — highest revenue | Increase inventory; bundle with Health and Beauty |
| **Best Branch** | Giza leads revenue | Audit Giza practices; replicate to Alex and Cairo |
| **Payment Preference** | Cash is most used | Incentivise Ewallet with cashback to cut cash-handling costs |
| **Peak Day** | Saturday is busiest day | Max staffing on Saturdays; Monday promotions for slow days |
| **Peak Hour** | 19:00–20:00 generates highest hourly revenue | Flash sales at 7 PM; additional checkout staff |
| **Loyalty Programme** | Members drive 58.7% of revenue | Membership drive with sign-up discounts; tier upgrades |
| **Customer Satisfaction** | Food and Beverages rated highest; Home and Lifestyle lowest | Investigate Home and Lifestyle service issues |
| **Gender Revenue** | Female customers contribute the larger share | Gender-targeted campaigns; initiatives to grow male engagement |

> All insight text in the dashboard is dynamic — it recalculates and rewrites itself automatically when filters change.

---

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- `pip` package manager

Verify your Python installation:

```bash
python --version
```

### Clone the Repository

```bash
git clone <repository-url>
cd supermarket-sales-analysis
```

### Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit >= 1.32.0`
- `pandas >= 2.0.0`
- `plotly >= 5.18.0`

---

## Running the Application

Ensure `SuperMarket Analysis.csv` is in the **same directory** as `app.py`, then run:

```bash
streamlit run app.py
```

Streamlit will print output similar to:

```
  You can now view your Streamlit app in your browser.

  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser. The dashboard loads, renders all six tabs, and is ready for interaction.

> If port 8501 is already in use, specify a different port:
> ```bash
> streamlit run app.py --server.port 8502
> ```

---

## Complete End-to-End Guide

Follow these steps from a completely fresh environment to a running dashboard.

### 1. Install Python

Download and install Python 3.11+ from [python.org](https://www.python.org/downloads/).  
During installation on Windows, check **"Add Python to PATH"**.

### 2. Download or Clone the Project

```bash
git clone <repository-url>
cd supermarket-sales-analysis
```

Or download the ZIP from GitHub and extract it.

### 3. Verify the Dataset is Present

Check that `SuperMarket Analysis.csv` exists in the project root:

```bash
# Windows
dir "SuperMarket Analysis.csv"

# macOS / Linux
ls "SuperMarket Analysis.csv"
```

### 4. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output ends with something like:
```
Successfully installed streamlit-x.x.x pandas-x.x.x plotly-x.x.x ...
```

### 6. Verify Required Files

```bash
# Windows
dir app.py requirements.txt "SuperMarket Analysis.csv"

# macOS / Linux
ls app.py requirements.txt "SuperMarket Analysis.csv"
```

All three files must be present.

### 7. Start the Dashboard

```bash
streamlit run app.py
```

### 8. Open in Browser

Navigate to `http://localhost:8501`.  
The dashboard title **🛒 Supermarket Sales Analysis Dashboard** should be visible with all six tabs loaded.

### 9. Explore the Dashboard

- Use the **sidebar filters** to narrow by branch, city, product line, gender, customer type, payment method, or date range.
- Click each tab to navigate between: Overview → Data Quality → Sales Analysis → Product & Branch → Customer Insights → Business Decisions.
- Hover over any chart to see precise values.
- The Business Decisions tab updates all eight insights to reflect the filtered selection.

### 10. Stop the Application

Press `Ctrl+C` in the terminal to stop the Streamlit server.

---

## Example Terminal Session

```bash
# Clone and navigate
git clone <repository-url>
cd supermarket-sales-analysis

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Troubleshooting

### `python` is not recognised

Verify Python is installed and on your PATH:
```bash
python --version
# or try:
python3 --version
```
If missing, reinstall Python and check "Add to PATH" during setup.

### `pip` is not recognised

Try:
```bash
python -m pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'streamlit'`

The virtual environment may not be activated, or dependencies were not installed:
```bash
pip install -r requirements.txt
```

### `FileNotFoundError: SuperMarket Analysis.csv`

The dataset must be in the **same directory as `app.py`**. Check its location:
```bash
# Windows
dir "SuperMarket Analysis.csv"
```
If missing, place the CSV in the project root folder.

### `streamlit: command not found`

Run Streamlit as a Python module:
```bash
python -m streamlit run app.py
```

### Port 8501 is already in use

Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Dashboard loads but shows a warning — "No data matches selected filters"

A sidebar filter combination returned zero rows. Reset filters to **"All"** values and set the date range back to the full dataset range.

---

## Data Analysis Methodology

The project follows the standard data analytics lifecycle:

| Stage | Implementation |
|---|---|
| **Ingestion** | `pd.read_csv()` with UTF-8 BOM handling |
| **Cleaning** | Deduplication, null-drop on key columns, type coercion |
| **Transformation** | Computed Sales column, Date → Month/Day/Hour features |
| **Aggregation** | `groupby().agg()` across six dimensions |
| **EDA** | Descriptive statistics, missing value analysis |
| **Visualisation** | 16 Plotly charts across five dashboard tabs |
| **Insight Generation** | Dynamic text computed from `idxmax()` / `idxmin()` on filtered data |

**Core formula:**
```
Computed Sales            = Quantity × Unit Price
Total Sales (incl. tax)   = Computed Sales × 1.05
```

All analytics operate on the **filtered** dataframe `fdf`, not the original raw data. This means every KPI, chart, and insight reflects only the records that pass the active sidebar filters.

---

## Dataset Results (Verified)

The following values are computed from the complete unfiltered dataset (`SuperMarket Analysis.csv`, 1,000 records):

```
Total Revenue (incl. 5% tax)  :  $322,966.75
Total Orders                  :  1,000
Average Order Value           :  $322.97
Total Units Sold              :  5,510
Average Customer Rating       :  6.97 / 10
Total Tax Collected (5%)      :  $15,379.37

Revenue by Branch:
  Giza    $110,568.71  (34.2%)
  Alex    $106,200.37  (32.9%)
  Cairo   $106,197.67  (32.9%)

Top Product Line by Revenue:
  Food and Beverages      $56,144.84
  Sports and Travel       $55,122.83
  Electronic Accessories  $54,337.53
  Fashion Accessories     $54,305.90
  Home and Lifestyle      $53,861.91
  Health and Beauty       $49,193.74  (lowest)

Revenue by Month:
  January 2019    $116,291.87  (36.0%)
  March   2019    $109,455.51  (33.9%)
  February 2019   $97,219.37   (30.1%)

Peak Day:   Saturday   $56,120.81
Slowest Day: Monday    $37,899.08
Peak Hour:  19:00–20:00
```

> These figures are calculated dynamically when the dashboard runs. They will change if filters are applied.
<!-- 
---

## Screenshots

All screenshots below are taken from the **live running Streamlit application** at 1440×900 resolution using headless Chrome.

---

### Dashboard Overview — KPI Cards & Revenue Trend

The entry tab showing all six KPI cards, the monthly revenue area chart, the branch revenue bar chart, and the payment method donut.

![Dashboard Overview — KPIs and Monthly Revenue Trend](assets/screenshots/01_overview_kpis.png)

---

### Data Quality Tab

Missing value analysis, column data types, duplicate detection, descriptive statistics, and raw data preview (first 20 rows).

![Data Quality — Missing value table, data types, statistics](assets/screenshots/02_data_quality.png)

---

### Sales Analysis Tab — Computed Sales & Aggregation Tables

Computed Sales sample showing `Quantity × Unit Price`, plus aggregation tables grouped by Branch, Product Line, City, and Payment Method.

![Sales Analysis — Computed sales and aggregation tables](assets/screenshots/03_sales_top.png)

---

### Product & Branch Tab — Charts

Revenue by product line (horizontal bar), units sold (donut), Branch × Product Line grouped bar, average rating (RdYlGn), and weekly sales pattern.

![Product and Branch — Revenue charts and cross-tab analysis](assets/screenshots/04_product_top.png)

---

### Customer Insights Tab

Member vs Normal revenue donut, gender revenue bar, product preference by gender, payment method split, rating distribution histogram, and gross income cross-table.

![Customer Insights — Demographics and behaviour analysis](assets/screenshots/05_customer_top.png)

---

### Business Decisions Tab — Auto-Generated Insights

Eight expandable insight cards, each dynamically computed from the filtered dataset, with a finding and a concrete recommended action.

![Business Decisions — Auto-derived insights with recommendations](assets/screenshots/06_biz_top.png)

---

### Sidebar Filters

The dark navy sidebar with seven real-time dropdown and date-range filters.

![Sidebar — Real-time filter panel](assets/screenshots/07_sidebar.png)

---

### Full Dashboard View

Wide-layout full-page view showing the sidebar, header, KPI cards, and tab navigation together.

![Full Dashboard View](assets/screenshots/08_full_dashboard.png)

--- -->

## Future Enhancements

The following are potential improvements not present in the current version:

- **Predictive Sales Forecasting** — Time-series models (ARIMA, Prophet) to predict future monthly revenue
- **Customer Segmentation** — K-means clustering on purchasing behaviour to identify customer personas
- **Automated Reporting** — Scheduled PDF/Word report generation with `python-docx` or `reportlab`
- **Machine Learning** — Product recommendation engine based on purchase history
- **Streamlit Cloud Deployment** — One-click public deployment at `streamlit.io/cloud`
- **Database Integration** — Replace CSV with a live PostgreSQL or SQLite database connection
- **Anomaly Detection** — Flag unusual transactions (outlier revenue, abnormal quantities)
- **Multi-Store Comparison** — Support for multiple CSV files representing different store periods
- **CSV Download** — Filtered dataset download button using `st.download_button`
- **User Authentication** — Login layer using `streamlit-authenticator` for multi-user access

---

## Learning Outcomes

This project demonstrates the following technical competencies:

- **Python Programming** — Pandas DataFrames, list comprehensions, lambda functions, caching decorators
- **Data Cleaning** — Deduplication, null handling, type coercion, feature engineering
- **Exploratory Data Analysis** — Descriptive statistics, distribution analysis, group-by aggregations
- **Data Visualisation** — 16 Plotly chart types including area, bar, pie, donut, heatmap, histogram, sunburst
- **Streamlit Development** — Multi-tab layout, sidebar filters, metric cards, custom CSS injection
- **Dashboard Design** — KPI card layout, responsive wide mode, consistent colour palette
- **Business Analytics** — Translating numerical findings into actionable retail recommendations
- **Data-Driven Decision Making** — Dynamic insight generation from live filtered data
- **Software Engineering** — Clean single-file architecture with caching, defensive data handling

---

## License

No license file is currently included in this repository. The repository owner may add an appropriate open-source license (e.g., MIT, Apache 2.0) at their discretion.

---

## Author

This project was developed as part of the **Data Analytics with AI** internship programme at **IBM**.

For questions or contributions, please open an issue or pull request on the repository.

---

<p align="center">
  Built with Python · Streamlit · Plotly &nbsp;|&nbsp; IBM Data Analytics with AI Internship
</p>
