# Import library
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import fungsi dari config.py
from config import *

# Set konfigurasi halaman dashboard
st.set_page_config("Dashboard Katalog Gempa", page_icon="🌋", layout="wide")

# Header Dashboard
st.title("🌋 Dashboard Katalog Gempa Bumi")
st.markdown("---")

# Ambil data gempa
result_earthquakes = view_all_earthquakes()
df_earthquakes = pd.DataFrame(result_earthquakes, columns=[
    "id", "tanggal", "waktu", "latitude", "longitude", "depth", "magnitude", "remark"
])

# Konversi tipe data
df_earthquakes['tanggal'] = pd.to_datetime(df_earthquakes['tanggal'])
df_earthquakes['magnitude'] = pd.to_numeric(df_earthquakes['magnitude'])
df_earthquakes['depth'] = pd.to_numeric(df_earthquakes['depth'])

# Ambil data statistik per bulan
result_stats = view_statistics_by_month()
df_stats = pd.DataFrame(result_stats, columns=[
    "bulan", "jumlah_gempa", "rata_rata_magnitude", "magnitude_maksimum", "magnitude_minimum"
])
df_stats['bulan'] = pd.to_datetime(df_stats['bulan'])

# Ambil data gempa per wilayah
result_regions = view_earthquakes_by_region()
df_regions = pd.DataFrame(result_regions, columns=["remark", "jumlah"])

# ============================
# SIDEBAR - Navigasi & Filter
# ============================
st.sidebar.header("📊 Navigasi Visualisasi")

# Dropdown untuk memilih jenis visualisasi
visualization_type = st.sidebar.selectbox(
    "Pilih Jenis Visualisasi",
    ["Pie Chart", "Area Chart", "Bar Chart", "Line Chart", "Map"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filter Data")

# Filter Rentang Magnitude
st.sidebar.subheader("Magnitude")
min_mag = float(df_earthquakes['magnitude'].min())
max_mag = float(df_earthquakes['magnitude'].max())
mag_range = st.sidebar.slider(
    "Pilih Rentang Magnitude",
    min_value=min_mag,
    max_value=max_mag,
    value=(min_mag, max_mag),
    step=0.1
)

# Filter Rentang Kedalaman
st.sidebar.subheader("Kedalaman (km)")
min_depth = int(df_earthquakes['depth'].min())
max_depth = int(df_earthquakes['depth'].max())
depth_range = st.sidebar.slider(
    "Pilih Rentang Kedalaman",
    min_value=min_depth,
    max_value=max_depth,
    value=(min_depth, max_depth)
)

# Filter Tanggal
st.sidebar.subheader("Rentang Waktu")
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(df_earthquakes['tanggal'].min(), df_earthquakes['tanggal'].max()),
    min_value=df_earthquakes['tanggal'].min(),
    max_value=df_earthquakes['tanggal'].max()
)

# Terapkan filter
filtered_df = df_earthquakes[
    (df_earthquakes['magnitude'].between(mag_range[0], mag_range[1])) &
    (df_earthquakes['depth'].between(depth_range[0], depth_range[1])) &
    (df_earthquakes['tanggal'] >= pd.to_datetime(date_range[0])) &
    (df_earthquakes['tanggal'] <= pd.to_datetime(date_range[1]))
]

# ============================
# METRICS - Statistik Utama
# ============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Gempa",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df_earthquakes):,} (filtered)"
    )

with col2:
    avg_magnitude = filtered_df['magnitude'].mean()
    st.metric(
        label="📈 Rata-rata Magnitude",
        value=f"{avg_magnitude:.2f}",
        delta=f"Max: {filtered_df['magnitude'].max():.1f}"
    )

with col3:
    avg_depth = filtered_df['depth'].mean()
    st.metric(
        label="🌊 Rata-rata Kedalaman",
        value=f"{avg_depth:.0f} km",
        delta=f"Max: {filtered_df['depth'].max()} km"
    )

with col4:
    total_regions = filtered_df['remark'].nunique()
    st.metric(
        label="📍 Wilayah Terdampak",
        value=f"{total_regions}",
        delta="Lokasi berbeda"
    )

st.markdown("---")

