import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Bike Rentals Premium Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_theme(style='whitegrid')

# 2. FUNGSI LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    
    if 'dteday_x' in df.columns:
        df['date_parsed'] = pd.to_datetime(df['dteday_x'])
    elif 'dteday' in df.columns:
        df['date_parsed'] = pd.to_datetime(df['dteday'])
    else:
        df['date_parsed'] = pd.date_range(start="2011-01-01", periods=len(df), freq='H')
    
    c_season = 'season_x' if 'season_x' in df.columns else 'season'
    season_map = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    if c_season in df.columns:
        df['season_name'] = df[c_season].map(season_map)
    else:
        df['season_name'] = 'Unknown'
        
    c_weather = 'weathersit_x' if 'weathersit_x' in df.columns else 'weathersit'
    weather_map = {1:'Clear/Partly Cloudy', 2:'Misty/Cloudy', 3:'Light Snow/Rain', 4:'Severe Weather'}
    if c_weather in df.columns:
        df['weather_name'] = df[c_weather].map(weather_map)
    else:
        df['weather_name'] = 'Unknown'

    c_wday = 'weekday_x' if 'weekday_x' in df.columns else 'weekday'
    weekday_map = {0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat'}
    if c_wday in df.columns:
        df['day_name'] = df[c_wday].map(weekday_map)
    else:
        df['day_name'] = df['date_parsed'].dt.strftime('%a')

    c_mnth = 'mnth_x' if 'mnth_x' in df.columns else 'mnth'
    month_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    if c_mnth in df.columns:
        df['month_name'] = df[c_mnth].map(month_map)
    else:
        df['month_name'] = df['date_parsed'].dt.strftime('%b')

    df['cnt'] = df['cnt_x'] if 'cnt_x' in df.columns else (df['cnt'] if 'cnt' in df.columns else 0)
    df['registered'] = df['registered_x'] if 'registered_x' in df.columns else (df['registered'] if 'registered' in df.columns else 0)
    df['casual'] = df['casual_x'] if 'casual_x' in df.columns else (df['casual'] if 'casual' in df.columns else 0)
    df['atemp'] = df['atemp_x'] if 'atemp_x' in df.columns else (df['atemp'] if 'atemp' in df.columns else 0)
    df['temp'] = df['temp_x'] if 'temp_x' in df.columns else (df['temp'] if 'temp' in df.columns else 0)
    df['hum'] = df['hum_x'] if 'hum_x' in df.columns else (df['hum'] if 'hum' in df.columns else 0)
    df['windspeed'] = df['windspeed_x'] if 'windspeed_x' in df.columns else (df['windspeed'] if 'windspeed' in df.columns else 0)
    
    df['hr'] = df['hr_x'] if 'hr_x' in df.columns else (df['hr'] if 'hr' in df.columns else df['date_parsed'].dt.hour)
    
    c_working = 'workingday_x' if 'workingday_x' in df.columns else 'workingday'
    if c_working in df.columns:
        df['day_type'] = df[c_working].map({1: 'Working Day', 0: 'Weekend / Holiday'})
    else:
        df['day_type'] = df['day_name'].apply(lambda x: 'Weekend / Holiday' if x in ['Sun', 'Sat'] else 'Working Day')

    return df

all_df = load_data()

# 3. SIDEBAR CONTROLS (FITUR FILTER)
with st.sidebar:
    try:
        st.image("bike_logo.png", width=150)
    except:
        st.title("🚴 Bike Corp")
        
    st.markdown("## **Dashboard Filters**")
    
    min_date = all_df['date_parsed'].min().date()
    max_date = all_df['date_parsed'].max().date()
    
    date_range = st.date_input(
        label="📅 Pilih Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )
    
    all_seasons = all_df['season_name'].dropna().unique().tolist()
    selected_seasons = st.multiselect(
        label="🍁 Pilih Musim",
        options=all_seasons,
        default=all_seasons
    )
    
    all_weather = all_df['weather_name'].dropna().unique().tolist()
    selected_weather = st.multiselect(
        label="🌧️ Pilih Kondisi Cuaca",
        options=all_weather,
        default=all_weather
    )
    
    all_day_types = all_df['day_type'].dropna().unique().tolist()
    selected_day_types = st.multiselect(
        label="💼 Jenis Hari Operasional",
        options=all_day_types,
        default=all_day_types
    )

# 4. PROSES PENYARINGAN DATA UTAMA
if isinstance(date_range, tuple) or isinstance(date_range, list):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = max_date
else:
    start_date = date_range
    end_date = max_date

main_df = all_df[
    (all_df['date_parsed'].dt.date >= start_date) & 
    (all_df['date_parsed'].dt.date <= end_date) &
    (all_df['season_name'].isin(selected_seasons)) &
    (all_df['weather_name'].isin(selected_weather)) &
    (all_df['day_type'].isin(selected_day_types))
]

# 5. MAIN PAGE LAYOUT
st.markdown("<h1 style='color: #1E3A8A; font-weight: bold; margin-bottom: 0px;'>🚲 Bike Rentals Advanced Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 15px; margin-bottom: 25px;'>Sistem pendukung keputusan operasional armada, manajemen risiko, dan strategi segmentasi marketing.</p>", unsafe_allow_html=True)
st.markdown("---")

if main_df.empty:
    st.warning("⚠️ Tidak ada data yang cocok dengan kombinasi filter Anda. Silakan ubah filter di sidebar.")
else:
    # --- SEKSI 1: KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Sewa Sepeda", value=f"{main_df['cnt'].sum():,}")
    with col2:
        st.metric(label="Pengguna Terdaftar (Registered)", value=f"{main_df['registered'].sum():,}")
    with col3:
        st.metric(label="Pengguna Kasual (Casual)", value=f"{main_df['casual'].sum():,}")
    with col4:
        avg_temp = main_df['atemp'].mean() * 50 if main_df['atemp'].max() <= 1 else main_df['atemp'].mean()
        st.metric(label="Rata-rata Suhu Terasa", value=f"{avg_temp:.1f} °C")

    # --- SEKSI 2: TREN OPERASIONAL UTAMA ---
    st.markdown("### 🕒 Deskripsi Tren Waktu & Distribusi Operasional")
    col_g1, col_g2 = st.columns(2)
    day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    
    with col_g1:
        grouped_weekday = main_df.groupby('day_name', observed=False)['cnt'].sum().reindex(day_order).fillna(0).reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='day_name', y='cnt', data=grouped_weekday, palette="Blues_r", ax=ax)
        ax.set_title("Total Rentals per Day of Week", fontweight="bold")
        ax.set_xlabel(None)
        ax.set_ylabel("Total Rentals")
        st.pyplot(fig)
        plt.close(fig)
        
    with col_g2:
        rentals_per_hour = main_df.groupby('hr', observed=False)['cnt'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(x='hr', y='cnt', data=rentals_per_hour, color='#10B981', marker="o", ax=ax)
        ax.set_title("Hourly Distribution of Rentals", fontweight="bold")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Total Rentals")
        st.pyplot(fig)
        plt.close(fig)

    # --- SEKSI 3: PERILAKU PENGGUNA & KEBUTUHAN LOGISTIK ---
    st.markdown("### 👥 Segmentasi Demografi & Alokasi Manajemen Logistik")
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        user_day_df = main_df.groupby('day_name', observed=False)[['registered', 'casual']].sum().reindex(day_order).fillna(0).reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(user_day_df['day_name']))
        width = 0.35
        ax.bar(x - width/2, user_day_df['registered'], width, label='Registered', color='#3B82F6')
        ax.bar(x + width/2, user_day_df['casual'], width, label='Casual', color='#F59E0B')
        ax.set_xticks(x)
        ax.set_xticklabels(user_day_df['day_name'])
        ax.legend()
        ax.set_title('Demografi Pengguna Berdasarkan Hari', fontweight='bold')
        st.pyplot(fig)
        plt.close(fig)

    with col_g4:
        main_df['temp_celcius'] = main_df['atemp'] * 50 if main_df['atemp'].max() <= 1 else main_df['atemp']
        bins = [0, 10, 20, 30, 40]
        labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
        main_df['temp_bin'] = pd.cut(main_df['temp_celcius'], bins=bins, labels=labels)
        binned_rentals = main_df.groupby('temp_bin', observed=False)['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='temp_bin', y='cnt', data=binned_rentals, palette="YlOrRd", ax=ax)
        ax.set_title('Total Rentals by Temperature Range', fontweight='bold')
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Total Rentals')
        st.pyplot(fig)
        plt.close(fig)

    # --- SEKSI 4: ANALISIS PENDUKUNG KEPUTUSAN EKSEKUTIF ---
    st.markdown("### 🎯 Analisis Pendukung Keputusan Strategis (Decision-Support)")
    col_g5, col_g6 = st.columns(2)
    
    with col_g5:
        weather_impact = main_df.groupby('weather_name', observed=False)['cnt'].mean().reset_index()
        if not weather_impact.empty:
            max_rent = weather_impact['cnt'].max()
            weather_impact['Drop (%)'] = ((weather_impact['cnt'] - max_rent) / max_rent) * 100
            
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x='Drop (%)', y='weather_name', data=weather_impact.sort_values(by='Drop (%)'), palette='Reds', ax=ax)
            ax.set_title("Manajemen Risiko: Dampak Penurunan Cuaca Buruk (vs Cuaca Cerah)", fontweight='bold')
            ax.set_xlabel("Persentase Penurunan Penyewaan (%)")
            ax.set_ylabel(None)
            st.pyplot(fig)
            plt.close(fig)
            
    with col_g6:
        hourly_users = main_df.groupby('hr', observed=False)[['registered', 'casual']].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(hourly_users['hr'], hourly_users['registered'], label='Registered (Komuter)', color='#3B82F6', linewidth=2.5)
        ax.plot(hourly_users['hr'], hourly_users['casual'], label='Casual (Turis/Santai)', color='#F59E0B', linewidth=2.5, linestyle='--')
        ax.set_xticks(range(0, 24, 2))
        ax.set_title("Strategi Marketing: Perbedaan Pola Jam Sibuk Pengguna", fontweight='bold')
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Penyewa")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

    # --- SEKSI 5: SIMULASI PROYEKSI BISNIS (WHAT-IF ANALYSIS) ---
    st.markdown("### 🔮 Simulasi Target Proyeksi Bisnis (What-If Analysis)")
    st.markdown("<p style='font-size: 14px; color: #4B5563; margin-top:-10px;'>Simulasikan pertumbuhan performa investasi atau ekspansi penambahan unit armada sepeda untuk tahun depan.</p>", unsafe_allow_html=True)
    
    growth_rate = st.slider("Target Kenaikan Pertumbuhan Volume Sewa (%)", min_value=0, max_value=100, value=15, step=5)
    
    current_total = main_df['cnt'].sum()
    projected_total = current_total * (1 + (growth_rate / 100))
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        st.metric(label="Volume Sewa Saat Ini (Berdasarkan Filter)", value=f"{current_total:,}")
    with col_sim2:
        st.metric(label="Proyeksi Volume Sewa Tahun Depan", value=f"{int(projected_total):,}", delta=f"+{growth_rate}%")

# --- FOOTER & RAW DATA ---
st.markdown("---")
if st.checkbox('🔍 Tampilkan Pratonton Data Mentah Terfilter'):
    st.dataframe(main_df.head(50), use_container_width=True)

st.caption('Copyright (c) Wahyu Ozorah Manurung 2026')
