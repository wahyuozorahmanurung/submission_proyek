import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="Bike Rentals Dashboard",
    page_icon="🚲",
    layout="wide", # Menggunakan mode wide agar visualisasi lebih luas dan rapi
    initial_sidebar_state="expanded"
)

# Set tema seaborn untuk grafik Matplotlib
sns.set_theme(style='minimal')
plt.rcParams.update({
    'font.size': 10,
    'axes.edgecolor': '#E6E6E6',
    'axes.linewidth': 0.8,
    'grid.color': '#F0F0F0'
})

# --- LOAD DATA ---
@st.cache_data # Menggunakan cache agar loading data jauh lebih cepat
def load_data():
    df = pd.read_csv("all_data.csv")
    # Pastikan kolom tanggal bertipe datetime
    if 'dteday' in df.columns:
        df['dteday'] = pd.to_datetime(df['dteday'])
    elif 'dteday_x' in df.columns:
        df['dteday'] = pd.to_datetime(df['dteday_x'])
    else:
        # Jika tidak ada kolom dteday, buat asumsi berdasarkan rentang dataset
        df['dteday'] = pd.date_range(start="2011-01-01", periods=len(df), freq='H')
    
    # Mapping angka menjadi teks agar user-friendly
    month_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    weekday_map = {0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat'}
    season_map = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    weather_map = {1:'Clear/Partly Cloudy', 2:'Misty/Cloudy', 3:'Light Snow/Rain', 4:'Severe Weather'}

    # Gunakan nama kolom yang fleksibel sesuai dataset Anda (_x atau asli)
    c_mnth = 'mnth_x' if 'mnth_x' in df.columns else 'mnth'
    c_wday = 'weekday_x' if 'weekday_x' in df.columns else 'weekday'
    c_seash = 'season_x' if 'season_x' in df.columns else 'season'
    c_weath = 'weathersit_x' if 'weathersit_x' in df.columns else 'weathersit'
    
    df['month_name'] = df[c_mnth].map(month_map)
    df['day_name'] = df[c_wday].map(weekday_map)
    df['season_name'] = df[c_seash].map(season_map)
    df['weather_name'] = df[c_weath].map(weather_map)
    
    # Standardisasi nama kolom utama untuk visualisasi
    df['cnt'] = df['cnt_x'] if 'cnt_x' in df.columns else df['cnt']
    df['registered'] = df['registered_x'] if 'registered_x' in df.columns else df['registered']
    df['casual'] = df['casual_x'] if 'casual_x' in df.columns else df['casual']
    df['atemp'] = df['atemp_x'] if 'atemp_x' in df.columns else df['atemp']
    df['temp'] = df['temp_x'] if 'temp_x' in df.columns else df['temp']
    df['hum'] = df['hum_x'] if 'hum_x' in df.columns else df['hum']
    df['windspeed'] = df['windspeed_x'] if 'windspeed_x' in df.columns else df['windspeed']
    
    return df

all_df = load_data()

# --- SIDEBAR INTERAKTIF (FILTERS) ---
with st.sidebar:
    try:
        st.image("bike_logo.png", width=150)
    except:
        st.title("🚴 Bike Corp")
        
    st.markdown("## **Dashboard Filters**")
    st.markdown("Sesuaikan parameter di bawah untuk memfilter data seluruh grafik.")
    
    # 1. Filter Rentang Tanggal
    min_date = all_df['dteday'].min().date()
    max_date = all_df['dteday'].max().date()
    
    start_date, end_date = st.date_input(
        label="📅 Pilih Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # 2. Filter Multi-select Musim
    all_seasons = all_df['season_name'].dropna().unique().tolist()
    selected_seasons = st.multiselect(
        label="🍁 Pilih Musim",
        options=all_seasons,
        default=all_seasons
    )
    
    # 3. Filter Multi-select Cuaca
    all_weather = all_df['weather_name'].dropna().unique().tolist()
    selected_weather = st.multiselect(
        label="🌧️ Pilih Kondisi Cuaca",
        options=all_weather,
        default=all_weather
    )

# --- PROSES FILTER DATA ---
main_df = all_df[
    (all_df['dteday'].dt.date >= start_date) & 
    (all_df['dteday'].dt.date <= end_date) &
    (all_df['season_name'].isin(selected_seasons)) &
    (all_df['weather_name'].isin(selected_weather))
]

# --- MAIN PAGE HEADER ---
st.markdown("<h1 style='text-align: left; font-size: 40px; font-weight: bold; color: #1E3A8A; margin-bottom: 0px;'>🚲 Bike Rentals Advanced Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 16px; margin-bottom: 30px;'>Menampilkan wawasan mendalam mengenai performa penyewaan sepeda berdasarkan tren waktu, tipe pengguna, dan faktor eksternal cuaca.</p>", unsafe_allow_html=True)

# --- SEKSI 1: KPI METRICS ---
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_rentals = main_df['cnt'].sum()
total_registered = main_df['registered'].sum()
total_casual = main_df['casual'].sum()
avg_temp = (main_df['atemp'].mean() * 50) if 'atemp' in main_df.columns else 0 # Asumsi denormalisasi atemp jika dikali 50

with col1:
    st.metric(label="Total Keseluruhan Sewa", value=f"{total_rentals:,}")
with col2:
    st.metric(label="Pengguna Terdaftar (Registered)", value=f"{total_registered:,}")
with col3:
    st.metric(label="Pengguna Kasual (Casual)", value=f"{total_casual:,}")
with col4:
    st.metric(label="Rata-rata Suhu Terasa", value=f"{avg_temp:.1f} °C")

st.markdown("---")

# --- SEKSI 2: GRAFIK WAKTU (WEEKDAY & HOUR) ---
st.markdown("### 🕒 Tren Waktu Penyewaan")
col_graph1, col_graph2 = st.columns(2)

# Mengurutkan hari agar rapi dari Sun-Sat
day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
grouped_weekday = main_df.groupby('day_name')['cnt'].sum().reindex(day_order).reset_index()

with col_graph1:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='day_name', y='cnt', data=grouped_weekday, palette="Blues_r", ax=ax)
    ax.set_title("📆 Total Rentals per Day of Week", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel(None)
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

with col_graph2:
    rentals_per_hour = main_df.groupby('hr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', data=rentals_per_hour, color='#10B981', linewidth=2.5, marker="o", ax=ax)
    ax.set_title("⏰ Hourly Distribution of Rentals", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Total Rentals")
    ax.set_xticks(range(0, 24, 2))
    st.pyplot(fig)

# --- SEKSI 3: KASUAL VS REGISTERED & SUHU ---
st.markdown("### 👥 Perilaku Pengguna & Pengaruh Lingkungan")
col_graph3, col_graph4 = st.columns(2)

with col_graph3:
    # Grafik Komparasi Tipe Pengguna per Hari
    user_day_df = main_df.groupby('day_name')[['registered', 'casual']].sum().reindex(day_order).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(user_day_df['day_name']))
    width = 0.35
    
    ax.bar(x - width/2, user_day_df['registered'], width, label='Registered Users', color='#3B82F6')
    ax.bar(x + width/2, user_day_df['casual'], width, label='Casual Users', color='#F59E0B')
    
    ax.set_title('📅 Demografi Pengguna Berdasarkan Hari', fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(user_day_df['day_name'])
    ax.legend(frameon=True, facecolor='white', edgecolor='none')
    st.pyplot(fig)

with col_graph4:
    # Rentang Suhu yang Diperbaiki (Menggunakan data main_df yang terfilter)
    # Asumsi nilai asli di dataset berkisar 0-1, jika dikali 50 menjadi skala derajat Celcius
    main_df['temp_celcius'] = main_df['atemp'] * 50
    bins = [0, 10, 20, 30, 40]
    labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
    main_df['temp_bin'] = pd.cut(main_df['temp_celcius'], bins=bins, labels=labels)
    binned_rentals = main_df.groupby('temp_bin', observed=False)['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='temp_bin', y='cnt', data=binned_rentals, palette="YlOrRd", ax=ax)
    ax.set_title('🌡️ Total Rentals by Temperature Range', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Temperature Group')
    ax.set_ylabel('Total Rentals')
    st.pyplot(fig)

# --- SEKSI 4: ANALISIS KORELASI & MATRIKS ---
st.markdown("### 📊 Faktor Korelasional Numerik")
col_corr1, col_corr2 = st.columns([1.2, 1])

with col_corr1:
    # Matriks Korelasi divisualisasikan dengan Heatmap (Jauh lebih interaktif/profesional daripada dataframe biasa)
    corr_columns = ['cnt', 'temp', 'atemp', 'hum', 'windspeed']
    # Memastikan kolom tersedia di df
    available_corr_cols = [c for c in corr_columns if c in main_df.columns]
    correlation_matrix = main_df[available_corr_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax, vmin=-1, vmax=1)
    ax.set_title("📈 Correlation Heatmap (Faktor Cuaca vs Jumlah Sewa)", fontsize=11, fontweight="bold", pad=10)
    st.pyplot(fig)

with col_corr2:
    # Scatter plot interaktif bawaan Streamlit untuk portofolio yang dinamis
    st.markdown("<p style='font-size:14px; font-weight:bold;'>Hubungan Spesifik Antara Suhu vs Penyewaan</p>", unsafe_allow_html=True)
    st.scatter_chart(
        data=main_df.sample(n=min(len(main_df), 1000)), # Sampling agar lancar jika datanya puluhan ribu
        x='temp_celcius',
        y='cnt',
        color='#EF4444',
        use_container_width=True
    )

# --- FOOTER & RAW DATA ---
st.markdown("---")
col_foot1, col_foot2 = st.columns([3, 1])

with col_foot1:
    if st.checkbox('🔍 Tampilkan Pratonton Data Mentah (Raw Data)'):
        st.markdown("#### 📜 Dataset Terfilter")
        st.dataframe(main_df.head(100), use_container_width=True)

with col_foot2:
    st.markdown("<p style='text-align: right; color: #9CA3AF; font-size: 12px; padding-top: 15px;'>Dashboard Portfolio | © Wahyu Ozorah Manurung 2026</p>", unsafe_allow_html=True)
