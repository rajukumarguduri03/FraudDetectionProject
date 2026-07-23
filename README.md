# ML Fraud Detection Dashboard

## Overview

An end-to-end machine learning fraud detection system that identifies suspicious financial transactions and provides explainable predictions using SHAP.

## Problem Statement

Financial institutions lose billions due to fraudulent transactions.
This project detects fraud automatically using machine learning classification models.

## Technologies

- Python
- Scikit-learn
- Random Forest
- XGBoost
- SMOTE
- StandardScaler
- SHAP
- Flask
- HTML/CSS/JavaScript
- Chart.js

## ML Pipeline

Dataset
↓
Data Preprocessing
↓
Feature Scaling
↓
SMOTE Balancing
↓
Model Training
↓
Evaluation
↓
SHAP Explainability
↓
Flask Deployment
↓
Dashboard

## Features

✔ CSV transaction upload  
✔ Fraud prediction  
✔ Fraud probability score  
✔ Fraud statistics dashboard  
✔ Explainable AI using SHAP  

## How to Run

Install dependencies:

pip install -r requirements.txt

Run:

python app.py

Open:

http://127.0.0.1:5000 

## Dataset

This project uses the Credit Card Fraud Detection dataset.

Dataset source:
Kaggle - Credit Card Fraud Detection Dataset

The dataset contains:
- 284,807 transactions
- 30 features
- Target variable: Class
  - 0 → Normal transaction
  - 1 → Fraud transaction

Features:
- Time
- Amount
- V1 to V28 (PCA transformed features)

Due to GitHub file size limitations, the dataset is not included in this repository.

To run the project:
1. Download the dataset.
2. Place the CSV file inside the `uploads/` folder.
3. Run the Flask application.


