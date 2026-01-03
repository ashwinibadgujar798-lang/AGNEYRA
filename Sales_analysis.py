import pandas as pd

def load_clean_data():
    df = pd.read_csv("Sales_data.csv")

    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    df["Product_Name"] = df["Product_Name"].astype(str).str.strip()
    df["City"] = df["City"].astype(str).str.strip()

    df["Quantity_Sold"] = pd.to_numeric(df["Quantity_Sold"], errors="coerce").fillna(0)
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").fillna(0)

    df["Sale_Date"] = pd.to_datetime(df["Sale_Date"], errors="coerce")

    df["Revenue"] = df["Quantity_Sold"] * df["Unit_Price"]
    df["Profit"] = df["Revenue"] * 0.3

    return df
