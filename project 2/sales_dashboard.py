"""
Sales & Revenue Analysis Dashboard
Internship Project — Assignment #1
Analyzes sales data: KPIs, trends, top products, region-wise breakdown
"""

import pandas as pd

# ── Sample Data (simulates CSV/Excel import) ──────────────────────────────────
data = {
    "Order_ID":    [1001,1002,1004,1005,1006,1007,1008,1009,1010,
                    1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,
                    1021,1022,1023,1024,1025,1026,1027,1028,1029,1030],
    "Customer":    ["Alice Johnson","Bob Smith","Charlie Brown","Diana Prince",
                    "Eve Adams","Frank Miller","Grace Lee","Unknown Customer","Henry Ford",
                    "Bob Smith","Ivy Chen","Jack Wilson","Karen Davis","Liam Brown",
                    "Mia Clark","Noah Scott","Olivia Wang","Peter Hall","Quinn Adams",
                    "Rachel Kim","Sam Taylor","Tina Moore","Uma Patel","Victor Cruz",
                    "Wendy Hill","Xander Reed","Yara Noel","Zoe Martin","Alice Johnson"],
    "Product":     ["Laptop","Phone","Tablet","Headphones","Monitor","Keyboard","Mouse",
                    "Laptop","Webcam","Phone","Speaker","Charger","Laptop","Tablet",
                    "Headphones","Monitor","Keyboard","Mouse","Webcam","Phone","Speaker",
                    "Charger","Laptop","Tablet","Headphones","Monitor","Keyboard","Mouse","Webcam"],
    "Category":    ["Electronics"]*10 + ["Electronics","Accessories","Electronics","Electronics",
                    "Electronics","Electronics","Accessories","Accessories","Accessories",
                    "Electronics","Electronics","Accessories","Electronics","Electronics",
                    "Electronics","Electronics","Accessories","Accessories","Accessories"],
    "Qty":         [2,2,1,3,2,5,10,1,2, 2,4,8,1,2,1,3,6,15,3, 2,5,10,1,3,2,1,7,12,2],
    "Unit_Price":  [75000,45000,30000,12000,18000,3500,1200,75000,5000,
                    45000,8000,1500,75000,30000,12000,18000,3500,1200,5000,
                    45000,8000,1500,75000,30000,12000,18000,3500,1200,5000],
    "Month":       ["Jan 2026"]*9 + ["Feb 2026"]*10 + ["Mar 2026"]*10,
    "Region":      ["North","South","East","West","North","South","East","West","North",
                    "South","East","West","North","South","East","West","North","South","East",
                    "West","North","South","East","West","North","South","East","West","North"],
    "Status":      ["Completed","Completed","Pending","Completed","Completed","Cancelled",
                    "Completed","Completed","Completed","Completed","Pending","Completed",
                    "Completed","Completed","Completed","Completed","Completed","Completed",
                    "Completed","Completed","Completed","Completed","Pending","Completed",
                    "Completed","Completed","Cancelled","Completed","Completed"],
}

# ── Load into DataFrame ───────────────────────────────────────────────────────
def load_data(source="inline"):
    """
    In a real project, replace with:
        pd.read_csv("sales.csv")   or
        pd.read_excel("sales.xlsx")
    """
    df = pd.DataFrame(data)
    df["Total_Sale"] = df["Qty"] * df["Unit_Price"]
    return df


# ── KPI Calculations ──────────────────────────────────────────────────────────
def compute_kpis(df):
    comp = df[df["Status"] == "Completed"]
    return {
        "Total Revenue (₹)":      comp["Total_Sale"].sum(),
        "Total Orders":           len(df),
        "Completed Orders":       len(comp),
        "Avg Order Value (₹)":    comp["Total_Sale"].mean(),
        "Total Units Sold":       comp["Qty"].sum(),
        "Completion Rate (%)":    round(len(comp) / len(df) * 100, 1),
    }


# ── Trend Analysis ────────────────────────────────────────────────────────────
def monthly_trend(df):
    comp = df[df["Status"] == "Completed"]
    return comp.groupby("Month")["Total_Sale"].sum().reset_index()


# ── Region Analysis ───────────────────────────────────────────────────────────
def region_analysis(df):
    comp = df[df["Status"] == "Completed"]
    return (comp.groupby("Region")["Total_Sale"]
            .sum().sort_values(ascending=False)
            .reset_index())


# ── Top Products ──────────────────────────────────────────────────────────────
def top_products(df, n=5):
    comp = df[df["Status"] == "Completed"]
    return (comp.groupby(["Product", "Category"])
            .agg(Revenue=("Total_Sale","sum"), Units=("Qty","sum"))
            .sort_values("Revenue", ascending=False)
            .head(n).reset_index())


# ── Category Split ────────────────────────────────────────────────────────────
def category_split(df):
    comp = df[df["Status"] == "Completed"]
    return comp.groupby("Category")["Total_Sale"].sum().reset_index()


# ── Main Report ───────────────────────────────────────────────────────────────
def print_report(df):
    sep = "─" * 52
    print(f"\n{'═'*52}")
    print("   SALES & REVENUE ANALYSIS DASHBOARD")
    print(f"{'═'*52}")

    kpis = compute_kpis(df)
    print("\n📊 KEY PERFORMANCE INDICATORS")
    print(sep)
    for k, v in kpis.items():
        if "₹" in k:
            print(f"  {k:<28} ₹{v:>12,.0f}")
        elif "%" in k:
            print(f"  {k:<28} {v:>11}%")
        else:
            print(f"  {k:<28} {v:>12}")

    print(f"\n📈 MONTHLY REVENUE TREND")
    print(sep)
    trend = monthly_trend(df)
    for _, row in trend.iterrows():
        bar = "█" * int(row["Total_Sale"] / 20000)
        print(f"  {row['Month']}   ₹{row['Total_Sale']:>10,.0f}  {bar}")

    print(f"\n🗺️  REVENUE BY REGION")
    print(sep)
    for _, row in region_analysis(df).iterrows():
        print(f"  {row['Region']:<10}  ₹{row['Total_Sale']:>10,.0f}")

    print(f"\n🏆 TOP 5 PRODUCTS")
    print(sep)
    for _, row in top_products(df).iterrows():
        print(f"  {row['Product']:<14} [{row['Category']:<13}]  ₹{row['Revenue']:>9,.0f}  {row['Units']} units")

    print(f"\n📦 CATEGORY SPLIT")
    print(sep)
    for _, row in category_split(df).iterrows():
        print(f"  {row['Category']:<16}  ₹{row['Total_Sale']:>10,.0f}")

    print(f"\n{'═'*52}\n")


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    print_report(df)

    # Export cleaned data
    df.to_csv("sales_data_export.csv", index=False)
    print("✅ Exported sales_data_export.csv")
    print("✅ Open Sales_Revenue_Dashboard.xlsx for the full Excel report with charts")
    print("✅ Open sales_dashboard.html in a browser for the interactive dashboard")
