## 🌟 Executive Summary

This project analyzes the **Bike Sharing Dataset** and presents the results through an interactive dashboard built with Streamlit. The dashboard helps users explore rental patterns based on time, season, weather conditions, and user types (casual and registered). By transforming raw data into visual insights, the project supports data-driven decision-making for operational planning and customer engagement strategies.

**Live Demo:**
https://wahyuozorahmanurungsubmission1.streamlit.app/

### Key Highlights

* Interactive dashboard with dynamic filtering capabilities.
* Real-time KPI monitoring for bike rental performance.
* Comparative analysis of casual and registered user behavior.
* Weather and seasonal impact analysis on rental demand.
* Simple forecasting tool for business scenario simulation.

---

## 🚀 Features

### 🎛️ Interactive Filters

Explore the dataset using flexible filters, including date range, season, and weather conditions.

### 📊 KPI Monitoring

Track key metrics such as:

* Total Rentals
* Registered Users
* Casual Users

All metrics update automatically based on the selected filters.

### 📈 User Behavior Analysis

Compare rental patterns between casual and registered users to identify differences in usage behavior and peak activity periods.

### 🌦️ Weather Impact Analysis

Evaluate how weather conditions affect rental demand and identify factors that may influence operational performance.

### 🔮 What-If Simulation

A simple forecasting feature that allows users to estimate future rental demand based on adjustable growth assumptions.

---

## 📐 Project Background

### Situation

The Bike Sharing Dataset contains historical rental records along with environmental and seasonal variables. While the data provides valuable information, extracting actionable insights from raw records can be challenging without proper visualization and analysis tools.

### Task

The objectives of this project were to:

1. Analyze rental trends across different time periods.
2. Identify seasonal and weather-related factors that influence demand.
3. Compare usage patterns between casual and registered users.
4. Develop an interactive dashboard that enables efficient data exploration.

### Action

The project was developed through the following stages:

* Data cleaning and preprocessing using Pandas.
* Exploratory Data Analysis (EDA) to identify trends and patterns.
* Creation of interactive visualizations using Matplotlib and Seaborn.
* Dashboard development with Streamlit.
* Implementation of caching mechanisms to improve application performance.

### Result

The analysis revealed several important insights:

* Registered users tend to show clear commuting patterns, with demand peaking during morning and evening hours.
* Casual users are more active during midday and leisure periods.
* Seasonal factors significantly influence rental demand.
* Adverse weather conditions generally reduce the number of rentals.

These findings can support operational planning, resource allocation, and customer engagement initiatives.

---

## 🛠️ Tech Stack

* **Programming Language:** Python 3.9+
* **Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn
* **Data Formatting:** Babel

---

## 📂 Project Structure

```text
project/
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── requirements.txt
└── README.md
```

---

## 💻 Installation & Local Setup

Follow the steps below to run the dashboard locally:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bike-sharing-analysis.git
cd bike-sharing-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run dashboard/dashboard.py
```

### 4. Open the dashboard

Visit the local URL displayed in your terminal, typically:

```text
http://localhost:8501
```