# ============================
# VISUALISASI BERDASARKAN PILIHAN
# ============================
st.subheader(f"📊 Visualisasi: {visualization_type}")

# Deskripsi untuk setiap jenis visualisasi
if visualization_type == "Pie Chart":
    st.info("📌 **Pie Chart** menampilkan proporsi atau persentase data dalam bentuk lingkaran. "
            "Visualisasi ini cocok untuk melihat kontribusi relatif dari setiap kategori terhadap keseluruhan data.")
elif visualization_type == "Area Chart":
    st.info("📌 **Area Chart** menampilkan tren data dari waktu ke waktu dengan area di bawah garis terisi warna. "
            "Visualisasi ini efektif untuk melihat perubahan dan pola temporal dalam data gempa.")
elif visualization_type == "Bar Chart":
    st.info("📌 **Bar Chart** menampilkan perbandingan nilai antar kategori menggunakan batang horizontal atau vertikal. "
            "Sangat berguna untuk membandingkan jumlah gempa di berbagai wilayah atau kategori kedalaman.")
elif visualization_type == "Line Chart":
    st.info("📌 **Line Chart** menampilkan tren dan pola data dalam bentuk garis yang menghubungkan titik-titik data. "
            "Ideal untuk menganalisis perubahan gempa dari waktu ke waktu dan mengidentifikasi pola musiman.")
elif visualization_type == "Map":
    st.info("📌 **Map** menampilkan sebaran geografis gempa pada peta interaktif. "
            "Visualisasi ini membantu memahami distribusi spasial dan mengidentifikasi hotspot aktivitas seismik.")

st.markdown("---")

