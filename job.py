# -*- coding: utf-8 -*-
"""
Dataproc Job: Predict Fraud using Trained Random Forest Model
"""

from pyspark.sql import SparkSession
import pandas as pd
import joblib
from google.cloud import storage
from io import BytesIO

# Init Spark
spark = SparkSession.builder.appName("FraudPrediction").getOrCreate()

# Load sample test data from GCS
df = spark.read.option("header", True).option("inferSchema", True).csv(
    "gs://cscie192-phuong-bucket-useast1/final-project/sample_test_data.csv"
)

# Convert to Pandas
pdf = df.toPandas()

# Drop unnecessary columns for prediction
X = pdf.drop(columns=["Time", "Class"], errors="ignore")

# Load model from GCS
client = storage.Client()
bucket = client.get_bucket("cscie192-phuong-bucket-useast1")
blob = bucket.blob("fraud-models/rf_fraud_model.pkl")
model_bytes = blob.download_as_bytes()
model = joblib.load(BytesIO(model_bytes))

# Predict
pdf["predicted_proba"] = model.predict_proba(X)[:, 1]
pdf["predicted_class"] = model.predict(X)

# Convert to Spark DataFrame for BigQuery or GCS output
spark_df = spark.createDataFrame(pdf)

# Save to BigQuery
spark_df.write.format("bigquery") \
    .option("temporaryGcsBucket", "cscie192-phuong-bucket-useast1") \
    .option("table", "csci-e192-project-452505.fraud_detection_dataset.fraud_predictions") \
    .mode("append") \
    .save()

# Also save to GCS
spark_df.write.option("header", True).mode("overwrite").csv(
    "gs://cscie192-phuong-bucket-useast1/final-project/prediction_output"
)
