# -*- coding: utf-8 -*-
"""
Created on Sun May  4 21:05:21 2025

@author: phuon
"""

from pyspark.sql import SparkSession
import pandas as pd
import joblib
from google.cloud import storage, pubsub_v1
from io import BytesIO
import json

# Init Spark
spark = SparkSession.builder.appName("FraudPredictionPubSub").getOrCreate()

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

# Publish fraud alerts to Pub/Sub
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("csci-e192-project-452505", "fraud-alerts")

fraud_cases = pdf[pdf["predicted_class"] == 1]
for _, row in fraud_cases.iterrows():
    message_data = row.to_json()
    publisher.publish(topic_path, data=message_data.encode("utf-8"))

# Save to GCS
spark_df = spark.createDataFrame(pdf)
spark_df.write.option("header", True).mode("overwrite").csv("gs://cscie192-phuong-bucket-useast1/final-project/prediction_output")
