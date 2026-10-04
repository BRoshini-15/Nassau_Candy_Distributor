# ============================================================
# NASSAU CANDY DISTRIBUTOR
# Data Science Internship Project
# Route Efficiency & Distribution Analysis Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f8fa;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .small-text {
        color: #6b7280;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Nassau_Candy_Cleaned.csv")

    route_df = pd.read_csv("Route_Analysis.csv")

    factory_df = pd.read_csv("Factory_Analysis.csv")

    state_df = pd.read_csv("State_Bottleneck_Analysis.csv")

    # Convert dates
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"],
            errors="coerce"
        )

    return df, route_df, factory_df, state_df


try:

    df, route_df, factory_df, state_df = load_data()

except FileNotFoundError as e:

    st.error(
        "Required CSV file was not found. "
        "Make sure all generated CSV files are in the same folder as app.py."
    )

    st.code(
        """
Nassau_Candy_Cleaned.csv
Route_Analysis.csv
Factory_Analysis.csv
State_Bottleneck_Analysis.csv
        """
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🍬 Nassau Candy Distribution Analytics")

st.markdown(
    """
    Interactive analysis of sales,  profitability,  products,
     factories,  customer regions and  distribution routes.
    """

)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Dashboard Controls")

st.sidebar.markdown("---")


# Factory filter
factory_options = sorted(
    df["Factory"].dropna().unique().tolist()
)

selected_factories = st.sidebar.multiselect(
    "Select Factory",
    options=factory_options,
    default=factory_options
)


# Region filter
region_options = sorted(
    df["Region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=region_options,
    default=region_options
)


# Ship mode filter
ship_mode_options = sorted(
    df["Ship Mode"].dropna().unique().tolist()
)

selected_ship_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    options=ship_mode_options,
    default=ship_mode_options
)


# Product filter
product_options = sorted(
    df["Product Name"].dropna().unique().tolist()
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=product_options,
    default=product_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["Factory"].isin(selected_factories)
    &
    df["Region"].isin(selected_regions)
    &
    df["Ship Mode"].isin(selected_ship_modes)
    &
    df["Product Name"].isin(selected_products)
].copy()


# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Route Efficiency",
        "Geographic Analysis",
        "Shipping Analysis",
        "Product & Factory Analysis",
        "Order Drill-Down"
    ]
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):

    return f"${value:,.2f}"


def number(value):

    return f"{value:,.0f}"


