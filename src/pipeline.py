#Mock Data of 1000 messy operational records containing data quality flaws (missing customer IDs)
#invalid data formats, negative amounts) using Faker
import pandas as pd
import numpy as np
from faker import Faker
import os
from sklearn.ensemble import IsolationForest

fake = Faker()
os.makedirs("data", exist_ok=True)

# --- PART 1: Generate Mock "Messy" Raw Data ---
print("Generating raw mock data...")
num_records = 1000

raw_data = {
    "transaction_id": [f"TXN_{i}" for i in range(num_records)],
    "customer_id": np.random.choice([np.nan, 101, 102, 103, 104, 105, 999], num_records),
    "vendor_id": np.random.choice([201, 202, 203, 204], num_records),
    "transaction_date": np.random.choice(["2026-09-01", "2026-09-02", "Invalid_Date", None], num_records),
    "amount": np.random.choice([-50.0, 120.5, 450.0, np.nan, 15000.0], num_records),
    "payment_method": np.random.choice(["Credit Card", "PayPal", "Bank Transfer", None], num_records)
}

df_raw = pd.DataFrame(raw_data)
raw_file_path = "data/raw_transactions.csv"
df_raw.to_csv(raw_file_path, index=False)
print(f"Raw mock data saved to {raw_file_path}")


# --- PART 2: Python Data Cleaning & Quality Checks ---
print("\nRunning Data Cleaning & Quality Checks...")
df = pd.read_csv(raw_file_path)
initial_row_count = len(df)

error_logs = []
mask_missing = df['transaction_id'].isnull() | df['customer_id'].isnull() | df['transaction_date'].isnull()
if mask_missing.sum() > 0:
    error_logs.append({"file_name": "raw_transactions.csv", "error_message": "Missing critical primary fields", "rows_affected": mask_missing.sum()})

df = df.dropna(subset=['transaction_id', 'customer_id', 'transaction_date'])

df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
date_error_count = df['transaction_date'].isnull().sum()
if date_error_count > 0:
    error_logs.append({"file_name": "raw_transactions.csv", "error_message": "Invalid date format parsed as NaT", "rows_affected": date_error_count})
df = df.dropna(subset=['transaction_date'])

amount_error_mask = df['amount'] <= 0
if amount_error_mask.sum() > 0:
    error_logs.append({"file_name": "raw_transactions.csv", "error_message": "Negative or zero transaction amounts", "rows_affected": amount_error_mask.sum()})
df = df[df['amount'] > 0]
df['payment_method'] = df['payment_method'].fillna('Unknown')

print(f"Cleaning complete! Clean rows retained: {len(df)} out of {initial_row_count}.")


# --- PART 3: AI Anomaly Detection (Isolation Forest) ---
print("\nRunning AI Anomaly Detection Model...")

features = df[['amount']]

# Initialize Isolation Forest (contamination=0.05 expects ~5% anomalies)
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly_prediction'] = model.fit_predict(features)

df['is_flagged_anomaly'] = df['anomaly_prediction'].apply(lambda x: 1 if x == -1 else 0)
df['anomaly_score'] = model.decision_function(features)

df = df.drop(columns=['anomaly_prediction'])

flagged_count = df['is_flagged_anomaly'].sum()
print(f"AI Model analysis complete. Flagged {flagged_count} anomalous transactions as high-risk.")

# Save final processed dataset ready for MySQL loading
final_file_path = "data/processed_transactions_with_ai.csv"
df.to_csv(final_file_path, index=False)
print(f"Processed data with AI scores saved to {final_file_path}")