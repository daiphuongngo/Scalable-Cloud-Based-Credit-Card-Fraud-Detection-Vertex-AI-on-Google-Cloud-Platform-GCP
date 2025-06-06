# Scalable-Cloud-Based-Credit-Card-Fraud-Detection-PySpark-Vertex-AI-on-Cloud-Platforms-GCP-AWS

![Harvard_University_logo svg](https://github.com/user-attachments/assets/cf1e57fb-fe56-4e09-9a8b-eb8a87343825)

![Harvard-Extension-School](https://github.com/user-attachments/assets/59ea7d94-ead9-47c0-b29f-f29b14edc1e0)

## **Master, Data Science**

## CSCI E-192 **Modern Data Analytics** (AWS, GCP)

## Professors: **Edward Sumitra**, **Marina Popova**

## Author: **Dai-Phuong Ngo (Liam)**

## Timeline: January 6th - May 16th, 2025

## Youtube (3-minute highlight): https://youtu.be/02aflw1--Uk

## Project Goal and Problem Statement

My goal for this project is to develop a scalable and efficient fraud detection pipeline for financial credit card transactions on Google Cloud Platform (GCP) so that customers are not charged for items that they did not purchase. My objective is to identify potentially fradulent transactions in near real-time leveraging multiple supervised learning models from cloud services for which I will retrain and deploy the models automatically as new data arrives.

## Data Source

My selected dataset is provided by publicly available source on Kaggle with a domain in financial credit card transactions, a size of more than 284 thousand records, 30 features and 1 target feature. All contributing features were anonymized with PCA from V1 to V28, Amount, Time and binary labeled target features having 0 for non-fraud and 1 for fraud. This dataset will be uploaded directly to Google Cloud Storage (GCS) and queried through BigQuery for preprocessing, exploration and analytics with charts and statistics.

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

## Expected Results

I expect my work to deliver trained binary classification models deployed on Vertex AI that predicts the probability of a credit card transaction being fraudument. Models to be trained and evaluated include Random Forest and more if necessary. Furthermore, a simulated new real-time scoring setup using Pub/Sub will be deployed. On AWS, a simulated real-time predicted scoring triggered by AWS EMR Serverless will be implemented.

## Application Overview and Technologies used 

1.	Google Cloud Storage is used for dataset storage including training and testing data.
2.	BigQuery is in usage then for data wrangling, SQL analytics and feature engineering in Python.
3.	Vertex AI is the backbone of Machine Learning model training on Jupyter notebooks in Python (pandas, sklearn, matplotlib) with custom trainings (based on models) or AutoML (if needed). Retraining can be considered on VertexAI when testing data is predicted and deployed before new data comes in. 
4.	PubSub, Dataproc are leverage for triggering real-time scoring pipeline.

## Processing Pipeline - System Architecture and Design Diagram of GCP and AWS:

```
           +--------------------+
           | Google Cloud       |
           | Storage (GCS)      |
           | old & new data     |   
           +--------------------+
                     |
                     v
           +--------------------+
           | BigQuery           |  [ BigQuery Table via Spark-BigQuery Connector ]	
           | Data Exploration   | <<<<----------------
           | + SQL Preprocessing|                    ^
           +--------------------+                    ^
                     |                               ^
                     v                               |
           +--------------------+                    |
           | Vertex AI Workbench|                    |
           | (Jupyter + Colab   |                    |  [ Pub/Sub Topic: "fraud-alerts" via Dataproc job]    
           | in PySpark)        |                    | 
           +--------------------+                    |
                     |                               |
                     v                               |
           +--------------------+                    |
           | Vertex AI Endpoint |                    |
           | for real-time infer|----------------->>>x<<<<-----------[Cloud Scheduler setup]
           | Dataproc, Pub Sub  |
           +--------------------+
```
![ChatGPT Image May 20, 2025, 01_32_41 AM](https://github.com/user-attachments/assets/61a68816-e302-4cc9-b481-98029fd040c8)

• Model Training: I trained the RandomForestClassifier using sklearn on Vertex AI Workbench’s Jupyter notebook and saved as .pkl to GCS. An alternative method is coding in PySpark in a train_model.py file saved in GCS folder that could be used and run via Dataproc to generate the model’s .pkl file stored in GCS.

• Prediction: Via Dataproc job run, PySpark job reads test data (10 testing rows without Target feature), applies the model, scores each row.

• Publishing: Results are published to Pub/Sub as fraud alerts in JSON format.

• Storage: When the model scored data, the output will be written via Dataproc job run to BigQuery for further analysis.

• Scheduling: When time arrives as scheduled, the fraud detection request at scheduled time will be triggered to run Pub/Sub job that launches the Dataproc job which runs Pyspark Random Forest prediction using Random Forest model and the new data in GCS, and receives fraude alerts in Pub/Sub and Big Query.


![ChatGPT Image May 16, 2025, 02_32_56 AM](https://github.com/user-attachments/assets/95be2edf-b319-4cb5-92d5-fb2ceec7d924)



## Implementation
							 					
My Technologies Used include: 

•	Google Cloud Platform: ``GCS``, ``BigQuery``, ``Pub/Sub``, ``Dataproc``, ``Vertex AI``

•	AWS: `S3`, `EMR Serverless`, `Glue`, `Athena`

•	Programming Languages: ``Python``, ``PySpark``, ``SQL``

•	Libraries: scikit-learn, pandas, joblib, google-cloud-pubsub, google-cloud-storage

My Step-by-step Highlights on GCP include:

1.	Uploaded dataset to GCS

2.	Used BigQuery for preprocessing & EDA

3.	Trained and saved an sklearn RandomForestClassifier on local Jupyter or Vertex AI Jupyter:

4.	Deployed PySpark jobs on Dataproc’s job using train_model.py:

•	Read test data

•	Loaded model from GCS with joblib

•	Applied model and generated predictions

5.	Published alerts to Pub/Sub via Dataproc’s job using fraud_pubsub_bigquery_job.py

6.	Saved full scored dataset to BigQuery table (fraud_alert_dataset2.fraud_alert_table)

7.	Troubleshot schema compatibility (resolved INT64 → use "INT" or "BIGINT")

8.	Verified Pub/Sub + BigQuery integration

9.	Scheduled Cloud Scheduler job that triggers Pub/Sub laurching the preset Dataproc job

My Step-by-step Highlights on AWS include:

1. Data Ingestion into Amazon S3

2. Model Training with PySpark via EMR Serverless

3. Prediction Job with EMR Serverless

4. Schema Discovery with AWS Glue Crawler

5. Query Results with Amazon Athena

| Component                | AWS Service              | Purpose                                  |
| ------------------------ | ------------------------ | ---------------------------------------- |
| Data Storage             | Amazon S3                | Store raw, intermediate, and output data |
| Model Training           | EMR Serverless (PySpark) | Train fraud detection model              |
| Prediction               | EMR Serverless (PySpark) | Generate predictions and save results    |
| Metadata Catalog         | AWS Glue Crawler         | Discover schema from S3 output           |
| Data Catalog & Query     | Glue + Athena            | Query prediction results via SQL         |
| Visualization (optional) | Amazon QuickSight        | Create fraud dashboards                  |

## Results on GCP:

Here are the results of my Credit Card Fraud Detection project:

•	Model Development with Vertex AI Workbench and PySpark 

•	Spark job logs showing successful execution via Dataproc

•	Output df.show() confirming predicted results on Colab Enterprise

•	Pub/Sub messages showing published fraud alerts

•	BigQuery tables with full output of fraud alert and fraud classification 

## Results on AWS:

| AWS Component    | Output Type             | Description                                            |
| ---------------- | ----------------------- | ------------------------------------------------------ |
| S3 (model)       | Spark MLlib model       | Trained classifier persisted in directory structure    |
| S3 (predictions) | CSV                     | Scored results with fraud probability                  |
| Glue             | Database + Table        | Metadata for Athena to read structured prediction data |
| Athena           | SQL Query Results       | View and export high-risk transactions                 |
| EMR              | Logs & Completion Flags | Training + inference run statuses                      |


## Bonus Option

•	I used Pub/Sub for real-time or near real-time scoring alerts.

•	I also integrated Spark-BigQuery Connector, which was not covered in assignments.

•	I also added Vertex AI model / PySpark model loading via GCS.

•	I simulated streaming fraud detection and storage for audit that are highly applicable for real world usage.

## Conclusions and Lesson Learned

**Lessons Learned**:

•	Understood practical setup of an end-to-end fraud detection pipeline using Spark.

•	Learned to work with GCP services integration (Pub/Sub, BigQuery, Vertex AI, Dataproc, GCS) and AWS Services Integration (S3, Athena, Glue, EMR Serverless).

•	Gained experience with schema compatibility and PySpark casting issues.

**Challenges**:

•	Schema mismatch between PySpark and BigQuery that I have acknowledged and resolved with matching schema for both.

•	INT64 data type not directly usable which I resolved using "BIGINT" or "LongType" in PySpark.

•	Latency and errors in Pub/Sub delivery required manual subscription testing that I tested to ensure correct schema, extraction point and destination point.

**Future Improvements**:

•	Add more components of Vertex AI Pipelines and AWS SageMajer for more automatic model retraining and registry.

•	Replace PySpark with Dataflow for real-time data processing, instead of near real-time processing.

•	Visualize fraud statistics via GCP Looker Studio / Tableau / AWS QuickSight if the test data was given with more data records for statistical analysis and inference.

•	Extend to a multi-class or unsupervised fraud detection setup.

# Fraud Detection Pipeline:

## Dataset Creation & Analysis in BigQuery

![1 - Create dataset and table in bigquery](https://github.com/user-attachments/assets/6c83b38d-6bc3-4fbd-ade8-c38f2aee215d)

![2 - select first 10](https://github.com/user-attachments/assets/2f9b5cd9-b7dd-4659-bc80-b1ff104ff780)

![2 - select first 10 p2](https://github.com/user-attachments/assets/0962df35-92b1-428a-9b51-0262934d827f)

![3 - Check summary of class](https://github.com/user-attachments/assets/953ac953-c10a-42cf-83cf-e38d657993fa)

![4 - Stats of Amount](https://github.com/user-attachments/assets/1bddef00-d516-4de5-a90e-e4a09a5c84bd)

## Vertex AI Pipeline

Here is a detailed explanation of my fraud detection model pipeline using Vertex AI and GCP, based on the first 10 screenshots I've shared:

---

### **Fraud Detection Model Pipeline Using Google Cloud Platform & Vertex AI**

This project demonstrates an end-to-end machine learning pipeline for credit card fraud detection using Google Cloud Platform (GCP), leveraging **BigQuery**, **Vertex AI Workbench**, and **GCS** (Google Cloud Storage) as well as **Pub/Sub** and **Dataproc**.

---

### **1. Vertex AI Workbench Notebook Setup**
![5 - Vertex Workbench Notebook Creation](https://github.com/user-attachments/assets/acf67aab-db36-490e-9310-5a23d70f9f80)

- A **Vertex AI Workbench** instance named `fraud-detection-notebook` was created using the `e2-standard-4` machine type (4 vCPUs, 16 GB RAM), running Python 3 (Intel MKL).
- This notebook serves as the central environment for data preprocessing, training, evaluation, and integration with BigQuery and GCS.

---

### **2. External Table Creation in BigQuery**
![1 - Create dataset and table in bigquery](https://github.com/user-attachments/assets/659746d4-f21d-4646-89fd-5bbd34b2f2d5)

- An **external table** was created using a CSV file stored in a GCS bucket. The file `creditcard.csv` was linked via URI using `CREATE OR REPLACE EXTERNAL TABLE` with the option `format='CSV'` and `skip_leading_rows=1`.
- This approach enables query execution without duplicating data into BigQuery’s native storage, thus reducing cost and maintaining data freshness.

---

### **3. Previewing the Dataset**
![2 - select first 10](https://github.com/user-attachments/assets/6671e052-69ad-46a3-bfe7-2d894a63d285)

![2 - select first 10 p2](https://github.com/user-attachments/assets/bad14a37-e76e-424d-a1be-b1e0a86244ae)

- A query was run to view the **first 10 rows** from the external table. This helps verify the schema and data integrity immediately after setup.

---

### **4. Class Distribution Summary**
![3 - Check summary of class](https://github.com/user-attachments/assets/d737964c-a573-4ad0-9ec4-386a7350c79c)

- A class distribution check (`SELECT Class, COUNT(*) GROUP BY Class`) was executed.
- Output: There are **284,315 non-fraudulent (Class=0)** and **492 fraudulent (Class=1)** transactions, highlighting the **severe class imbalance** common in fraud datasets.

---

### **5. Basic Statistics of 'Amount' Column**
![4 - Stats of Amount](https://github.com/user-attachments/assets/08de09b0-df7e-4734-86fd-ca4410a44e24)

- A simple aggregation query retrieved the **average and standard deviation** of the `Amount` field.
- This helped understand the transaction value distribution and prepare for scaling during preprocessing.

---

### **6. Data Exploration**
![8 - Correlation Matrix](https://github.com/user-attachments/assets/e2419d1a-2ec6-4947-936b-2465ed839252)

- A **correlation matrix heatmap** was created to visualize relationships among features and identify any multicollinearity. PCA-transformed variables (V1 to V28) show weak correlations, as expected from anonymized data.

---

### **7. Class Imbalance Visualization**
![7 - Class Distribution](https://github.com/user-attachments/assets/cb8da513-d54a-4e9a-8c6f-c325aac30fbb)

- A bar plot confirms the **high imbalance**, reinforcing the need to apply resampling techniques such as SMOTE.

---

### **8. Preprocessing and Train-Test Split**
![9 - Data Preprocessing, Train Test Split, Handling Class Imbalance with SMOTE, Model Training with Random Forest](https://github.com/user-attachments/assets/16d53701-7de5-4128-93de-9a0b66a65722)

- The **Time** column was dropped, and the **Amount** column was standardized using `StandardScaler`.
- The dataset was split using stratified sampling (80% training, 20% testing) to preserve class ratio across splits.

---

### **9. Class Imbalance Handling with SMOTE**
![9 - Data Preprocessing, Train Test Split, Handling Class Imbalance with SMOTE, Model Training with Random Forest](https://github.com/user-attachments/assets/16d53701-7de5-4128-93de-9a0b66a65722)
- **SMOTE (Synthetic Minority Oversampling Technique)** was applied to the training data to synthetically generate minority class (fraud) samples, helping mitigate the class imbalance issue before model training.

---

### **10. Model Training and Evaluation (Random Forest)**
![10 - Model Evaluation](https://github.com/user-attachments/assets/013fad6b-63c2-4992-8f47-1e817aab71b1)

![10 - Model Evaluation p2](https://github.com/user-attachments/assets/23686cd2-14e3-42d7-8e11-4a7e0ade88d8)

- A **Random Forest Classifier** was trained on the resampled dataset. Evaluation was done using:
  - **Classification Report** (Precision, Recall, F1-score)
  - **Confusion Matrix**
  - **ROC-AUC Score** and ROC Curve
- Results show high accuracy and strong fraud detection capability:
  - **Precision:** 0.87 (fraud), 1.00 (non-fraud)
  - **Recall:** 0.83 (fraud), 1.00 (non-fraud)
  - **ROC AUC Score:** ~0.99
- The model performs exceptionally well, considering the original class imbalance.

---

### 11. **Creating a Dataproc Cluster**
A Dataproc cluster named `cluster-fraud-detection-useast` was created with 1 master and multiple workers, optimized for Spark jobs.
![12 - Create Dataproc Cluster](https://github.com/user-attachments/assets/c0bfd95e-e2d5-4878-8b9d-d4d2d241cf8e)


---

### 12. **Training with Dataproc Job**
The training script (`train_model.py`) was submitted as a **PySpark job** to the Dataproc cluster.
![13 - Retrain model with Dataproc vs GCS to fit the libraries version](https://github.com/user-attachments/assets/ca4413bc-44df-4541-b806-707db6aabe13)

![13 - Retrain model with Dataproc vs GCS to fit the libraries version (succeeded)](https://github.com/user-attachments/assets/c566bfb9-5354-4c67-9091-80a1709b4c1f)

Once successful, the updated model was verified in GCS.
![14 - Succeeded retraining the model](https://github.com/user-attachments/assets/9d88a6f3-ce20-4473-ad30-060dc40dfe35)

![15 - Check if the retrained model is updated in GCS](https://github.com/user-attachments/assets/41cbac2b-0cd5-4751-a39f-4730563ad415)

---

### 13. **Prediction Job on New Data**
- Another PySpark job (`job.py`) was submitted to predict on a new dataset.
- The prediction job succeeded, and the results were stored in a new BigQuery table:
  ```
  csci-e192-project-452505.fraud_detection_dataset.fraud_predictions
  ```
![16 - Run job to predict on new input](https://github.com/user-attachments/assets/018f7d31-6249-4cf2-9b1b-ec1fab30757a)

![17 - Completed the job predicting new data successfully](https://github.com/user-attachments/assets/05c2f656-b9d0-48db-935f-bd2db996489f)
---

### 14. **Verifying Predictions in BigQuery**
A query confirmed that predictions were written successfully with `predicted_proba` and `predicted_class` for each transaction.
![18 - Checking the BigQuery table of newly predicted output](https://github.com/user-attachments/assets/d7033dc4-ceb1-430d-b581-024d6f170ce2)

---

## Notes of current progress
This pipeline demonstrates a complete **ML lifecycle on GCP**:
- Scalable data processing with **Dataproc**
- ML experimentation using **Vertex AI Workbench**
- Model deployment and versioning in **Cloud Storage**
- Batch inference jobs using **PySpark**
- Persistent storage of results in **BigQuery**

---

### **15. Model Prediction & Output Storage in GCS**
- **Colab Notebook**: I loaded and displayed predicted output files using `gcsfs` and `pandas` from:
  ```
  gs://cscie192-phuong-bucket-useast1/final-project/prediction_output/part-*
  ```
- The predictions contain features (V1–V28), `Amount`, `predicted_proba`, and `predicted_class`.

- **GCS Confirmation**:
  - Two part files and a `_SUCCESS` flag confirm successful Spark output write.
  - Timestamped May 4, 2025, 8:17 PM.

![train_model_job](https://github.com/user-attachments/assets/37654109-36fe-482a-8aa7-2a1f4d349bc5)

![19 - Check the GCS results of predicted output](https://github.com/user-attachments/assets/dbb50f59-daed-45cd-9b5a-e263d11e9d38)

---

### **16. Verification in BigQuery**
- I created a table:
  ```
  fraud_detection_dataset.fraud_predictions
  ```
- The schema includes all 28 features, amount, `predicted_proba`, and `predicted_class`.

- A query:
  ```sql
  SELECT * FROM `fraud_detection_dataset.fraud_predictions` LIMIT 100;
  ```
  confirms expected prediction results - with fraud predictions (`predicted_class = 1`) having high `predicted_proba`.

![20 - Colab check GCS outputs part 1](https://github.com/user-attachments/assets/efec7c72-47d4-42e7-878f-5664adfde8e3)

![20 - Colab check GCS outputs part 2](https://github.com/user-attachments/assets/136dd94d-9782-4899-8a32-a0afae416ca3)


---

### **17. Pub/Sub + Dataproc Job for Real-time Alerting**
- **Job `fraud_pubsub_job` succeeded**, reading new data, predicting fraud, and writing results back to:
  ```
  gs://.../prediction_output/
  ```

- **Another job `job-pubsub-bigquery4`** confirms:
  - Messages (fraud predictions) were published to a **Pub/Sub topic**.
  - I successfully used Spark to push predictions to Pub/Sub:
    ```
    Published message: {"transaction_id": ..., "score": ..., "label": ...}
    ```
![21 - Create sub](https://github.com/user-attachments/assets/0e1405f6-9b94-40be-9381-a300e1eb32c1)



---

### **18. Pub/Sub Subscription & Dataproc Job for BigQuery Alerts**
- I created a **subscription `fraud-subscription`** to the topic `fraud-alerts`.

![21 - Created sub](https://github.com/user-attachments/assets/bb85f5ff-5e52-4960-8787-c9811be88bee)

![22 - Completed Dataproc job for sub to BigQuery](https://github.com/user-attachments/assets/6a5a0044-6fae-4b60-a502-aa8571d1c64f)

![fraud_pubsub_job](https://github.com/user-attachments/assets/824d168f-ed40-407d-9063-5a5ea5237eea)

![23 - Completed pubsub to bigquery](https://github.com/user-attachments/assets/ebb04d96-f8b4-493f-a92f-b8754239c294)

- This subscription was configured to:
  - **Delivery type**: Write directly to BigQuery.
  - **Target table**: `fraud_alert_dataset2.fraud_alert_table`.
  - Schema: Uses the **table schema**.

- **BigQuery table `fraud_alert_table`** exists and will capture streaming alerts from Pub/Sub for downstream usage or visualization.

![24 - BigQuery fraud detection dataset and table](https://github.com/user-attachments/assets/dd7bbf1a-1315-4bdf-b475-1ba3a4ef24fc)

![24 - BigQuery fraud detection table as alert](https://github.com/user-attachments/assets/064debce-4b57-4fa3-8b94-ee72685d3b53)

![Edit Schema for fraud alert table](https://github.com/user-attachments/assets/f3692d14-b9e0-4aa5-8e5e-0b8720f8bee6)

![Succeeded in writing to PubSub and BigQuery](https://github.com/user-attachments/assets/79f963af-df3c-4982-8b7f-1ad72ff721a5)

![Wrote alert to BigQuery](https://github.com/user-attachments/assets/17c7cc92-d214-4bd9-827f-68cab98c2c79)

---

### **19. Cloud Scheduler schedules the Pub/Sub everyday at 6AM EDT**:
![Create GCP Cloud Scheduler Job](https://github.com/user-attachments/assets/46d63816-1494-4301-a1c4-cc2fb9f6bd5a)

![Scheduler result](https://github.com/user-attachments/assets/e1af5455-f982-4260-af86-cf437df646c8)

### **20. Summary of Pipeline Flow**
Here’s the **end-to-end data pipeline** I built:

1. **Dataproc Job** → Predict fraud on input data.
2. **Output stored** → GCS (`prediction_output/`).
3. **Prediction results loaded** → into BigQuery `fraud_predictions`.
4. **Streamed output** → Published to Pub/Sub (`fraud-alerts` topic).
5. **Subscription** → Pushes Pub/Sub messages to `fraud_alert_table` in BigQuery.
6. **Dataproc Job** → Record fraud alert in BigQuery when Pub/Sub messages are triggered.
7. **BigQuery alerts table** → Can now be visualized or queried for fraud monitoring.
8. **Cloud Scheduler** → Trigger Pub/Sub job at scheduled 6AM EDT for fraud detection schedule.

# AWS Pipeline

Here's a **full step-by-step explanation** of my **fraud detection pipeline on AWS**, from ingesting CSV data in S3 to running PySpark in EMR Serverless, storing schema in Glue, and querying via Athena:

---

### **System Architecture Overview**

---

### 📌 **Step-by-Step Explanation**

---

### **1. Data Ingestion into Amazon S3**

* **What happens:** I upload raw or processed CSV files (like `creditcard_sample.csv`, `sample_test_data.csv`, and `prediction_output/*.csv`) to an Amazon S3 bucket (`s3://daiphuongcscie192/credit_card_fraud_detection/`).
* **Purpose:** Acts as my raw and intermediate data lake storage.

![AWS S3](https://github.com/user-attachments/assets/d0cc8a11-7387-4158-a89a-9eb7954db9b0)

---

### **2. Model Training with PySpark via EMR Serverless**

* **Trigger:** I run a PySpark job (e.g., `AWS_train_model.py`) using EMR Serverless.

* **Script activities:**

  * Load training data from S3.
  * Preprocess and vectorize features.
  * Train a `RandomForestClassifier` using PySpark MLlib.
  * Save the trained model using `.save()` to a specific S3 path (`models/spark_rf_model`).

* **Why EMR Serverless:** No need to manage clusters; it dynamically provisions compute and scales based on job load.

![AWS train model py](https://github.com/user-attachments/assets/4440ac63-bc3d-401f-9094-3ea3b9f0efba)

![AWS EMR train model](https://github.com/user-attachments/assets/356d36cc-786c-4b9e-9d43-9a2d50dd80a0)

---

### **3. Prediction Job with EMR Serverless**

* **Trigger:** A second PySpark job (e.g., `predict_fraud.py`) runs using the trained model.
* **Script activities:**

  * Loads test data (`sample_test_data.csv`) from S3.
  * Loads the saved model from `models/spark_rf_model`.
  * Generates predictions with fraud probabilities.
  * Saves output to `s3://.../prediction_output/` as CSV.

![AWS predict model py](https://github.com/user-attachments/assets/6c1ee711-ab24-4ea5-8d39-c8855597e5f4)

![EMR prediction](https://github.com/user-attachments/assets/bd96d50f-319c-4743-9e63-8b4c736447c1)

![AWS prediction output](https://github.com/user-attachments/assets/734a24c5-fd35-4764-835a-3d97a54dcd4c)

---

### **4. Schema Discovery with AWS Glue Crawler**

* **Action:** I create and run a **Glue crawler** (`fraud_prediction_crawler`) pointed at the `prediction_output/` prefix in S3.
* **Outcome:**

  * Glue automatically infers schema (columns like `Time`, `predicted_class`, `fraud_score`).
  * Creates a Glue **table** in a Glue **database** (e.g., `fraud_detection_db`).
  * This table acts as metadata for Athena to query structured output.

![AWS Glue crawler](https://github.com/user-attachments/assets/5299f0d9-bae1-4d68-a98f-89590b10a8d7)

![AWS Glue Table](https://github.com/user-attachments/assets/c0002bd4-acde-4a05-b1c3-7b2a527d1f6a)

---

### **5. Query Results with Amazon Athena**

* **Action:** In Athena, I connect to the Glue Data Catalog, select the `fraud_detection_db`, and query the table using standard SQL.

  ```sql
  SELECT * FROM fraud_detection_db.prediction_output
  ORDER BY fraud_score DESC
  ```

![AWS Athena](https://github.com/user-attachments/assets/378b67a4-a228-4bba-912c-463d055b4970)

* **Benefits:**

  * No infrastructure to manage.
  * Near-instant ad hoc analysis of fraud predictions.

---

### **Future Improment (Next Steps)**

You can now integrate with:

* **QuickSight:** For dashboarding and visualizations.
* **OpenSearch / DynamoDB:** For real-time querying or alerting.
* **CloudWatch:** To log job statuses, monitor Glue jobs, or EMR job failures.

---


