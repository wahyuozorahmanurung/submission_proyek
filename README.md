import base64

# Content for README.md
readme_content = """# 🚲 Bike Rentals Advanced Analytics Dashboard

A dynamic, business-driven interactive dashboard developed with **Streamlit**, **Pandas**, and **Seaborn** to optimize bike-sharing operations. This project delivers actionable insights into rental behaviors, temporal patterns, user demographics, risk management, and predictive simulations.

---

## 🌟 Executive Summary & Impact
This project transforms raw data from the **Bike Sharing Dataset** into a high-performance decision support tool. It addresses critical business problems such as logistics allocation (fleet distribution), target marketing, and weather-related risk mitigation. 

* **Live Demo:** `[Insert Your Streamlit Cloud Link Here]`
* **Key Achievements:** Built an end-to-end interactive reporting pipeline with real-time responsive analytics, reducing static report dependencies and introducing automated "What-If" business forecasting.

---

## 🚀 Key Features

* **🎛️ Real-Time Responsive Filters:** Sift through multiple years of data instantly using date range picker, seasonal parameters, and weather selectors.
* **📈 Executive KPI Metrics:** High-level counters for Total Rentals, Registered Users, and Casual Users that recalculate dynamically based on active filter criteria.
* **🎯 Decision-Support Analytics (Advanced):**
  * *Marketing Strategy:* Visualizes contrasting peak hour trends between casual users and registered commuters to inform targeted promo timing.
  * *Risk Management:* Calculates percentage drops in revenue/rentals under adverse weather conditions to support temporary station closure decisions.
* **🔮 Simulation Tool (What-If Analysis):** Features an interactive slider for stakeholder forecasting, allowing immediate calculation of future fleet expansion targets.

---

## 📐 Project Structure & Case Study 

To demonstrate rigorous data analysis and engineering standards for portfolio evaluation, the development workflow is structured using the **STAR (Situation, Task, Action, Result)** technique:

### 1. 🔍 Situation
The bike-sharing operation collected vast amounts of hourly and daily transaction data containing environmental, seasonal, and demographic variables. However, stakeholders and operational managers lacked an efficient, consolidated tool to monitor performance and adjust strategies. Analytical questions were static, and there was no operational bridge to understand how factors like rapid temperature changes or heavy rain impacted hourly resource distribution in real-time.

### 2. 🎯 Task
The primary objectives were to:
1. Identify monthly rental trends across 2011 and 2012 to discover cyclical patterns and Year-over-Year (YoY) growth.
2. Determine which seasons and precise temperature thresholds maximize utilization versus which ones introduce severe operational risks.
3. Design and build a production-ready, ultra-clean web application with zero rendering lag, optimized cache management, and strict separation of customer demographic behavior.

### 3. 🛠️ Action
* **Data Engineering & Standardization:** Developed a bulletproof preprocessing pipeline inside a cached data block (`@st.cache_data`). Built adaptive column mapping handlers (`cnt_x`, `dteday_x`, etc.) to accommodate dataset variations and prevent pipeline failures during deployment.
* **User Interface Customization:** Replaced old dark-themed visual grids with a clean, high-contrast, minimalist `whitegrid` layout using Matplotlib/Seaborn. Configured dynamic grid layouts (`st.columns`) ensuring charts render beautifully in side-by-side structures.
* **Advanced Decision Modules:** Engineered custom aggregation metrics to plot user demography disparities (Casual vs. Registered) and implemented an advanced conditional statistical matrix to quantify risk drops during poor weather.

### 4. 🏆 Result
* **Actionable Insights Uncovered:** * Discovered that Registered users peak heavily during commute hours (08:00 and 17:00), while Casual users peak steadily during midday (11:00 - 16:00). This provides an explicit decision vector: introduce off-peak discounts to Casual users to utilize idling inventory.
  * Quantified that Fall (Musim Gugur) yields peak utilization, whereas severe weather conditions result in steep, measurable rental drops, allowing managers to dynamically reduce field-staff costs.
* **Technical Performance:** Achieved rapid load times via computational caching, eliminated background memory leaks using explicit canvas terminations (`plt.close(fig)`), and established a completely dynamic data loop.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.9+
* **Framework:** Streamlit (Web Application Layout & Interactive Inputs)
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn (Custom Whitegrid Theme)
* **Formatting:** Babel (Currency and Numerical Formatting Support)

---
link : https://wahyuozorahmanurungsubmission1.streamlit.app/
## 💿 Installation & Local Setup

Follow these simple steps to cloned this project and run the dashboard locally on your machine:

1. **Clone the repository:**
