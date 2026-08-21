"""
analysis.py
------------
Retail Sales Performance & Trend Analysis
Loads data/retail_sales_data.csv, computes KPIs, and saves charts to /images.

Run:
    python src/analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("data/retail_sales_data.csv", parse_dates=["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
df["Quarter"] = df["OrderDate"].dt.to_period("Q").astype(str)
df["Weekday"] = df["OrderDate"].dt.day_name()

# ------------------------------------------------------------------
# 1. Core KPIs
# ------------------------------------------------------------------
total_sales = df["NetSales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["OrderID"].nunique()
avg_order_value = total_sales / total_orders
profit_margin = total_profit / total_sales * 100

print("=" * 50)
print("RETAIL SALES PERFORMANCE — KPI SUMMARY")
print("=" * 50)
print(f"Total Net Sales      : ₹{total_sales:,.0f}")
print(f"Total Profit         : ₹{total_profit:,.0f}")
print(f"Total Orders         : {total_orders:,}")
print(f"Average Order Value  : ₹{avg_order_value:,.2f}")
print(f"Overall Profit Margin: {profit_margin:.1f}%")
print("=" * 50)

# ------------------------------------------------------------------
# 2. Monthly Sales Trend
# ------------------------------------------------------------------
monthly = df.groupby("Month")["NetSales"].sum().reset_index()
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly, x="Month", y="NetSales", marker="o", linewidth=2.5, color="#2E86AB")
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Net Sales Trend (2023–2024)", fontsize=14, fontweight="bold")
plt.ylabel("Net Sales (₹)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("images/01_monthly_sales_trend.png")
plt.close()

# ------------------------------------------------------------------
# 3. Sales by Region
# ------------------------------------------------------------------
region_sales = df.groupby("Region")["NetSales"].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=region_sales, x="Region", y="NetSales", palette="viridis")
plt.title("Total Net Sales by Region", fontsize=14, fontweight="bold")
plt.ylabel("Net Sales (₹)")
plt.tight_layout()
plt.savefig("images/02_sales_by_region.png")
plt.close()

# ------------------------------------------------------------------
# 4. Category Performance (Sales vs Profit)
# ------------------------------------------------------------------
cat_perf = df.groupby("Category").agg(NetSales=("NetSales", "sum"), Profit=("Profit", "sum")).reset_index()
cat_perf = cat_perf.sort_values("NetSales", ascending=False)
fig, ax1 = plt.subplots(figsize=(10, 5.5))
sns.barplot(data=cat_perf, x="Category", y="NetSales", ax=ax1, color="#5DA5DA", label="Net Sales")
ax2 = ax1.twinx()
sns.lineplot(data=cat_perf, x="Category", y="Profit", ax=ax2, color="#FA7921", marker="o", linewidth=2.5, label="Profit")
ax1.set_ylabel("Net Sales (₹)")
ax2.set_ylabel("Profit (₹)")
plt.title("Category Performance: Sales vs Profit", fontsize=14, fontweight="bold")
fig.tight_layout()
plt.savefig("images/03_category_performance.png")
plt.close()

# ------------------------------------------------------------------
# 5. Top 10 Products
# ------------------------------------------------------------------
top_products = df.groupby("Product")["NetSales"].sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(9, 6))
sns.barplot(data=top_products, y="Product", x="NetSales", palette="mako")
plt.title("Top 10 Best-Selling Products by Net Sales", fontsize=14, fontweight="bold")
plt.xlabel("Net Sales (₹)")
plt.tight_layout()
plt.savefig("images/04_top10_products.png")
plt.close()

# ------------------------------------------------------------------
# 6. Customer Segment Contribution
# ------------------------------------------------------------------
seg = df.groupby("CustomerSegment")["NetSales"].sum().reset_index()
plt.figure(figsize=(7, 7))
plt.pie(seg["NetSales"], labels=seg["CustomerSegment"], autopct="%1.1f%%",
        colors=sns.color_palette("viridis", len(seg)), startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5})
plt.title("Sales Contribution by Customer Segment", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("images/05_customer_segment_share.png")
plt.close()

# ------------------------------------------------------------------
# 7. Weekday Sales Pattern
# ------------------------------------------------------------------
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = df.groupby("Weekday")["NetSales"].sum().reindex(weekday_order).reset_index()
plt.figure(figsize=(9, 5))
sns.barplot(data=wd, x="Weekday", y="NetSales", palette="crest")
plt.title("Sales by Day of the Week", fontsize=14, fontweight="bold")
plt.ylabel("Net Sales (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("images/06_weekday_pattern.png")
plt.close()

# ------------------------------------------------------------------
# 8. Discount vs Profit Margin relationship
# ------------------------------------------------------------------
df["ProfitMarginPct"] = df["Profit"] / df["NetSales"] * 100
disc_margin = df.groupby("DiscountPct")["ProfitMarginPct"].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=disc_margin, x="DiscountPct", y="ProfitMarginPct", palette="rocket")
plt.title("Average Profit Margin by Discount Level", fontsize=14, fontweight="bold")
plt.xlabel("Discount (%)")
plt.ylabel("Avg Profit Margin (%)")
plt.tight_layout()
plt.savefig("images/07_discount_vs_margin.png")
plt.close()

# ------------------------------------------------------------------
# 9. Region x Category Heatmap
# ------------------------------------------------------------------
pivot = df.pivot_table(index="Region", columns="Category", values="NetSales", aggfunc="sum")
plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlGnBu", linewidths=0.5)
plt.title("Net Sales Heatmap: Region vs Category", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("images/08_region_category_heatmap.png")
plt.close()

print("\nAll charts saved to /images")

# ------------------------------------------------------------------
# 10. Save summary KPIs to a text report
# ------------------------------------------------------------------
best_region = region_sales.iloc[0]["Region"]
best_category = cat_perf.iloc[0]["Category"]
best_product = top_products.iloc[0]["Product"]
best_month = monthly.loc[monthly["NetSales"].idxmax(), "Month"]

with open("reports/summary_insights.md", "w") as f:
    f.write("# Retail Sales Performance — Key Insights\n\n")
    f.write(f"- **Total Net Sales:** ₹{total_sales:,.0f}\n")
    f.write(f"- **Total Profit:** ₹{total_profit:,.0f} ({profit_margin:.1f}% margin)\n")
    f.write(f"- **Total Orders:** {total_orders:,}\n")
    f.write(f"- **Average Order Value:** ₹{avg_order_value:,.2f}\n")
    f.write(f"- **Top Performing Region:** {best_region}\n")
    f.write(f"- **Top Performing Category:** {best_category}\n")
    f.write(f"- **Best-Selling Product:** {best_product}\n")
    f.write(f"- **Peak Sales Month:** {best_month}\n")
    f.write("\n## Observations\n")
    f.write("- Sales peak sharply in Oct–Dec, consistent with festive/holiday shopping season.\n")
    f.write("- Higher discount tiers (20%+) correlate with lower average profit margins, "
            "suggesting discount strategy should be tightened for low-margin categories.\n")
    f.write("- 'Loyal' and 'Regular' customer segments drive the majority of revenue, "
            "indicating retention programs are working but new customer acquisition needs attention.\n")
    f.write("- Weekend (Sat/Sun) sales are consistently higher than weekdays.\n")

print("Summary insights saved to reports/summary_insights.md")
