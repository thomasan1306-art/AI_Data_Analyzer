import streamlit as st
import pandas as pd
from sales_app import analyze_sales
from google import genai


st.set_page_config(
    page_title="AI Business Data Analyzer",
    page_icon="📊",
    layout="wide"
)


# ==================== AI KEY ====================

client = genai.Client(
    api_key=st.secrets["GEMNI_KEY"]
)


st.title("AI Business Data Analyzer")

st.write(
    "Analyze your sales data with AI-powered insights."
)


# ==================== Upload CSV ====================

uploaded_file = st.file_uploader(
    "Upload your sales CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👆 Please upload a CSV file to get started.")
    st.stop()

data = pd.read_csv(uploaded_file)


# ==================== Data Validation ====================

required_columns = [
    "Product",
    "Category",
    "Quantity",
    "Price"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:
    st.error(
        f"Missing columns: {', '.join(missing_columns)}"
    )
    st.stop()

# ==================== Numeric Validation ====================

for column in ["Quantity", "Price"]:

    if not pd.api.types.is_numeric_dtype(data[column]):

        st.error(
            f"{column} must contain numbers."
        )

        st.stop()

    if data[column].isna().any():

        st.error(
            f"{column} contains missing values."
        )

        st.stop()

    if (data[column] < 0).any():

        st.error(
            f"{column} cannot be negative."
        )

        st.stop()

# ==================== View Data ====================

with st.expander("View Sales Data"):
    st.dataframe(data)


# ==================== Analyze Sales ====================

results = analyze_sales(data)


# ==================== Business Summary ====================

st.subheader("Business Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"${results['total_revenue']:,.0f}"
    )

with col2:
    st.metric(
        "Total Quantity",
        f"{results['quantity']:,}"
    )

with col3:
    st.metric(
        "Average Price",
        f"${results['average_price']:,.2f}"
    )


# ==================== Business Insights ====================

st.subheader("Business Insights")

st.info(results["insight"])

st.info(results["insight2"])

st.info(results["insight3"])

st.write(results["sales_vs_revenue"])


# ==================== AI Explanation ====================

st.subheader("🤖 AI Business Explanation")

if st.button("Generate AI Explanation"):

    prompt = f"""
    Analyze the following business sales results.

    Total Revenue: ${results['total_revenue']:,.2f}
    Total Quantity: {results['quantity']}
    Best Product: {results['best_product']}
    Best Category: {results['best_category']}
    Most Sold Product: {results['most_sold']}
    Average Price: ${results['average_price']:,.2f}

    Business Insights:
    {results['insight']}
    {results['insight2']}
    {results['insight3']}
    {results['sales_vs_revenue']}

    Explain these results in simple business language.

    Give 3 useful observations.

    Do not invent any numbers.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        st.write(response.text)
    except Exception:
        st.error("Gemini AI is temporarily unavailable. Please try again later.")


# ==================== Top Products ====================

st.subheader("Top Products")

for product, revenue in results["top_products"].items():

    st.write(
        f"**{product}** — ${revenue:,.0f}"
    )


# ==================== Create Revenue Column ====================

chart_data = data.copy()

chart_data["Revenue"] = (
    chart_data["Quantity"]
    * chart_data["Price"]
)


# ==================== Calculate Chart Data ====================

top_5 = (
    chart_data
    .groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

revenue_by_product = (
    chart_data
    .groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

revenue_by_category = (
    chart_data
    .groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

quantity_by_product = (
    chart_data
    .groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)


# ==================== Sales Charts ====================

st.subheader("Sales Charts")

col1, col2 = st.columns(2)

with col1:

    st.write("### 🏆 Top 5 Products by Revenue")

    st.bar_chart(top_5)


with col2:

    st.write("### 💰 Revenue by Product")

    st.bar_chart(revenue_by_product)


col3, col4 = st.columns(2)

with col3:

    st.write("### 🏢 Revenue by Category")

    st.bar_chart(revenue_by_category)


with col4:

    st.write("### 📦 Quantity by Product")

    st.bar_chart(quantity_by_product)


# ==================== Download Report ====================

st.subheader("📥 Export Report")

report = pd.DataFrame({

    "Metric": [
        "Total Revenue",
        "Total Quantity",
        "Average Price",
        "Best Product",
        "Best Category",
        "Most Sold Product"
    ],

    "Value": [
        results["total_revenue"],
        results["quantity"],
        results["average_price"],
        results["best_product"],
        results["best_category"],
        results["most_sold"]
    ]
})


csv_report = report.to_csv(index=False)


st.download_button(
    label="Download Sales Report",
    data=csv_report,
    file_name="sales_report.csv",
    mime="text/csv"
)
