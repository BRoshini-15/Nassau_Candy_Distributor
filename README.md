# 🍬 Nassau Candy Distributor: Route Efficiency & Distribution Analytics Dashboard

An interactive **Streamlit** dashboard that analyzes sales, profitability, products, factories, customer regions, and factory-to-customer distribution routes for **Nassau Candy Distributor**. Built as part of a **Data Science Internship** project.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)

---

## 📌 Table of Contents

- [🍬 Nassau Candy Distributor: Route Efficiency \& Distribution Analytics Dashboard](#-nassau-candy-distributor-route-efficiency--distribution-analytics-dashboard)
  - [📌 Table of Contents](#-table-of-contents)
  - [📖 Project Overview](#-project-overview)
  - [🎯 Business Objectives](#-business-objectives)
  - [✨ Key Features](#-key-features)
  - [🧭 Dashboard Pages](#-dashboard-pages)
  - [🛠 Tech Stack](#-tech-stack)
  - [📂 Project Structure](#-project-structure)
  - [🗃 Dataset \& Required Files](#-dataset--required-files)
    - [Expected columns in `Nassau_Candy_Cleaned.csv`](#expected-columns-in-nassau_candy_cleanedcsv)
  - [⚙️ Installation \& Setup](#️-installation--setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. (Optional) Create a virtual environment](#2-optional-create-a-virtual-environment)
    - [3. Install dependencies](#3-install-dependencies)
    - [4. Add the data files](#4-add-the-data-files)
  - [▶️ Usage](#️-usage)
  - [📊 Key Metrics](#-key-metrics)
  - [⚠️ Data Quality Note](#️-data-quality-note)
  - [👩‍💻 Author](#-author)

---

## 📖 Project Overview

Nassau Candy Distributor ships products from multiple factories to customers across US regions and states. This project turns the cleaned order and shipment data into an interactive analytics dashboard that helps stakeholders:

- Monitor overall **sales, profit, and shipment volume**
- Compare **factory-to-region routes** by volume, lead time, and profitability
- Identify **geographic patterns** and states with long calculated shipping gaps
- Evaluate **shipping modes** by volume, sales, and lead time
- Drill down into **individual orders** and export the results

The analysis pipeline first cleans the raw data and generates supporting CSV files (route, factory, and state-level analyses). The Streamlit app (`app.py`) then loads these files and provides a filterable, multi-page dashboard.

---

## 🎯 Business Objectives

1. Measure the **efficiency of distribution routes** from factories to customer regions.
2. Identify **top-performing products, factories, and states** by sales and gross profit.
3. Detect **potential shipping bottlenecks** by region and state.
4. Compare **ship modes** in terms of volume, sales, and calculated lead time.
5. Provide a **self-service, filter-driven tool** for decision makers.

---

## ✨ Key Features

- **Global sidebar filters** for Factory, Region, Ship Mode, and Product that apply across every page
- **Six dashboard pages** reachable from sidebar navigation
- **Interactive Plotly charts** with hover details: bar charts, scatter plots, box plots, and a US choropleth map
- **KPI cards** for sales, gross profit, orders, units, profit margin, and average lead time
- **Downloadable CSV exports** of the filtered route analysis and order-level data
- **Cached data loading** with `@st.cache_data` for fast performance
- **Graceful error handling** with a clear message if required CSV files are missing
- **Custom styling** and a wide-layout UI

---

## 🧭 Dashboard Pages

| Page | Description |
|------|-------------|
| **Executive Dashboard** | KPIs (sales, gross profit, orders, units, profit margin, average lead time), Top 10 products by sales, sales by region, and gross profit by factory |
| **Route Efficiency** | Factory × Region route analysis with a scatter plot of route volume vs. calculated lead time (bubble size = sales), a route performance table, and CSV download |
| **Geographic Analysis** | Top 15 states by sales, states with the longest average calculated date gap, a US choropleth sales map, and a state-level analysis table |
| **Shipping Analysis** | Shipment volume, average lead time, and sales by ship mode, a lead-time box plot, and a ship mode summary table |
| **Product & Factory Analysis** | Top products by sales and gross profit, a factory performance table (shipments, orders, units, sales, cost, profit, lead time, margin), and sales by factory |
| **Order Drill-Down** | Select a specific Order ID (or view all), see order-level metrics and shipment records, and download the data as CSV |

---

## 🛠 Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Dashboard Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |

---

## 📂 Project Structure

```
nassau-candy-analytics/
│
├── app.py                              # Streamlit dashboard application
├── Nassau_Candy_Cleaned.csv            # Cleaned order/shipment dataset
├── Route_Analysis.csv                  # Route-level analysis output
├── Factory_Analysis.csv                # Factory-level analysis output
├── State_Bottleneck_Analysis.csv       # State-level bottleneck analysis output
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

---

## 🗃 Dataset & Required Files

The app expects the following CSV files in the **same folder as `app.py`**:

- `Nassau_Candy_Cleaned.csv`
- `Route_Analysis.csv`
- `Factory_Analysis.csv`
- `State_Bottleneck_Analysis.csv`

If any file is missing, the dashboard displays an error listing the required files and stops.

### Expected columns in `Nassau_Candy_Cleaned.csv`

| Column | Description |
|--------|-------------|
| `Order ID` | Unique order identifier |
| `Order Date` | Date the order was placed |
| `Ship Date` | Date the order was shipped |
| `Shipping Lead Time` | Calculated gap between order and ship dates (days) |
| `Ship Mode` | Shipping method |
| `Product Name` | Product ordered |
| `Factory` | Originating factory |
| `Region` | Customer region |
| `State/Province` | Customer state |
| `Units` | Units sold |
| `Sales` | Sales revenue |
| `Cost` | Cost of goods |
| `Gross Profit` | Sales minus cost |

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/BRoshini-15/Nassau_Candy_Distributor.git
cd Nassau_Candy_Distributor
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the data files

Place the four CSV files listed above in the same directory as `app.py`.

---

## ▶️ Usage

Run the dashboard locally:

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`).

**How to use it:**

1. Use the **sidebar filters** (Factory, Region, Ship Mode, Product) to narrow the data.
2. Choose a page under **Navigation**.
3. Hover over charts for details, and use the **download buttons** to export route or order data.

---

## 📊 Key Metrics

| Metric | Definition |
|--------|------------|
| **Total Sales** | Sum of `Sales` |
| **Gross Profit** | Sum of `Gross Profit` |
| **Profit Margin %** | `Gross Profit / Sales × 100` |
| **Total Orders** | Count of unique `Order ID` |
| **Total Units** | Sum of `Units` |
| **Average Lead Time** | Mean of `Shipping Lead Time` (days) |
| **Route** | A unique Factory + Region combination |
| **Lead Time Std** | Standard deviation of lead time per route |

---

## ⚠️ Data Quality Note

The supplied dataset contains **unusually large differences between Order Date and Ship Date**. The calculated date gap (`Shipping Lead Time`) should therefore **not be interpreted as a validated standard delivery duration**. It is used here only for relative comparison between routes, regions, states, and ship modes.

---

## 👩‍💻 Author

**Baikan Roshini**

B.Tech, Computer Science Engineering | Data Science Intern

🔗 GitHub: [github.com/BRoshini-15/Nassau_Candy_Distributor](https://github.com/BRoshini-15/Nassau_Candy_Distributor)

---

⭐ If you found this project useful, consider giving it a star!
