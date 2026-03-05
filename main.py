import pandas as pd
import matplotlib.pyplot as plt
import os

# ===============================
# 👇 هنا تعطي اسم ملف CSV الخاص بك
# ===============================
csv_path = input("Enter the path to your CSV file: ")  # مثال: data/raw/my_data.csv

# ===============================
# تحميل البيانات
# ===============================
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("❌ File not found! تأكد من المسار.")
    exit()

# ===============================
# تنظيف البيانات
# ===============================
df = df.drop_duplicates()
df = df.dropna()

# إذا موجود عمود date، حوله إلى datetime
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

# ===============================
# حفظ نسخة نظيفة
# ===============================
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/cleaned_data.csv", index=False)

# ===============================
# التحليل
# ===============================
if "sales" not in df.columns:
    print("❌ CSV must have a 'sales' column.")
    exit()

# Total و Average
total_sales = df["sales"].sum()
average_sales = df["sales"].mean()

# Sales by category إذا موجود عمود category
if "category" in df.columns:
    sales_by_category = df.groupby("category")["sales"].sum()
else:
    sales_by_category = None

print("\nTotal Sales:", total_sales)
print("Average Sales:", average_sales)
if sales_by_category is not None:
    print("\nSales by Category:\n", sales_by_category)

# ===============================
# الرسم
# ===============================
os.makedirs("plots", exist_ok=True)
if sales_by_category is not None:
    sales_by_category.plot(kind="bar")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("plots/sales_by_category.png")
    plt.close()
    print("\n✅ Bar chart saved at 'plots/sales_by_category.png'")

print("\n✅ Cleaned CSV saved at 'data/processed/cleaned_data.csv'")