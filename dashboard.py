import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("all_data.csv")

with st.sidebar:
    st.image("bike_logo.png", width=200)
    st.title("🚴 Bike Rentals Dashboard")
    st.markdown("### 📊 Visualisasi Data Penyewaan Sepeda")

    start_date = pd.to_datetime("2011-01-01")
    end_date = pd.to_datetime("2012-12-31")
    selected_date = st.date_input("📅 Pilih Tanggal", value=start_date, min_value=start_date, max_value=end_date)
    st.write("📌 Tanggal yang dipilih:", selected_date)
    
# Data Processing
grouped_weekday_all = all_df.groupby(['weekday_x']).agg({
    'casual_x': 'sum',
    'registered_x': 'sum',
    'cnt_x': 'sum'
}).reset_index()

correlation_all = all_df[['cnt_x', 'season_x', 'temp_x', 'hum_x', 'windspeed_x', 'weathersit_x']].corr()
season_rentals_all = all_df.groupby(by="season_x").instant.nunique().sort_values(ascending=False)
monthly_rentals_all = all_df.groupby(by="mnth_x")['cnt_x'].sum()
weather_rentals_all = all_df.groupby(by="weathersit_x").instant.nunique().sort_values(ascending=False)

# Title
st.markdown("<h1 style='text-align: center; font-size: 36px;'>🚲 Bike Rentals Dashboard</h1>", unsafe_allow_html=True)

# Grafik Penyewaan per Hari dan per Jam
st.subheader("📊 Bike Rentals by Weekday and Hour")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(grouped_weekday_all['weekday_x'], grouped_weekday_all['cnt_x'], color='royalblue', alpha=0.8)
axes[0].set_title("📆 Total Rentals per Weekday", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Weekday", fontsize=12)
axes[0].set_ylabel("Total Rentals", fontsize=12)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

rentals_per_hour = all_df.groupby('hr')['cnt_x'].sum()
axes[1].bar(rentals_per_hour.index, rentals_per_hour.values, color='seagreen', alpha=0.8)
axes[1].set_title("⏰ Total Rentals per Hour", fontsize=14, fontweight="bold")
axes[1].set_xlabel("Hour", fontsize=12)
axes[1].set_ylabel("Total Rentals", fontsize=12)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

# Grafik Penyewaan berdasarkan Jenis Pengguna
st.subheader("👥 Daily Rentals by User Type")
daily_rent_df = grouped_weekday_all

fig1, ax1 = plt.subplots(figsize=(14, 6))
bar_width = 0.4  
x = np.arange(len(daily_rent_df['weekday_x'])) 
ax1.bar(x + bar_width/2, daily_rent_df['registered_x'], width=bar_width, label='Registered', color='green', align='center')
ax1.bar(x - bar_width/2, daily_rent_df['casual_x'], width=bar_width, label='Casual', color='blue', align='center')

ax1.set_xlabel('Days', fontsize=12)
ax1.set_ylabel('Total Rent', fontsize=12)
ax1.set_title('📅 Bike Rentals by Casual and Registered Users', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(daily_rent_df['weekday_x'])  
ax1.legend()
st.pyplot(fig1)

# Grafik Hubungan Penyewaan dengan Suhu Rata-rata
st.subheader("🌡️ Bike Rentals vs Average Temperature per Month")
monthly_summary_df = all_df.groupby('mnth_x').agg({
    'cnt_x': 'sum',
    'atemp_x': 'mean'  
}).reset_index()

fig4, ax4 = plt.subplots(figsize=(14, 6))
ax4.scatter(monthly_summary_df['mnth_x'], monthly_summary_df['atemp_x'], color='red')
ax4.set_title("Bike Rentals vs Average Temperature per Month", fontsize=14, fontweight='bold')
ax4.set_xlabel("Month", fontsize=12)
ax4.set_ylabel("Average Temperature (°C)", fontsize=12)
st.pyplot(fig4)

# Correlation Matrix
st.subheader("📈 Correlation Matrix")
st.dataframe(correlation_all)

# Rentang Suhu dan Penyewaan Sepeda
st.subheader("🌡️ Bike Rentals by Temperature Range")
bins = [0, 10, 20, 30, 40]
labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
monthly_summary_df['temp_bin'] = pd.cut(monthly_summary_df['atemp_x'] * 50, bins=bins, labels=labels)
binned_rentals = monthly_summary_df.groupby('temp_bin')['cnt_x'].sum().reset_index()

fig5, ax5 = plt.subplots(figsize=(14, 6))
ax5.bar(binned_rentals['temp_bin'], binned_rentals['cnt_x'], color='skyblue')
ax5.set_title('Bike Rentals by Temperature', fontsize=14, fontweight='bold')
ax5.set_xlabel('Temperature Range', fontsize=12)
ax5.set_ylabel('Total Rentals', fontsize=12)
st.pyplot(fig5)

# Tombol Tampilkan Data Mentah
if st.checkbox('🔍 Show Raw Data'):
    st.subheader('📜 Raw Data')
    st.write(all_df)

st.caption('Copyright (c) Wahyu Ozorah Manurung 2025')