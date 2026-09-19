# Quantitative-Data-Quality-Risk-Analytics-

This project implements an end-to-end data quality and risk analytics pipeline designed to ingest, sanitize, structurally model, analyze, and report on transactional streams. 

By combining programmatic data cleaning in Python with unsupervised machine learning (Isolation Forest), a fully normalized relational Star Schema in MySQL, advanced SQL window functions, and programmatic Excel report automation, the system bridges the gap between raw data ingestion and executive-level risk visibility.

---
## 📊 Project Outputs & Visual Evidence

### 1. Executive Risk Summary (SQL Output)
*Categorizing high-risk anomalies versus standard operational transactions:*
![Executive Risk Summary](Summary%20of%20flagged%20anomalies%20vs%20normal.png)

### 2. Vendor Risk Exposure Analysis (Multi-Table JOINs)
*Identifying vendors handling high monetary volumes and flagged risk counts:*
![Vendor Risk Analysis](Vendor%20Risk%20Exposure%20Analysis%20%28Multi%20Table%20Join%20and%20Aggregations%29.png)

### 3. Customer Risk & Spending Rankings (Window Functions)
*Dynamic ranking of high-value accounts using advanced SQL window functions:*
![Customer Risk Ranking](Customer%20Risk%20and%20Spending%20ranking%20%28advanced%20window%20functions%29.png)


## 🔍 Model Evaluation & Operational Validation
The model was evaluated through structural and operational validation:

1. **Contamination Parameter Calibration:** 
   * Configured `contamination=0.05`, establishing an a priori business expectation that approximately 5% of incoming operational transactions would exhibit outlier behavior or heightened risk.
2. **Distribution & Decision Function Analysis:** 
   * The model outputs a continuous decision function score where negative values indicate anomalies. Post-execution logs confirmed that the volume of flagged records aligned precisely with the expected contamination boundary.
3. **Audit & Sanity Verification:** 
   * Cross-referenced flagged anomaly IDs against transaction amounts in MySQL via `sql/analytics.sql` to verify that the model correctly isolated extreme monetary outliers (e.g., unusually large transaction amounts) rather than normal operational spend.


## Technical Stack & Architecture
* **Language & Core Libraries:** Python, Pandas, NumPy, Scikit-Learn, Faker, OpenPyXL, MySQL Connector
* **Database & Querying:** MySQL / MySQL Workbench (Relational Star Schema, Multi-Table JOINs, Analytical Window Functions)
* **Machine Learning:** Unsupervised Anomaly Detection (Isolation Forest)
* **Reporting Output:** Automated Stakeholder Excel Workbooks with Conditional Formatting
* **Version Control:** Git & GitHub

---

## Project Structure
```text
Risk_Analytics_Engine/
│
├── data/                    # Generated raw, AI-scored CSVs, and Excel reports
│   ├── raw_transactions.csv
│   ├── processed_transactions_with_ai.csv
│   └── Executive_Risk_Report.xlsx
│
├── sql/                     # Database definitions and analytical queries
│   ├── schema.sql           # Relational star schema & audit log tables
│   └── analytics.sql        # Advanced SQL queries, window functions & aggregations
│
├── src/                     # Core application source code
│   ├── pipeline.py          # Data generation, cleaning, and AI risk scoring engine
│   ├── load_to_mysql.py     # Database connection and batch insertion loader
│   └── generate_report.py   # Automated styling & conditional formatting Excel exporter
│
