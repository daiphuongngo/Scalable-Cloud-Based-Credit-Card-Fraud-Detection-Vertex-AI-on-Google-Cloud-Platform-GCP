# -*- coding: utf-8 -*-
"""
Created on Sun May  4 19:40:55 2025
@author: phuon
"""

from pyspark.sql import SparkSession
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from google.cloud import storage

# Start Spark session
spark = SparkSession.builder.appName("FraudModelTraining").getOrCreate()

# Load CSV
df = spark.read.option("header", True).option("inferSchema", True).csv(
    "gs://cscie192-phuong-bucket-useast1/final-project/creditcard.csv"
)

# Convert to Pandas
pdf = df.toPandas()

# Drop unnecessary columns
X = pdf.drop(columns=["Class", "Time"], errors="ignore")
y = pdf["Class"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model locally
local_model_path = "/tmp/rf_fraud_model.pkl"
joblib.dump(clf, local_model_path)

# Upload to GCS
bucket_name = "cscie192-phuong-bucket-useast1"
gcs_model_path = "fraud-models/rf_fraud_model.pkl"

client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(gcs_model_path)
blob.upload_from_filename(local_model_path)

print(f"Model uploaded to: gs://{bucket_name}/{gcs_model_path}")
