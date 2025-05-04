# Scalable-Cloud-Based-Credit-Card-Fraud-Detection-Vertex-AI-on-Google-Cloud-Platform-GCP

![Harvard_University_logo svg](https://github.com/user-attachments/assets/cf1e57fb-fe56-4e09-9a8b-eb8a87343825)

![Harvard-Extension-School](https://github.com/user-attachments/assets/59ea7d94-ead9-47c0-b29f-f29b14edc1e0)

## **Master, Data Science**

## CSCI E-192 **Modern Data Analytics** (AWS, GCP)

## Professors: **Edward Sumitra**, **Marina Popova**

## Author: **Dai-Phuong Ngo (Liam)**

## Timeline: January 6th - May 16th, 2025

## Project Goal and Problem Statement

My goal for this project is to develop a scalable and efficient fraud detection pipeline for financial credit card transactions on Google Cloud Platform (GCP) so that customers are not charged for items that they did not purchase. My objective is to identify potentially fradulent transactions in near real-time leveraging multiple supervised learning models from cloud services for which I will retrain and deploy the models automatically as new data arrives.

## Data Source

My selected dataset is provided by publicly available source on Kaggle with a domain in financial credit card transactions, a size of more than 284 thousand records, 30 features and 1 target feature. All contributing features were anonymized with PCA from V1 to V28, Amount, Time and binary labeled target features having 0 for non-fraud and 1 for fraud. This dataset will be uploaded directly to Google Cloud Storage (GCS) and queried through BigQuery for preprocessing, exploration and analytics with charts and statistics.

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

## Expected Results

I expect my work to deliver trained binary classification models deployed on Vertex AI that predicts the probability of a credit card transaction being fraudument. Models to be trained and evaluated include Decision Tree, Random Forest, XGBoost, LightGBM and more if necessary. Furthermore, a simulated new real-time scoring setup using Pub/Sub, Dataflow and Vertex AI Endpoint. 

## Application Overview and Technologies used 

1.	Google Cloud Storage is used for dataset storage including training and testing data.
2.	BigQuery is in usage then for data wrangling, SQL analytics and feature engineering in Python.
3.	Vertex AI is the backbone of Machine Learning model training on Jupyter notebooks in Python (pandas, sklearn, matplotlib) with custom trainings (based on models) or AutoML (if needed). Retraining can be considered on VertexAI when testing data is predicted and deployed before new data comes in. 
4.	Cloud Scheduler, PubSub, Dataflow (probably) are leverage for triggering real-time scoring pipeline.

```
           +--------------------+
           | Google Cloud       |
           | Storage (GCS)      |   
           +--------------------+
                     |
                     v
           +--------------------+
           | BigQuery           |
           | Data Exploration   |
           | + SQL Preprocessing|
           +--------------------+
                     |
                     v
           +--------------------+
           | Vertex AI Workbench|
           | (Notebooks + AutoML|
           | or Custom Model)   |
           +--------------------+
                     |
                     v
           +--------------------+
           | Vertex AI Pipelines|
           | + Model Registry   |
           | + HyperTune (opt)  |
           +--------------------+
                     |
                     v
           +--------------------+
           | Vertex AI Endpoint |
           | for real-time infer|
           +--------------------+
```

## New Stages Used

Some aspects I will examine to put into my project include:

•	Vertex AI Pipelines to automate data ingestion from BigQuery, train, validate, evaluate and deploy models (not convered in the course assignments and I have mentioned above).

•	Vertex AI Model Registry to manage model versions for each model used.

I also plan for simulating real time credit card fraud detection by streaming small data via PubSub and provide real time score with either Cloud Functions or Dataflow which triggers Vertex AI Endpoints.

## Dataset Creation & Analysis in BigQuery

![1 - Create dataset and table in bigquery](https://github.com/user-attachments/assets/6c83b38d-6bc3-4fbd-ade8-c38f2aee215d)

![2 - select first 10](https://github.com/user-attachments/assets/2f9b5cd9-b7dd-4659-bc80-b1ff104ff780)

![2 - select first 10 p2](https://github.com/user-attachments/assets/0962df35-92b1-428a-9b51-0262934d827f)

![3 - Check summary of class](https://github.com/user-attachments/assets/953ac953-c10a-42cf-83cf-e38d657993fa)

![4 - Stats of Amount](https://github.com/user-attachments/assets/1bddef00-d516-4de5-a90e-e4a09a5c84bd)

## Vertex AI Pipeline

### Vertex Workbench Notebook Creation

![5 - Vertex Workbench Notebook Creation](https://github.com/user-attachments/assets/7d2a9c12-7df0-496d-9588-597d626f1773)

### Libraries Setup and Data Loading

![Libraries Setup and Data Loading](https://github.com/user-attachments/assets/8b06cdf4-4583-44ce-9669-b5bbee6676fc)

### Class Distribution

![5 - Vertex Workbench Notebook Creation](https://github.com/user-attachments/assets/324a7b5c-62d2-49f7-a337-caef2de633cd)

### Correlation Matrix

![8 - Correlation Matrix](https://github.com/user-attachments/assets/40a7c697-98c2-431a-8ee0-b6443cf325d7)

### Data Preprocessing, Train Test Split, Handling Class Imbalance with SMOTE, Model Training with Random Forest

![9 - Data Preprocessing, Train Test Split, Handling Class Imbalance with SMOTE, Model Training with Random Forest](https://github.com/user-attachments/assets/f94595dc-0e73-4576-9042-ab9b65f6ba36)

### Model Evaluation

![10 - Model Evaluation](https://github.com/user-attachments/assets/6c33f1e5-9872-42a9-b777-84ec059f9f13)

![10 - Model Evaluation p2](https://github.com/user-attachments/assets/60a14126-7dd3-4be7-898e-d04f4c53a4b9)

### Save and Upload Model to GCS

![11 - Save and Upload Model to GCS](https://github.com/user-attachments/assets/29926ab5-d970-42cd-906b-6f4713729702)




