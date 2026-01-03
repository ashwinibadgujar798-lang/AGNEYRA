import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Mobile Sales Dashboard",
    layout="wide"
)

st.title("📊 Mobile Sales Performance Dashboard")
st.caption("Professional | Clean | Client-Ready")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Sales_data.csv")

# ---------------- DATA CLEANING ----------------
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df["Product_Name"] = df["Product_Name"].str.strip().str.title()
df["City"] = df["City"].str.strip()

df["Quantity_Sold"] = pd.to_numeric(df["Quantity_Sold"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"], errors="coerce")

df = df.dropna(subset=["Quantity_Sold", "Unit_Price", "Sale_Date"])
df = df[(df["Quantity_Sold"] > 0) & (df["Unit_Price"] > 0)]

df["Revenue"] = df["Quantity_Sold"] * df["Unit_Price"]
df["Profit"] = df["Revenue"] * 0.30

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

product_filter = st.sidebar.multiselect(
    "Select Product",
    sorted(df["Product_Name"].unique()),
    default=sorted(df["Product_Name"].unique())
)

df_filtered = df[
    (df["City"].isin(city_filter)) &
    (df["Product_Name"].isin(product_filter))
]

# ---------------- KPI ROW ----------------
k1, k2, k3 = st.columns(3)

k1.metric("📦 Units Sold", int(df_filtered["Quantity_Sold"].sum()))
k2.metric("💰 Revenue", f"₹ {int(df_filtered['Revenue'].sum()):,}")
k3.metric("📈 Profit", f"₹ {int(df_filtered['Profit'].sum()):,}")

st.divider()

# ================= ROW 1 : TWO CHARTS =================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📱 Top Products (Units Sold)")
    product_sales = (
        df_filtered.groupby("Product_Name")["Quantity_Sold"]
        .sum().sort_values(ascending=False).head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=product_sales.values,
        y=product_sales.index,
        palette="magma",
        ax=ax1
    )
    ax1.set_xlabel("Units Sold")
    ax1.set_ylabel("Product")
    st.pyplot(fig1)

with c2:
    st.subheader("🏙 City-wise Sales")
    city_sales = df_filtered.groupby("City")["Quantity_Sold"].sum()

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=city_sales.index,
        y=city_sales.values,
        palette="viridis",
        ax=ax2
    )
    ax2.set_xlabel("City")
    ax2.set_ylabel("Units Sold")
    st.pyplot(fig2)

st.divider()

# ================= ROW 2 : TWO CHARTS =================
c3, c4 = st.columns(2)

with c3:
    st.subheader("📅 Monthly Sales Trend")

    monthly_sales = (
        df_filtered
        .groupby(df_filtered["Sale_Date"].dt.to_period("M"))["Quantity_Sold"]
        .sum()
        .reset_index()
    )

    monthly_sales["Sale_Date"] = monthly_sales["Sale_Date"].astype(str)

    fig3, ax3 = plt.subplots(figsize=(6,4))
    ax3.plot(
        monthly_sales["Sale_Date"],
        monthly_sales["Quantity_Sold"],
        marker="o",
        linewidth=3
    )

    ax3.set_xlabel("Month")
    ax3.set_ylabel("Units Sold")
    ax3.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig3)


with c4:
    st.subheader("💹 Profit by Product")
    profit_product = (
        df_filtered.groupby("Product_Name")["Profit"]
        .sum().sort_values(ascending=False).head(10)
    )

    fig4, ax4 = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=profit_product.values,
        y=profit_product.index,
        palette="coolwarm",
        ax=ax4
    )
    ax4.set_xlabel("Profit")
    ax4.set_ylabel("Product")
    st.pyplot(fig4)

st.divider()

# ---------------- RAW DATA ----------------
with st.expander("📄 View Cleaned Data"):
    st.dataframe(df_filtered)
