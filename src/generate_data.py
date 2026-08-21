"""
generate_data.py
-----------------
Generates a realistic synthetic retail sales dataset for the
Retail Sales Performance & Trend Analysis project.

Run:
    python src/generate_data.py
Output:
    data/retail_sales_data.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
N_TRANSACTIONS = 15000

REGIONS = ["North", "South", "East", "West", "Central"]
STORES = {
    "North": ["Store_N1", "Store_N2"],
    "South": ["Store_S1", "Store_S2"],
    "East": ["Store_E1"],
    "West": ["Store_W1", "Store_W2"],
    "Central": ["Store_C1"],
}

CATEGORIES = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Speaker"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Home & Kitchen": ["Mixer", "Cookware Set", "Vacuum Cleaner", "Lamp", "Bedsheet"],
    "Grocery": ["Rice 5kg", "Cooking Oil", "Snack Pack", "Beverages", "Spices Combo"],
    "Beauty": ["Face Wash", "Perfume", "Lipstick", "Shampoo", "Sunscreen"],
}

BASE_PRICE = {
    "Headphones": 1800, "Smartphone": 18000, "Laptop": 45000, "Smartwatch": 3500, "Speaker": 2500,
    "T-Shirt": 600, "Jeans": 1500, "Jacket": 2800, "Sneakers": 3200, "Cap": 350,
    "Mixer": 2200, "Cookware Set": 3500, "Vacuum Cleaner": 6500, "Lamp": 900, "Bedsheet": 1200,
    "Rice 5kg": 450, "Cooking Oil": 220, "Snack Pack": 150, "Beverages": 180, "Spices Combo": 300,
    "Face Wash": 250, "Perfume": 1800, "Lipstick": 500, "Shampoo": 350, "Sunscreen": 450,
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
CUSTOMER_SEGMENTS = ["New", "Regular", "Loyal", "VIP"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=np.random.randint(0, delta.days), seconds=np.random.randint(0, 86400))


def seasonal_multiplier(date):
    """Boost sales around festive/holiday season (Oct-Dec) and summer sale (Jun)."""
    month = date.month
    if month in (10, 11, 12):
        return np.random.uniform(1.3, 1.8)
    if month == 6:
        return np.random.uniform(1.1, 1.3)
    if month in (1, 2):
        return np.random.uniform(0.8, 1.0)
    return np.random.uniform(0.9, 1.15)


rows = []
for i in range(N_TRANSACTIONS):
    order_date = random_date(START_DATE, END_DATE)
    region = np.random.choice(REGIONS)
    store = np.random.choice(STORES[region])
    category = np.random.choice(list(CATEGORIES.keys()))
    product = np.random.choice(CATEGORIES[category])

    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4], p=[0.35, 0.2, 0.15, 0.15, 0.07, 0.05, 0.03])
    unit_price = BASE_PRICE[product] * np.random.uniform(0.92, 1.08)
    discount_pct = np.random.choice([0, 5, 10, 15, 20, 25], p=[0.35, 0.2, 0.2, 0.15, 0.07, 0.03])

    mult = seasonal_multiplier(order_date)
    gross_sales = unit_price * quantity * mult
    discount_amt = gross_sales * (discount_pct / 100)
    net_sales = gross_sales - discount_amt

    profit_margin_pct = np.random.uniform(0.10, 0.35)
    profit = net_sales * profit_margin_pct

    rows.append({
        "OrderID": f"ORD{100000 + i}",
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "Region": region,
        "Store": store,
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "UnitPrice": round(unit_price, 2),
        "DiscountPct": discount_pct,
        "GrossSales": round(gross_sales, 2),
        "NetSales": round(net_sales, 2),
        "Profit": round(profit, 2),
        "PaymentMethod": np.random.choice(PAYMENT_METHODS, p=[0.25, 0.2, 0.35, 0.1, 0.1]),
        "CustomerSegment": np.random.choice(CUSTOMER_SEGMENTS, p=[0.3, 0.4, 0.2, 0.1]),
        "CustomerAge": int(np.clip(np.random.normal(34, 10), 18, 70)),
    })

df = pd.DataFrame(rows).sort_values("OrderDate").reset_index(drop=True)
df.to_csv("data/retail_sales_data.csv", index=False)
print(f"Generated {len(df)} rows -> data/retail_sales_data.csv")
print(df.head())
