# Tech Sales Analytics Platform

## Overview

Tech Sales Analytics Platform is an end-to-end Business Intelligence, Forecasting and Machine Learning solution built with Python and Streamlit.

The platform was designed to transform raw sales data into actionable business insights through advanced analytics, predictive modeling and executive reporting.

---

## Main Features

### Business Intelligence

* Executive Dashboard
* Commercial Geography Analysis
* Product Intelligence
* Business Health Score
* Executive Command Center
* Seasonality Analysis

### Machine Learning

* K-Means Customer/Product Segmentation
* Anomaly Detection
* XGBoost Forecasting
* Random Forest Benchmarking
* Predictive Model Evaluation

### Forecasting

* 30 / 60 / 90 Day Sales Forecast
* Confidence Bands
* Trend Analysis
* Forecast vs Actual Comparison
* Backtesting and MAPE Evaluation

### AI Insights

* CFO Copilot
* Executive Narratives
* Business Risks Detection
* Growth Opportunities Identification
* Actionable Recommendations

---

## Data Requirements

The platform expects an Excel file containing the following columns:

| Column    |
| --------- |
| fecha     |
| pais      |
| ciudad    |
| categoria |
| producto  |
| cantidad  |
| total     |
| utilidad  |

---

## Project Architecture

app.py

pages/

* Dashboard
* Geography
* KMeans
* Anomalies
* Forecast Center
* AI Insights
* RFM
* Ranking Intelligence
* Predictive Models
* What If Simulator
* Business Health
* Product Intelligence
* Command Center
* Seasonality Analysis
* Executive Report

models/

* forecast.py
* predictive.py
* kmeans.py
* anomalies.py

data/

* ventas.xlsx

utils.py

---

## Technology Stack

* Python
* Streamlit
* Pandas
* Plotly
* Scikit-Learn
* XGBoost
* OpenPyXL
* ReportLab

---

## Business Objective

Provide decision makers, analysts and executives with a unified environment for:

* Monitoring business performance
* Identifying growth opportunities
* Detecting anomalies
* Forecasting future sales
* Generating executive insights
* Supporting strategic decision making

---

## Future Roadmap

* PDF Executive Reports
* Forecast Reports
* Business Health Reports
* LLM Insights
* Automated Recommendations
* Explainable Anomaly Detection
* Data Hub & File Management
* AI-Powered CFO Copilot
