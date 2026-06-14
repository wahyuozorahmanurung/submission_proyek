import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from babel.numbers import format_currency

# 1. KONFIGURASI HALAMAN & TEMA
st.set_page_config(
    page_title="Bike Rentals Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)


sns.set_theme(style='whitegrid')

all_df = pd.read_csv("all_data.csv")

# Standardisasi format tanggal
if 'dteday_x' in all_df.columns:
    all_df['date_parsed'] = pd.to_datetime(all_df['dteday_x'])
elif 'dteday' in all_df.columns:
    all_df['date_parsed'] = pd.to_datetime(all_df['dteday'])
else:
    all_df['date_parsed'] = pd.date_range(start="2011-01-01", periods=len(all_df), freq='H')

# 2. SIDEBAR CONTROLS (FITUR FILTER)
with st.sidebar:
    try:
        st.image("bike_logo.png", width=200)
    except:
        pass
    st.title("🚴 Bike Rentals Dashboard")
    st.markdown("### 📊 Visualisasi Data Penyewaan Sepeda")

    start_date = pd.to_datetime("2011-01-01").date()
    end_date = pd.to_datetime("2012-12-31").date()
    
    selected_date = st.date_input(
        "📅 Pilih Rentang Tanggal", 
        value=(start_date, end_date), 
        min_value=start_date, 
        max_value=end_date
    )
    
    c_season = 'season_x' if 'season_x' in all_df.columns else 'season'
    season_map = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    if c_season in all_df.columns:
        all_df['season_name'] = all_df[c_season].map(season_map)
        all_seasons = all_df['season_name'].dropna().unique().tolist()
        selected_seasons = st.multiselect("🍁 Pilih Musim", options=all_seasons, default=all_seasons)
    else:
        selected_seasons = []

# 3. PROSES PENYARINGAN DATA REAL-TIME
if isinstance(selected_date, tuple) and len(selected_date) == 2:
    s_date, e_date = selected_date
else:
    s_date, e_date = start_date, end_date

main_df = all_df[
    (all_df['date_parsed'].dt.date >= s_date) & 
    (all_df['date_parsed'].dt.date <= e_date)
]
if selected_seasons:
    main_df = main_df[main_df['season_name'].isin(selected_seasons)]

# 4. KUMPULAN DATA PROCESSING
c_wday = 'weekday_x' if 'weekday_x' in main_df.columns else 'weekday'
grouped_weekday_all = main_df.groupby([c_wday]).agg({
    'casual_x': 'sum' if 'casual_x' in main_df.columns else 'casual',
    'registered_x': 'sum' if 'registered_x' in main_df.columns else 'registered',
    'cnt_x': 'sum' if 'cnt_x' in main_df.columns else 'cnt'
}).reset_index()

c_cnt = 'cnt_x' if 'cnt_x' in main_df.columns else 'cnt'
c_temp = 'temp_x' if 'temp_x' in main_df.columns else 'temp'
c_hum = 'hum_x' if 'hum_x' in main_df.columns else 'hum'
c_wind = 'windspeed_x' if 'windspeed_x' in main_df.columns else 'windspeed'
c_weath = 'weathersit_x' if 'weathersit_x' in main_df.columns else 'weathersit'
c_atemp = 'atemp_x' if 'atemp_x' in main_df.columns else 'atemp'
c_hr = 'hr' if 'hr' in main_df.columns else 'hr_x'

correlation_all = main_df[[c_cnt, c_season, c_temp, c_hum, c_wind, c_weath]].corr()

# 5. MAIN PAGE HEADER & KPI METRICS
st.markdown("<h1 style='text-align: center; font-size: 36px;'>🚲 Bike Rentals Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    total_rent = main_df[c_cnt].sum()
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rent:,}")
with col_m2:
    c_reg = 'registered_x' if 'registered_x' in main_df.columns else 'registered'
    total_reg = main_df[c_reg].sum()
    st.metric(label="Total Pengguna Terdaftar (Registered)", value=f"{total_reg:,}")
with col_m3:
    c_cas = 'casual_x' if 'casual_x' in main_df.columns else 'casual'
    total_cas = main_df[c_cas].sum()
    st.metric(label="Total Pengguna Kasual (Casual)", value=f"{total_cas:,}")
st.markdown("---")

# 6. GRAFIK 
st.subheader("📊 Bike Rentals by Weekday and Hour")
fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='white') # Menjamin sisi luar kanvas berwarna putih