def percentage(value):

    return f"{value:.2f}%"


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("Executive Dashboard")

    st.caption(
        "High-level view of sales, profitability, shipment volume "
        "and calculated shipping lead time."
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["Gross Profit"].sum()

    total_units = filtered_df["Units"].sum()

    total_orders = filtered_df["Order ID"].nunique()

    avg_lead_time = filtered_df[
        "Shipping Lead Time"
    ].mean()

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sales",
        money(total_sales)
    )

    col2.metric(
        "Gross Profit",
        money(total_profit)
    )

    col3.metric(
        "Total Orders",
        number(total_orders)
    )

    col4.metric(
        "Total Units",
        number(total_units)
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "Profit Margin",
        percentage(profit_margin)
    )

    col6.metric(
        "Average Calculated Lead Time",
        f"{avg_lead_time:.0f} days"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SALES AND PROFIT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        product_sales = (
            filtered_df
            .groupby("Product Name", as_index=False)
            ["Sales"]
            .sum()
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            product_sales,
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top 10 Products by Sales"
        )

        fig.update_layout(
            height=500,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        region_sales = (
            filtered_df
            .groupby("Region", as_index=False)
            ["Sales"]
            .sum()
            .sort_values(
                "Sales",
                ascending=False
            )
        )

        fig = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            title="Sales by Region"
        )

        fig.update_layout(
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # PROFIT BY FACTORY
    # --------------------------------------------------------

    factory_profit = (
        filtered_df
        .groupby("Factory", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
    )

    fig = px.bar(
        factory_profit,
        x="Factory",
        y="Gross_Profit",
        title="Gross Profit by Factory",
        text_auto=".2s"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ROUTE EFFICIENCY
# ============================================================

elif page == "Route Efficiency":

    st.header("🚚 Route Efficiency Analysis")

    st.markdown(
        """
        This section analyzes factory-to-customer routes using
        shipment volume, calculated lead time, sales and delay frequency.
        """
    )

    # --------------------------------------------------------
    # CREATE ROUTE DATA FROM FILTERED DATA
    # --------------------------------------------------------

    route_filtered = (
        filtered_df
        .groupby(
            ["Factory", "Region"],
            as_index=False
        )
        .agg(
            Shipments=("Order ID", "count"),
            Orders=("Order ID", "nunique"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Median_Lead_Time=("Shipping Lead Time", "median"),
            Lead_Time_Std=("Shipping Lead Time", "std")
        )
    )

    route_filtered["Profit Margin %"] = np.where(
        route_filtered["Sales"] != 0,
        (
            route_filtered["Gross_Profit"]
            /
            route_filtered["Sales"]
        ) * 100,
        0
    )

    # --------------------------------------------------------
    # ROUTE KPIs
    # --------------------------------------------------------

    if len(route_filtered) > 0:

        route_col1, route_col2, route_col3 = st.columns(3)

        route_col1.metric(
            "Routes",
            number(len(route_filtered))
        )

        route_col2.metric(
            "Total Shipments",
            number(route_filtered["Shipments"].sum())
        )

        route_col3.metric(
            "Average Lead Time",
            f"{route_filtered['Average_Lead_Time'].mean():.0f} days"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # SCATTER PLOT
    # --------------------------------------------------------

    fig = px.scatter(
        route_filtered,
        x="Average_Lead_Time",
        y="Shipments",
        size="Sales",
        color="Region",
        hover_name="Factory",
        hover_data=[
            "Orders",
            "Gross_Profit",
            "Median_Lead_Time",
            "Profit Margin %"
        ],
        title="Route Volume vs Calculated Lead Time"
    )

    fig.update_layout(
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # ROUTE TABLE
    # --------------------------------------------------------

    st.subheader("Route Performance Table")

    route_display = route_filtered.copy()

    route_display["Sales"] = (
        route_display["Sales"]
        .round(2)
    )

    route_display["Gross_Profit"] = (
        route_display["Gross_Profit"]
        .round(2)
    )

    route_display["Average_Lead_Time"] = (
        route_display["Average_Lead_Time"]
        .round(2)
    )

    route_display["Median_Lead_Time"] = (
        route_display["Median_Lead_Time"]
        .round(2)
    )

    route_display["Profit Margin %"] = (
        route_display["Profit Margin %"]
        .round(2)
    )

    st.dataframe(
        route_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv = route_display.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Route Analysis",
        data=csv,
        file_name="filtered_route_analysis.csv",
        mime="text/csv"
    )


# ============================================================
# GEOGRAPHIC ANALYSIS
# ============================================================

elif page == "Geographic Analysis":

    st.header("🗺️ Geographic Analysis")

    st.markdown(
        """
        Geographic analysis of customer states and regions,
        including sales volume and calculated shipping lead time.
        """
    )

    # --------------------------------------------------------
    # STATE SUMMARY
    # --------------------------------------------------------

    state_filtered = (
        filtered_df
        .groupby(
            "State/Province",
            as_index=False
        )
        .agg(
            Shipments=("Order ID", "count"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Average_Lead_Time=("Shipping Lead Time", "mean")
        )
    )

    # --------------------------------------------------------
    # TOP SALES STATES
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        top_states = (
            state_filtered
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            top_states,
            x="Sales",
            y="State/Province",
            orientation="h",
            title="Top 15 States by Sales"
        )

        fig.update_layout(
            height=600,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # LONGEST LEAD-TIME STATES
    # --------------------------------------------------------

    with col2:

        longest_states = (
            state_filtered
            .sort_values(
                "Average_Lead_Time",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            longest_states,
            x="Average_Lead_Time",
            y="State/Province",
            orientation="h",
            title="States by Average Calculated Date Gap"
        )

        fig.update_layout(
            height=600,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # US MAP
    # --------------------------------------------------------

    st.subheader("State Sales Map")

    # State abbreviation mapping
    state_abbreviations = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY"
    }

    state_filtered["State Code"] = (
        state_filtered["State/Province"]
        .map(state_abbreviations)
    )

    map_data = state_filtered.dropna(
        subset=["State Code"]
    )

    if len(map_data) > 0:

        fig = px.choropleth(
            map_data,
            locations="State Code",
            locationmode="USA-states",
            color="Sales",
            scope="usa",
            hover_name="State/Province",
            hover_data=[
                "Shipments",
                "Gross_Profit",
                "Average_Lead_Time"
            ],
            title="Sales Distribution Across US States"
        )

        fig.update_layout(
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "The state names in the dataset could not be matched "
            "to the US state abbreviation map."
        )

    # --------------------------------------------------------
    # STATE TABLE
    # --------------------------------------------------------

    st.subheader("State-Level Analysis")

    st.dataframe(
        state_filtered.sort_values(
            "Sales",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SHIPPING ANALYSIS
# ============================================================

elif page == "Shipping Analysis":

    st.header("📦 Shipping Analysis")

    # --------------------------------------------------------
    # SHIP MODE SUMMARY
    # --------------------------------------------------------

    ship_summary = (
        filtered_df
        .groupby(
            "Ship Mode",
            as_index=False
        )
        .agg(
            Shipments=("Order ID", "count"),
            Orders=("Order ID", "nunique"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Median_Lead_Time=("Shipping Lead Time", "median")
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            ship_summary,
            x="Ship Mode",
            y="Shipments",
            title="Shipment Volume by Ship Mode",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            ship_summary,
            x="Ship Mode",
            y="Average_Lead_Time",
            title="Average Calculated Lead Time by Ship Mode",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # SHIP MODE SALES
    # --------------------------------------------------------

    fig = px.bar(
        ship_summary,
        x="Ship Mode",
        y="Sales",
        title="Sales by Ship Mode"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # LEAD-TIME DISTRIBUTION
    # --------------------------------------------------------

    fig = px.box(
        filtered_df,
        x="Ship Mode",
        y="Shipping Lead Time",
        color="Ship Mode",
        title="Shipping Lead Time Distribution by Ship Mode"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # SUMMARY TABLE
    # --------------------------------------------------------

    st.subheader("Shipping Mode Summary")

    st.dataframe(
        ship_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PRODUCT & FACTORY ANALYSIS
# ============================================================

elif page == "Product & Factory Analysis":

    st.header("🏭 Product & Factory Analysis")

    # --------------------------------------------------------
    # PRODUCT SUMMARY
    # --------------------------------------------------------

    product_summary = (
        filtered_df
        .groupby(
            "Product Name",
            as_index=False
        )
        .agg(
            Units=("Units", "sum"),
            Sales=("Sales", "sum"),
            Cost=("Cost", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Average_Lead_Time=("Shipping Lead Time", "mean")
        )
    )

    product_summary["Profit Margin %"] = np.where(
        product_summary["Sales"] != 0,
        (
            product_summary["Gross_Profit"]
            /
            product_summary["Sales"]
        ) * 100,
        0
    )

    col1, col2 = st.columns(2)

    with col1:

        top_products = (
            product_summary
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top Products by Sales"
        )

        fig.update_layout(
            height=600,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        top_profit_products = (
            product_summary
            .sort_values(
                "Gross_Profit",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            top_profit_products,
            x="Gross_Profit",
            y="Product Name",
            orientation="h",
            title="Top Products by Gross Profit"
        )

        fig.update_layout(
            height=600,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # FACTORY SUMMARY
    # --------------------------------------------------------

    factory_summary = (
        filtered_df
        .groupby(
            "Factory",
            as_index=False
        )
        .agg(
            Shipments=("Order ID", "count"),
            Orders=("Order ID", "nunique"),
            Units=("Units", "sum"),
            Sales=("Sales", "sum"),
            Cost=("Cost", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Median_Lead_Time=("Shipping Lead Time", "median")
        )
    )

    factory_summary["Profit Margin %"] = np.where(
        factory_summary["Sales"] != 0,
        (
            factory_summary["Gross_Profit"]
            /
            factory_summary["Sales"]
        ) * 100,
        0
    )

    st.subheader("Factory Performance")

    st.dataframe(
        factory_summary.sort_values(
            "Sales",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # FACTORY CHART
    # --------------------------------------------------------

    fig = px.bar(
        factory_summary,
        x="Factory",
        y="Sales",
        color="Factory",
        title="Sales by Factory"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ORDER DRILL-DOWN
# ============================================================

elif page == "Order Drill-Down":

    st.header("🔎 Order-Level Drill-Down")

    st.markdown(
        """
        Use the controls below to inspect individual shipment records.
        """
    )

    # --------------------------------------------------------
    # ORDER SELECTOR
    # --------------------------------------------------------

    order_options = sorted(
        filtered_df["Order ID"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_order = st.selectbox(
        "Select Order ID",
        options=["All Orders"] + order_options
    )

    if selected_order != "All Orders":

        order_data = filtered_df[
            filtered_df["Order ID"]
            == selected_order
        ].copy()

    else:

        order_data = filtered_df.copy()

    # --------------------------------------------------------
    # ORDER DETAILS
    # --------------------------------------------------------

    if len(order_data) > 0:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Records",
            number(len(order_data))
        )

        col2.metric(
            "Sales",
            money(order_data["Sales"].sum())
        )

        col3.metric(
            "Gross Profit",
            money(order_data["Gross Profit"].sum())
        )

        col4.metric(
            "Units",
            number(order_data["Units"].sum())
        )

        st.markdown("---")

        # ----------------------------------------------------
        # DISPLAY COLUMNS
        # ----------------------------------------------------

        display_columns = [
            "Order ID",
            "Order Date",
            "Ship Date",
            "Shipping Lead Time",
            "Ship Mode",
            "Product Name",
            "Factory",
            "Region",
            "State/Province",
            "Units",
            "Sales",
            "Cost",
            "Gross Profit"
        ]

        available_columns = [
            col
            for col in display_columns
            if col in order_data.columns
        ]

        st.dataframe(
            order_data[available_columns],
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # DOWNLOAD ORDER DATA
        # ----------------------------------------------------

        order_csv = order_data[
            available_columns
        ].to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Order Data",
            data=order_csv,
            file_name="order_details.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No records match the selected filters."
        )


# ============================================================
# DATA QUALITY NOTE
# ============================================================

st.sidebar.markdown("---")

st.sidebar.info(

    """
    Data Quality Note :
    
    The supplied dataset contains unusually large
    differences between Order Date and Ship Date. Therefore, the
    calculated date gap should not be interpreted as a validated
    standard delivery duration.
    """
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption("Nassau Candy Distributor")