if visualization_type == "Pie Chart":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥧 Distribusi Gempa per Wilayah (Top 10)")
        st.caption("Menampilkan 10 wilayah dengan frekuensi gempa tertinggi dalam bentuk persentase.")
        top_10_regions = filtered_df['remark'].value_counts().head(10)
        fig_pie = px.pie(
            values=top_10_regions.values,
            names=top_10_regions.index,
            title='Top 10 Wilayah dengan Gempa Terbanyak',
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### 🥧 Distribusi Berdasarkan Kategori Magnitude")
        st.caption("Mengelompokkan gempa berdasarkan kekuatan magnitude: Kecil, Sedang, Besar, dan Sangat Besar.")
        # Kategorikan magnitude
        def categorize_magnitude(mag):
            if mag < 3.0:
                return "Kecil (< 3.0)"
            elif mag < 4.0:
                return "Sedang (3.0-4.0)"
            elif mag < 5.0:
                return "Besar (4.0-5.0)"
            else:
                return "Sangat Besar (≥ 5.0)"
        
        filtered_df['kategori_magnitude'] = filtered_df['magnitude'].apply(categorize_magnitude)
        mag_counts = filtered_df['kategori_magnitude'].value_counts()
        
        fig_pie_mag = px.pie(
            values=mag_counts.values,
            names=mag_counts.index,
            title='Distribusi Kategori Magnitude',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie_mag, use_container_width=True)

elif visualization_type == "Area Chart":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Tren Jumlah Gempa per Hari")
        st.caption("Menampilkan pola aktivitas gempa harian dengan area terisi untuk melihat intensitas periode tertentu.")
        daily_counts = filtered_df.groupby(filtered_df['tanggal'].dt.date).size().reset_index()
        daily_counts.columns = ['Tanggal', 'Jumlah Gempa']
        
        fig_area = px.area(
            daily_counts,
            x='Tanggal',
            y='Jumlah Gempa',
            title='Aktivitas Gempa Harian',
            labels={'Tanggal': 'Tanggal', 'Jumlah Gempa': 'Jumlah Gempa'}
        )
        fig_area.update_traces(fillcolor='rgba(255, 75, 75, 0.3)', line_color='#FF4B4B')
        st.plotly_chart(fig_area, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Tren Rata-rata Magnitude per Hari")
        st.caption("Memvisualisasikan perubahan kekuatan rata-rata gempa setiap hari untuk mengidentifikasi periode intensitas tinggi.")
        daily_mag = filtered_df.groupby(filtered_df['tanggal'].dt.date)['magnitude'].mean().reset_index()
        daily_mag.columns = ['Tanggal', 'Rata-rata Magnitude']
        
        fig_area_mag = px.area(
            daily_mag,
            x='Tanggal',
            y='Rata-rata Magnitude',
            title='Rata-rata Magnitude Harian',
            labels={'Tanggal': 'Tanggal', 'Rata-rata Magnitude': 'Magnitude'}
        )
        fig_area_mag.update_traces(fillcolor='rgba(255, 107, 107, 0.3)', line_color='#FF6B6B')
        st.plotly_chart(fig_area_mag, use_container_width=True)

elif visualization_type == "Bar Chart":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Top 10 Wilayah dengan Gempa Terbanyak")
        st.caption("Ranking wilayah berdasarkan jumlah kejadian gempa, membantu identifikasi zona rawan gempa.")
        top_regions = filtered_df['remark'].value_counts().head(10).reset_index()
        top_regions.columns = ['Wilayah', 'Jumlah Gempa']
        
        fig_bar = px.bar(
            top_regions,
            x='Jumlah Gempa',
            y='Wilayah',
            orientation='h',
            title='10 Wilayah Terdampak Terbanyak',
            color='Jumlah Gempa',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Distribusi Gempa Berdasarkan Rentang Kedalaman")
        st.caption("Mengelompokkan gempa berdasarkan kedalaman episentrum untuk analisis karakteristik gempa dangkal vs dalam.")
        # Kategorikan kedalaman
        bins = [0, 50, 100, 200, 300, 500]
        labels = ['0-50 km', '50-100 km', '100-200 km', '200-300 km', '300+ km']
        filtered_df['kategori_kedalaman'] = pd.cut(filtered_df['depth'], bins=bins, labels=labels, include_lowest=True)
        depth_counts = filtered_df['kategori_kedalaman'].value_counts().sort_index()
        
        fig_bar_depth = px.bar(
            x=depth_counts.index,
            y=depth_counts.values,
            title='Distribusi Kedalaman Gempa',
            labels={'x': 'Kategori Kedalaman', 'y': 'Jumlah Gempa'},
            color=depth_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar_depth, use_container_width=True)

elif visualization_type == "Line Chart":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Tren Gempa per Bulan")
        st.caption("Menunjukkan pola bulanan kejadian gempa untuk mengidentifikasi tren jangka panjang dan fluktuasi musiman.")
        if not df_stats.empty:
            fig_line = px.line(
                df_stats,
                x='bulan',
                y='jumlah_gempa',
                title='Jumlah Gempa per Bulan',
                labels={'bulan': 'Bulan', 'jumlah_gempa': 'Jumlah Gempa'},
                markers=True
            )
            fig_line.update_traces(line_color='#FF4B4B', marker=dict(size=10))
            st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Tren Magnitude Maksimum per Bulan")
        st.caption("Melacak kekuatan gempa tertinggi setiap bulan untuk memantau periode aktivitas seismik ekstrem.")
        if not df_stats.empty:
            fig_line_mag = px.line(
                df_stats,
                x='bulan',
                y='magnitude_maksimum',
                title='Magnitude Maksimum per Bulan',
                labels={'bulan': 'Bulan', 'magnitude_maksimum': 'Magnitude Maksimum'},
                markers=True
            )
            fig_line_mag.update_traces(line_color='#E63946', marker=dict(size=10))
            st.plotly_chart(fig_line_mag, use_container_width=True)
    
    st.markdown("#### 📈 Distribusi Gempa per Jam dalam Sehari")
    st.caption("Analisis pola temporal harian untuk melihat apakah ada jam-jam tertentu dengan aktivitas gempa lebih tinggi.")
    filtered_df['jam'] = pd.to_datetime(filtered_df['waktu'], format='%H:%M:%S').dt.hour
    hour_counts = filtered_df['jam'].value_counts().sort_index()
    
    fig_line_hour = px.line(
        x=hour_counts.index,
        y=hour_counts.values,
        title='Aktivitas Gempa per Jam (24 jam)',
        labels={'x': 'Jam', 'y': 'Jumlah Gempa'},
        markers=True
    )
    fig_line_hour.update_traces(line_color='#11999E', marker=dict(size=8))
    st.plotly_chart(fig_line_hour, use_container_width=True)

elif visualization_type == "Map":
    st.markdown("#### 🗺️ Peta Sebaran Gempa Interaktif")
    st.caption("Visualisasi geografis yang menampilkan lokasi episentrum gempa dengan ukuran dan warna berdasarkan magnitude.")
    
    # Peta scatter geografis
    fig_map = px.scatter_geo(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='magnitude',
        size='magnitude',
        hover_name='remark',
        hover_data={'tanggal': True, 'waktu': True, 'depth': True, 'magnitude': True, 'latitude': ':.4f', 'longitude': ':.4f'},
        title='Sebaran Gempa Berdasarkan Lokasi Geografis',
        color_continuous_scale='YlOrRd',
        size_max=20
    )
    fig_map.update_geos(
        projection_type="natural earth",
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor='lightgray',
        coastlinecolor='gray',
        showlakes=True,
        lakecolor='lightblue'
    )
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗺️ Peta Kepadatan Gempa (Heatmap)")
        st.caption("Heatmap menunjukkan konsentrasi aktivitas gempa, area merah mengindikasikan zona dengan aktivitas tertinggi.")
        fig_density = px.density_mapbox(
            filtered_df,
            lat='latitude',
            lon='longitude',
            z='magnitude',
            radius=10,
            center=dict(lat=filtered_df['latitude'].mean(), lon=filtered_df['longitude'].mean()),
            zoom=3,
            mapbox_style="open-street-map",
            title='Heatmap Kepadatan Gempa',
            color_continuous_scale='Hot'
        )
        fig_density.update_layout(height=400)
        st.plotly_chart(fig_density, use_container_width=True)
    
    with col2:
        st.markdown("#### 📍 Gempa Terkuat di Peta")
        st.caption("Daftar 5 gempa dengan magnitude tertinggi beserta lokasi koordinat geografisnya.")
        top_5_earthquakes = filtered_df.nlargest(5, 'magnitude')
        st.dataframe(
            top_5_earthquakes[['tanggal', 'waktu', 'magnitude', 'depth', 'remark', 'latitude', 'longitude']],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

# ============================
# TABS - Organisasi Konten
# ============================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Gempa", "📊 Statistik", "🗺️ Peta & Wilayah", "📈 Analisis"])

# TAB 1: Tabel Data Gempa
with tab1:
    st.subheader("📋 Tabel Data Gempa Bumi")
    
    # Pilih kolom yang ditampilkan
    showdata = st.multiselect(
        "Pilih Kolom yang Ditampilkan",
        options=filtered_df.columns,
        default=["tanggal", "waktu", "magnitude", "depth", "remark", "latitude", "longitude"]
    )
    
    # Tampilkan tabel
    st.dataframe(filtered_df[showdata], use_container_width=True, height=400)
    
    # Download CSV
    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df_to_csv(filtered_df[showdata])
    st.download_button(
        label="⬇️ Download Data sebagai CSV",
        data=csv,
        file_name=f'katalog_gempa_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

# TAB 2: Statistik
with tab2:
    st.subheader("📊 Statistik Gempa Bumi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Tren Gempa per Bulan")
        fig_trend = px.line(
            df_stats,
            x='bulan',
            y='jumlah_gempa',
            title='Jumlah Gempa per Bulan',
            labels={'bulan': 'Bulan', 'jumlah_gempa': 'Jumlah Gempa'}
        )
        fig_trend.update_traces(line_color='#FF4B4B')
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("### 🌊 Distribusi Kedalaman Gempa")
        fig_depth = px.histogram(
            filtered_df,
            x='depth',
            nbins=30,
            title='Distribusi Kedalaman Gempa',
            labels={'depth': 'Kedalaman (km)', 'count': 'Frekuensi'}
        )
        fig_depth.update_traces(marker_color='#1f77b4')
        st.plotly_chart(fig_depth, use_container_width=True)
    
    with col2:
        st.markdown("### 💪 Rata-rata Magnitude per Bulan")
        fig_mag = px.bar(
            df_stats,
            x='bulan',
            y='rata_rata_magnitude',
            title='Rata-rata Magnitude per Bulan',
            labels={'bulan': 'Bulan', 'rata_rata_magnitude': 'Rata-rata Magnitude'}
        )
        fig_mag.update_traces(marker_color='#FF6B6B')
        st.plotly_chart(fig_mag, use_container_width=True)
        
        st.markdown("### 📊 Distribusi Magnitude")
        fig_mag_dist = px.histogram(
            filtered_df,
            x='magnitude',
            nbins=20,
            title='Distribusi Magnitude Gempa',
            labels={'magnitude': 'Magnitude', 'count': 'Frekuensi'}
        )
        fig_mag_dist.update_traces(marker_color='#FF9F1C')
        st.plotly_chart(fig_mag_dist, use_container_width=True)

# TAB 3: Peta & Wilayah
with tab3:
    st.subheader("🗺️ Peta Sebaran Gempa")
    
    # Peta scatter
    fig_map = px.scatter_geo(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='magnitude',
        size='magnitude',
        hover_name='remark',
        hover_data={'tanggal': True, 'waktu': True, 'depth': True, 'magnitude': True},
        title='Sebaran Gempa Berdasarkan Lokasi',
        color_continuous_scale='YlOrRd'
    )
    fig_map.update_geos(
        projection_type="natural earth",
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor='lightgray'
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Top 10 Wilayah dengan Gempa Terbanyak")
        top_regions = filtered_df['remark'].value_counts().head(10).reset_index()
        top_regions.columns = ['Wilayah', 'Jumlah Gempa']
        
        fig_regions = px.bar(
            top_regions,
            x='Jumlah Gempa',
            y='Wilayah',
            orientation='h',
            title='10 Wilayah Terdampak Terbanyak'
        )
        fig_regions.update_traces(marker_color='#2EC4B6')
        st.plotly_chart(fig_regions, use_container_width=True)
    
    with col2:
        st.markdown("### 🔥 Gempa dengan Magnitude Tertinggi")
        top_earthquakes = filtered_df.nlargest(10, 'magnitude')[
            ['tanggal', 'waktu', 'magnitude', 'depth', 'remark']
        ]
        st.dataframe(top_earthquakes, use_container_width=True, hide_index=True)

# TAB 4: Analisis
with tab4:
    st.subheader("📈 Analisis Lanjutan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Korelasi Magnitude vs Kedalaman")
        fig_scatter = px.scatter(
            filtered_df,
            x='depth',
            y='magnitude',
            color='magnitude',
            size='magnitude',
            hover_data=['tanggal', 'remark'],
            title='Hubungan Magnitude dengan Kedalaman',
            labels={'depth': 'Kedalaman (km)', 'magnitude': 'Magnitude'},
            color_continuous_scale='Turbo'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("### 📅 Aktivitas Gempa per Hari dalam Seminggu")
        filtered_df['hari'] = filtered_df['tanggal'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = filtered_df['hari'].value_counts().reindex(day_order).fillna(0)
        
        fig_days = px.bar(
            x=day_counts.index,
            y=day_counts.values,
            title='Frekuensi Gempa per Hari',
            labels={'x': 'Hari', 'y': 'Jumlah Gempa'}
        )
        fig_days.update_traces(marker_color='#11999E')
        st.plotly_chart(fig_days, use_container_width=True)
    
    with col2:
        st.markdown("### 🕐 Sebaran Waktu Kejadian Gempa")
        filtered_df['jam'] = pd.to_datetime(filtered_df['waktu'], format='%H:%M:%S').dt.hour
        hour_counts = filtered_df['jam'].value_counts().sort_index()
        
        fig_hours = px.line(
            x=hour_counts.index,
            y=hour_counts.values,
            title='Distribusi Gempa per Jam',
            labels={'x': 'Jam (24h)', 'y': 'Jumlah Gempa'},
            markers=True
        )
        fig_hours.update_traces(line_color='#E63946')
        st.plotly_chart(fig_hours, use_container_width=True)
        
        st.markdown("### 📊 Statistik Deskriptif")
        stats_df = filtered_df[['magnitude', 'depth']].describe()
        st.dataframe(stats_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🌋 Dashboard Katalog Gempa Bumi | Data dari BMKG</p>
    </div>
    """,
    unsafe_allow_html=True
)