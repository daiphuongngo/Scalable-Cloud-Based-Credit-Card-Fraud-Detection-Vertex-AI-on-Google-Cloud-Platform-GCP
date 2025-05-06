CREATE OR REPLACE EXTERNAL TABLE `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
OPTIONS (
  format = 'CSV',
  uris = ['gs://cscie192-phuong-bucket-useast1/final-project/creditcard.csv'],
  skip_leading_rows = 1
);

-- View of the first 10 rows
SELECT * FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw` LIMIT 100;

-- Check Summary of Class
SELECT Class, COUNT(*) FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw` GROUP BY Class;

-- Statistics of Amount
SELECT AVG(Amount), STDDEV(Amount) FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`;

--  1. Fraud Transactions by Day
SELECT 
  DATE(TIMESTAMP_SECONDS(CAST(Time AS INT64))) AS txn_date,
  COUNT(*) AS fraud_count,
  SUM(Amount) AS total_fraud_amount
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
GROUP BY txn_date
ORDER BY txn_date;

--  2. Fraud Transactions by Hour of Day
SELECT 
  EXTRACT(HOUR FROM TIMESTAMP_SECONDS(CAST(CAST(Time AS FLOAT64) AS INT64))) AS hour_of_day,
  COUNT(*) AS fraud_count,
  SUM(Amount) AS total_fraud_amount
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- 3. Fraud by Month (only if you added a timestamp field)
SELECT 
  FORMAT_DATE('%Y-%m', DATE(TIMESTAMP_SECONDS(CAST(Time AS INT64)))) AS year_month,
  COUNT(*) AS fraud_count,
  SUM(Amount) AS total_fraud_amount
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
GROUP BY year_month
ORDER BY year_month;

-- 4. Top 5% of Fraud Transactions by Amount (Quantile)
SELECT *
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
  AND Amount >= (
    SELECT APPROX_QUANTILES(Amount, 100)[95]
    FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
    WHERE Class = 1
  )
ORDER BY Amount DESC;

-- 5. Top Average Fraud Amount per Hour
SELECT 
  EXTRACT(HOUR FROM TIMESTAMP_SECONDS(CAST(Time AS INT64))) AS hour_of_day,
  AVG(Amount) AS avg_fraud_amount,
  COUNT(*) AS fraud_txns
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
GROUP BY hour_of_day
ORDER BY avg_fraud_amount DESC;

-- Create new table from raw data
CREATE OR REPLACE EXTERNAL TABLE `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw_string`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  autodetect = FALSE,
  uris = ['gs://cscie192-phuong-bucket-useast1/final-project/creditcard.csv']
);

--  1. Fraud Count and Total Amount by Hour Bins
SELECT 
  FLOOR(Time / 3600) AS hour_bin,
  COUNT(*) AS fraud_count,
  SUM(Amount) AS total_fraud_amount
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
GROUP BY hour_bin
ORDER BY hour_bin;

-- 2. Top 10 Largest Fraud Transactions
SELECT *
FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
WHERE Class = 1
ORDER BY Amount DESC
LIMIT 10;

--  3. Fraud Amount Distribution by Quantile Bucket
SELECT quantile_bucket, COUNT(*) AS count, AVG(Amount) AS avg_amount
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY Amount DESC) AS quantile_bucket
  FROM `csci-e192-project-452505.credit_card_fraud_detection.fraud_raw`
  WHERE Class = 1
)
GROUP BY quantile_bucket
ORDER BY quantile_bucket;

