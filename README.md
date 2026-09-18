# Quantitative-Data-Quality-Risk-Analytics-

This project implements an end-to-end data quality and risk analytics pipeline designed to ingest, sanitize, structurally model, analyze, and report on transactional streams. 

By combining programmatic data cleaning in Python with unsupervised machine learning (Isolation Forest), a fully normalized relational Star Schema in MySQL, advanced SQL window functions, and programmatic Excel report automation, the system bridges the gap between raw data ingestion and executive-level risk visibility.


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
