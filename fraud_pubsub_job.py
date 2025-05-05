from pyspark.sql import SparkSession
from google.cloud import pubsub_v1
import json

# Initialize Spark
spark = SparkSession.builder.appName("FraudPubSubJob").getOrCreate()

# Load predictions from GCS

df = spark.read.option("recursiveFileLookup", "true").csv(
    "gs://cscie192-phuong-bucket-useast1/final-project/prediction_output/", 
    header=True
)

# Inspect first few rows
df.show(10)

# Convert to Pandas to loop over results (efficient for small batch jobs)
rows = df.toPandas()

# Set Pub/Sub details
project_id = "csci-e192-project-452505"
topic_id = "fraud-alerts"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Loop and publish each fraud alert
for index, row in rows.iterrows():
    message_dict = {
        "transaction_id": row.iloc[0],      # Time
        "score": float(row.iloc[-2]),       # predicted_proba
        "label": int(float(row.iloc[-1]))   # predicted_class
    }
    message_json = json.dumps(message_dict).encode("utf-8")
    future = publisher.publish(topic_path, data=message_json)
    print(f"Published message: {message_dict}")


print("✅ All fraud predictions published to Pub/Sub.")
