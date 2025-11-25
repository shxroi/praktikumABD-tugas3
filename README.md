# 🌋 Dashboard Katalog Gempa - PostgreSQL & Streamlit

Proyek dashboard interaktif untuk menganalisis dan memvisualisasikan data gempa bumi dari CSV ke database PostgreSQL menggunakan Streamlit.

## 📋 Persyaratan
- Python 3.8+
- PostgreSQL 12+
- pip

## 🚀 Instalasi

### 1. Install Dependencies Python
```powershell
pip install -r requirements.txt
```

Dependencies yang akan terinstall:
- `streamlit` - Framework dashboard web
- `pandas` - Manipulasi data
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variables
- `plotly` - Visualisasi interaktif

### 2. Setup Database PostgreSQL

**Cara 1: Menggunakan psql (Command Line)**
```powershell
# Buat database
psql -U postgres -c "CREATE DATABASE earthquake_db;"

# Jalankan schema
psql -U postgres -d earthquake_db -f schema.sql
```

**Cara 2: Menggunakan pgAdmin**
1. Buka pgAdmin
2. Klik kanan pada "Databases" → Create → Database
3. Nama database: `earthquake_db`
4. Klik kanan pada database → Query Tool
5. Copy-paste isi file `schema.sql` → Execute

**Cara 3: Menggunakan DBeaver/Database Client Lainnya**
1. Buat koneksi ke PostgreSQL
2. Buat database baru: `earthquake_db`
3. Buka SQL Editor
4. Jalankan isi file `schema.sql`

### 3. Konfigurasi Environment
Edit file `.env` sesuai dengan konfigurasi PostgreSQL Anda:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=earthquake_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Import Data CSV ke Database
Sebelum menjalankan dashboard, import data terlebih dahulu:
```powershell
python import_data.py
```

Program akan mengimport semua data dari `katalog_gempa_new.csv` ke database PostgreSQL.

## 🎯 Cara Menjalankan Dashboard

```powershell
streamlit run main.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 🎨 Fitur Dashboard

### 1. **Filter Interaktif (Sidebar)**
   - Filter rentang magnitude (slider)
   - Filter rentang kedalaman (slider)
   - Filter rentang tanggal (date picker)

### 2. **Metrics Overview**
   - Total gempa (dengan counter filtered data)
   - Rata-rata magnitude
   - Rata-rata kedalaman
   - Jumlah wilayah terdampak

### 3. **Tab: Data Gempa** 📋
   - Tabel data lengkap dengan filter
   - Pilihan kolom yang ditampilkan (multiselect)
   - Export ke CSV

### 4. **Tab: Statistik** 📊
   - Line chart: Tren gempa per bulan
   - Bar chart: Rata-rata magnitude per bulan
   - Histogram: Distribusi kedalaman
   - Histogram: Distribusi magnitude

### 5. **Tab: Peta & Wilayah** 🗺️
   - Peta geografis sebaran gempa (scatter geo map)
   - Top 10 wilayah dengan gempa terbanyak
   - Tabel gempa dengan magnitude tertinggi

### 6. **Tab: Analisis** 📈
   - Scatter plot: Korelasi magnitude vs kedalaman
   - Bar chart: Aktivitas gempa per hari dalam seminggu
   - Line chart: Distribusi gempa per jam
   - Statistik deskriptif (describe)

## 📁 Struktur File

```
Tugas 3/
├── main.py                    # Dashboard Streamlit
├── import_data.py             # Script import CSV ke database
├── config.py                  # Konfigurasi database & fungsi query
├── schema.sql                 # DDL database
├── katalog_gempa_new.csv     # Data gempa (source)
├── requirements.txt           # Dependencies Python
├── .env                       # Konfigurasi environment
└── README.md                  # Dokumentasi
```

## 🗄️ Struktur Database

### Tabel: katalog_gempa
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | SERIAL | Primary key |
| tanggal | DATE | Tanggal gempa |
| waktu | TIME | Waktu gempa |
| latitude | DECIMAL(10,6) | Lintang |
| longitude | DECIMAL(10,6) | Bujur |
| depth | INTEGER | Kedalaman (km) |
| magnitude | DECIMAL(3,1) | Kekuatan gempa |
| remark | VARCHAR(255) | Lokasi/wilayah |
| created_at | TIMESTAMP | Waktu input data |

### View: statistik_gempa
Menyediakan statistik gempa per bulan:
- Jumlah gempa
- Rata-rata magnitude
- Magnitude maksimum dan minimum

## Troubleshooting

### Error: "database earthquake_db does not exist"
**Solusi:** Buat database terlebih dahulu
```bash
psql -U postgres -c "CREATE DATABASE earthquake_db;"
```

### Error: "relation katalog_gempa does not exist"
**Solusi:** Jalankan schema.sql
```bash
psql -U postgres -d earthquake_db -f schema.sql
```

### Error: "password authentication failed"
**Solusi:** Periksa kredensial di file `.env`

### Error: "ModuleNotFoundError: No module named 'psycopg2'"
**Solusi:** Install dependencies
```bash
pip install -r requirements.txt
```

## Contoh Query

```sql
-- Gempa terkuat
SELECT * FROM katalog_gempa ORDER BY magnitude DESC LIMIT 10;

-- Statistik per bulan
SELECT * FROM statistik_gempa;

-- Wilayah dengan gempa terbanyak
SELECT remark, COUNT(*) 
FROM katalog_gempa 
GROUP BY remark 
ORDER BY COUNT(*) DESC 
LIMIT 10;
```
