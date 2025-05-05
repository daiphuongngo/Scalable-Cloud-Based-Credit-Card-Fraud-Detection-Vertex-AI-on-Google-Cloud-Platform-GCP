from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from google.cloud import pubsub_v1
import json

# 1. Start Spark session
spark = SparkSession.builder \
    .appName("FraudPubSubToBigQueryJob") \
    .getOrCreate()

# 2. Load prediction output from GCS
df = spark.read.option("recursiveFileLookup", "true") \
    .option("header", "true") \
    .csv("gs://cscie192-phuong-bucket-useast1/final-project/prediction_output/")

df.show(5)

# 3. Convert to correct types for BigQuery compatibility
df_casted = df.select(
    col("Time").cast("long"),
    *[col(f"V{i}").cast("double") for i in range(1, 29)],
    col("Amount").cast("double"),
    col("predicted_proba").cast("double"),
    col("predicted_class").cast("long")
)

# 4. Publish to Pub/Sub
rows = df_casted.toPandas()

project_id = "csci-e192-project-452505"
topic_id = "fraud-alerts"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

fraud_rows = rows[rows["predicted_class"] == 1]

for _, row in fraud_rows.iterrows():
    message_dict = {
        "transaction_id": int(row["Time"]),
        "score": float(row["predicted_proba"]),
        "label": int(row["predicted_class"])
    }
    publisher.publish(topic_path, data=json.dumps(message_dict).encode("utf-8"))
    print(f"✅ Published: {message_dict}")

# 5. Write to BigQuery
df_casted.write \
    .format("bigquery") \
    .option("table", "csci-e192-project-452505.fraud_alert_dataset2.fraud_alert_table") \
    .option("writeMethod", "direct") \
    .mode("append") \
    .save()

print("✅ All records written to BigQuery.")
