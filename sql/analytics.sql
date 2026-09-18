USE risk_analytics_db;

--EXECUTIVE RISK DASHBOARD: Summary of Flagged AI Anomalies vs Normal--
SELECT 
CASE WHEN is_flagged_anomaly = 1 THEN 'High RISK / Anomaly' ELSE 'STANDARD' END AS risk_category,
COUNT(transaction_id) AS total_transactions,
ROUND(SUM(amount), 2) AS total_transaction_volume,
ROUND(AVG(amount), 2) AS average_transaction_amount,
ROUND(AVG(anomaly_score), 4) AS avg_model_confidence_score
FROM fact_transactions
GROUP BY risk_category;

--VENDOR RISK EXPOSURE ANALYSIS (Multi-Table JOIN & Aggregations)--
--Identifies which vendors handle the highest monetary volume and carry the most risk--
SELECT 
    v.vendor_id,
    v.vendor_name,
    v.vendor_category,
    COUNT(f.transaction_id) AS transaction_count,
    ROUND(SUM(f.amount), 2) AS total_exposure_amount,
    SUM(f.is_flagged_anomaly) AS flagged_anomaly_count
FROM fact_transactions f
JOIN dim_vendors v ON f.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name, v.vendor_category
ORDER BY total_exposure_amount DESC;

--CUSTOMER RISK & SPENDING RANKINGS (Advanced Window Functions)--
--Ranks customers by their total spend and flags top high-value accounts using window functions--
WITH CustomerSpend AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.country,
        COUNT(f.transaction_id) AS total_transactions,
        SUM(f.amount) AS total_spend,
        SUM(f.is_flagged_anomaly) as customer_flagged_count
    FROM fact_transactions f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name, c.country
)
SELECT 
    customer_id,
    customer_name,
    country,
    total_transactions,
    ROUND(total_spend, 2) AS total_spend,
    customer_flagged_count,
    RANK() OVER (ORDER BY total_spend DESC) AS spending_rank
FROM CustomerSpend;

--DATA QUALITY & PIPELINE AUDIT REPORT--
--Evaluates pipeline health and error logs captured during ingestion--
SELECT 
    error_timestamp,
    file_name,
    error_message,
    rows_affected
FROM pipeline_error_logs
ORDER BY error_timestamp DESC;