axes[0].set_facecolor('white') 
axes[0].bar(grouped_weekday_all[c_wday], grouped_weekday_all[c_cnt], color='royalblue', alpha=0.8)
axes[0].set_title("📆 Total Rentals per Weekday", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Weekday", fontsize=12)
axes[0].set_ylabel("Total Rentals", fontsize=12)
axes[0].grid(axis='y', linestyle='--', alpha=0.5, color='#CCCCCC') # Grid abu-abu lembut agar rapi

axes[1].set_facecolor('white')
rentals_per_hour = main_df.groupby(c_hr)[c_cnt].sum()
axes[1].bar(rentals_per_hour.index, rentals_per_hour.values, color='seagreen', alpha=0.8)
axes[1].set_title("⏰ Total Rentals per Hour", fontsize=14, fontweight="bold")
axes[1].set_xlabel("Hour", fontsize=12)
axes[1].set_ylabel("Total Rentals", fontsize=12)
axes[1].grid(axis='y', linestyle='--', alpha=0.5, color='#CCCCCC')

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Grafik Penyewaan berdasarkan Jenis Pengguna
st.subheader("👥 Daily Rentals by User Type")
daily_rent_df = grouped_weekday_all

fig1, ax1 = plt.subplots(figsize=(14, 6), facecolor='white')
ax1.set_facecolor('white')
bar_width = 0.4  
x = np.arange(len(daily_rent_df[c_wday])) 

c_reg_col = 'registered_x' if 'registered_x' in daily_rent_df.columns else 'registered'
c_cas_col = 'casual_x' if 'casual_x' in daily_rent_df.columns else 'casual'

ax1.bar(x + bar_width/2, daily_rent_df[c_reg_col], width=bar_width, label='Registered', color='green', align='center')
ax1.bar(x - bar_width/2, daily_rent_df[c_cas_col], width=bar_width, label='Casual', color='blue', align='center')

ax1.set_xlabel('Days', fontsize=12)
ax1.set_ylabel('Total Rent', fontsize=12)
ax1.set_title('📅 Bike Rentals by Casual and Registered Users', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(daily_rent_df[c_wday])  
ax1.grid(axis='y', linestyle='--', alpha=0.5, color='#CCCCCC')
ax1.legend(facecolor='white', edgecolor='#CCCCCC') # Legend berlatar putih dengan border tipis
st.pyplot(fig1)
plt.close(fig1)

# Grafik Hubungan Penyewaan dengan Suhu Rata-rata
st.subheader("🌡️ Bike Rentals vs Average Temperature per Month")
c_mnth = 'mnth_x' if 'mnth_x' in main_df.columns else 'mnth'
monthly_summary_df = main_df.groupby(c_mnth).agg({
    c_cnt: 'sum',
    c_atemp: 'mean'  
}).reset_index()

fig4, ax4 = plt.subplots(figsize=(14, 6), facecolor='white')
ax4.set_facecolor('white')
ax4.scatter(monthly_summary_df[c_mnth], monthly_summary_df[c_atemp], color='red', s=100, zorder=3) 
ax4.set_title("Bike Rentals vs Average Temperature per Month", fontsize=14, fontweight='bold')
ax4.set_xlabel("Month", fontsize=12)
ax4.set_ylabel("Average Temperature (°C)", fontsize=12)
ax4.grid(linestyle='--', alpha=0.5, color='#CCCCCC')
st.pyplot(fig4)
plt.close(fig4)

# Correlation Matrix
st.subheader("📈 Correlation Matrix")
st.dataframe(correlation_all)

# Rentang Suhu dan Penyewaan Sepeda
st.subheader("🌡️ Bike Rentals by Temperature Range")
bins = [0, 10, 20, 30, 40]
labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']

multiplier = 50 if monthly_summary_df[c_atemp].max() <= 1 else 1
monthly_summary_df['temp_bin'] = pd.cut(monthly_summary_df[c_atemp] * multiplier, bins=bins, labels=labels)
binned_rentals = monthly_summary_df.groupby('temp_bin', observed=False)[c_cnt].sum().reset_index()

fig5, ax5 = plt.subplots(figsize=(14, 6), facecolor='white')
ax5.set_facecolor('white')
ax5.bar(binned_rentals['temp_bin'].astype(str), binned_rentals[c_cnt], color='skyblue')
ax5.set_title('Bike Rentals by Temperature', fontsize=14, fontweight='bold')
ax5.set_xlabel('Temperature Range', fontsize=12)
ax5.set_ylabel('Total Rentals', fontsize=12)
ax5.grid(axis='y', linestyle='--', alpha=0.5, color='#CCCCCC')
st.pyplot(fig5)
plt.close(fig5)

# 7. FITUR TAMBAHAN UNTUK PENDUKUNG KEPUTUSAN BISNIS
st.markdown("---")
st.markdown("### 🎯 Analisis Pendukung Keputusan Strategis (Executive Decision Support)")
col_dec1, col_dec2 = st.columns(2)

with col_dec1:
    hourly_users = main_df.groupby(c_hr, observed=False)[[c_reg_col, c_cas_col]].mean().reset_index()
    fig_dec1, ax_dec1 = plt.subplots(figsize=(8, 4), facecolor='white')
    ax_dec1.set_facecolor('white')
    ax_dec1.plot(hourly_users[c_hr], hourly_users[c_reg_col], label='Registered (Komuter)', color='green', linewidth=2.5)
    ax_dec1.plot(hourly_users[c_hr], hourly_users[c_cas_col], label='Casual (Turis)', color='blue', linewidth=2.5, linestyle='--')
    ax_dec1.set_xticks(range(0, 24, 2))
    ax_dec1.set_title("Perbandingan Pola Jam Sibuk Pengguna (Strategi Promo Efisiensi)", fontweight='bold')
    ax_dec1.set_xlabel("Jam")
    ax_dec1.set_ylabel("Rata-rata Penyewa")
    ax_dec1.grid(linestyle='--', alpha=0.5, color='#CCCCCC')
    ax_dec1.legend(facecolor='white', edgecolor='#CCCCCC')
    st.pyplot(fig_dec1)
    plt.close(fig_dec1)

with col_dec2:
    weather_impact = main_df.groupby(c_weath, observed=False)[c_cnt].mean().reset_index()
    if not weather_impact.empty:
        max_rent = weather_impact[c_cnt].max()
        weather_impact['Penurunan (%)'] = ((weather_impact[c_cnt] - max_rent) / max_rent) * 100
        
        fig_dec2, ax_dec2 = plt.subplots(figsize=(8, 4), facecolor='white')
        ax_dec2.set_facecolor('white')
        # Diganti memakai palette bergradasi cerah ke gelap agar terlihat estetik di atas warna putih
        sns.barplot(x='Penurunan (%)', y=c_weath, data=weather_impact.sort_values(by='Penurunan (%)'), palette='Oranges_r', ax=ax_dec2)
        ax_dec2.set_title("Manajemen Risiko: Persentase Dampak Penurunan Akibat Cuaca", fontweight='bold')
        ax_dec2.set_xlabel("Persentase Dampak (%)")
        ax_dec2.set_ylabel("Kondisi Cuaca (Kode)")
        ax_dec2.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')
        st.pyplot(fig_dec2)
        plt.close(fig_dec2)

# 8. FITUR SIMULASI PROYEKSI MASA DEPAN (WHAT-IF ANALYSIS)
st.markdown("### 🔮 Simulasi Target Proyeksi Bisnis (What-If Analysis)")
st.markdown("<p style='font-size: 14px; color: #4B5563; margin-top:-10px;'>Simulasikan rencana target pertumbuhan investasi armada sepeda atau penambahan unit untuk tahun mendatang.</p>", unsafe_allow_html=True)

growth_rate = st.slider("Target Ekspektasi Kenaikan Pertumbuhan Volume Sewa (%)", min_value=0, max_value=100, value=20, step=5)
projected_total = total_rent * (1 + (growth_rate / 100))

col_sim1, col_sim2 = st.columns(2)
with col_sim1:
    st.metric(label="Volume Sewa Berdasarkan Filter Saat Ini", value=f"{total_rent:,}")
with col_sim2:
    st.metric(label="Proyeksi Volume Sewa di Lapangan Masa Depan", value=f"{int(projected_total):,}", delta=f"+{growth_rate}%")

# 9. FOOTER & CHECKBOX DATA MENTAH
st.markdown("---")
if st.checkbox('🔍 Show Raw Data'):
    st.subheader('📜 Raw Data')
    st.write(main_df)

st.caption('Copyright (c) Wahyu Ozorah Manurung 2025')
