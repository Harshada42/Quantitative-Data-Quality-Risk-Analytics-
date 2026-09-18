#Script connect to local mysql database, populates the parent dimension table
import pandas as pd
import mysql.connector
from datetime import datetime

# --- 1. Connect to MySQL Database ---
print("Connecting to MySQL Database...")
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",          # Default root user
    password="",          # Blank password based on your setup
    database="risk_analytics_db"
)
cursor = db.cursor()
print("Successfully connected to MySQL!")

# --- 2. Load Processed Data from Data Folder ---
df = pd.read_csv("data/processed_transactions_with_ai.csv")

# --- 3. Populate Dimension Tables First (Foreign Key Requirements) ---
print("\nPopulating Dimension Tables...")

# Populate dim_customers
unique_customers = df['customer_id'].unique()
for cust_id in unique_customers:
    cursor.execute("""
        INSERT IGNORE INTO dim_customers (customer_id, customer_name, signup_date, country, account_status)
        VALUES (%s, %s, %s, %s, %s)
    """, (int(cust_id), f"Customer_{cust_id}", '2025-01-01', 'USA', 'Active'))

# Populate dim_vendors
unique_vendors = df['vendor_id'].unique()
for vend_id in unique_vendors:
    cursor.execute("""
        INSERT IGNORE INTO dim_vendors (vendor_id, vendor_name, vendor_category, risk_rating)
        VALUES (%s, %s, %s, %s)
    """, (int(vend_id), f"Vendor_{vend_id}", 'Technology', 'Standard'))

# Populate dim_dates
unique_dates = df['transaction_date'].unique()
for d_str in unique_dates:
    dt = datetime.strptime(d_str.split()[0], '%Y-%m-%d')
    cursor.execute("""
        INSERT IGNORE INTO dim_dates (date_key, year, quarter, month, day_of_week)
        VALUES (%s, %s, %s, %s, %s)
    """, (dt.date(), dt.year, (dt.month - 1) // 3 + 1, dt.month, dt.strftime('%A')))

db.commit()
print("Dimension tables populated successfully!")

# --- 4. Populate Fact Table ---
print("\nPopulating Fact Table (fact_transactions)...")
inserted_count = 0

for _, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO fact_transactions 
            (transaction_id, customer_id, vendor_id, transaction_date, amount, payment_method, is_flagged_anomaly, anomaly_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE amount=VALUES(amount)
        """, (
            row['transaction_id'],
            int(row['customer_id']),
            int(row['vendor_id']),
            row['transaction_date'].split()[0],
            float(row['amount']),
            row['payment_method'],
            int(row['is_flagged_anomaly']),
            float(row['anomaly_score'])
        ))
        inserted_count += 1
    except mysql.connector.Error as err:
        print(f"Error inserting row {row['transaction_id']}: {err}")

db.commit()
cursor.close()
db.close()
print(f"\nSuccessfully loaded {inserted_count} rows into `fact_transactions` in MySQL!")