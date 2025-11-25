import psycopg2
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Variabel global untuk koneksi
conn = None
c = None

def get_connection():
    """Membuat atau mengembalikan koneksi database"""
    global conn, c
    if conn is None:
        try:
            # Debug: Cek .env terbaca atau tidak
            print(f"🔍 DEBUG - DB_HOST dari .env: {os.getenv('DB_HOST')}")
            print(f"🔍 DEBUG - DB_PORT dari .env: {os.getenv('DB_PORT')}")
            print(f"🔍 DEBUG - DB_NAME dari .env: {os.getenv('DB_NAME')}")
            
            # Cek apakah ada st.secrets (untuk Streamlit Cloud)
            use_secrets = False
            try:
                if hasattr(st, 'secrets') and 'DB_HOST' in st.secrets:
                    use_secrets = True
                    print("🔍 DEBUG - Menggunakan st.secrets")
            except:
                use_secrets = False
                print("🔍 DEBUG - Menggunakan .env file")
            
            if use_secrets:
                # Di Streamlit Cloud, gunakan st.secrets
                db_config = {
                    'host': st.secrets["DB_HOST"],
                    'port': int(st.secrets.get("DB_PORT", "5432")),
                    'database': st.secrets.get("DB_NAME", "postgres"),
                    'user': st.secrets.get("DB_USER", "postgres"),
                    'password': st.secrets["DB_PASSWORD"]
                }
            else:
                # Di local, gunakan .env - FORCE SUPABASE VALUES
                db_host = os.getenv('DB_HOST')
                if not db_host or db_host == 'localhost':
                    print("⚠️ WARNING: DB_HOST tidak terbaca atau masih localhost!")
                    st.warning("⚠️ File .env mungkin tidak terbaca. Menggunakan konfigurasi Supabase default.")
                    db_host = 'db.hpuczdikgdhrtqimoovt.supabase.co'
                
                db_config = {
                    'host': db_host,
                    'port': int(os.getenv('DB_PORT', '5432')),
                    'database': os.getenv('DB_NAME', 'postgres'),
                    'user': os.getenv('DB_USER', 'postgres'),
                    'password': os.getenv('DB_PASSWORD', '0WiWduMkDzytHnL5')
                }
            
            # Debug info (tanpa password)
            print(f"🔌 Connecting to: {db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
            st.info(f"🔌 Connecting: {db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
            
            conn = psycopg2.connect(**db_config)
            c = conn.cursor()
            st.success("✅ Koneksi database berhasil!")
            print("✓ Koneksi PostgreSQL berhasil!")
            
        except Exception as e:
            print(f"✗ Error koneksi database: {e}")
            st.error(f"❌ Gagal koneksi ke database: {e}")
            st.info("💡 Pastikan database PostgreSQL sudah running dan konfigurasi sudah benar.")
            raise
    return conn, c

# ============================
# Fungsi ambil data dari tabel
# ============================

def view_all_earthquakes():
    """Mengambil semua data gempa"""
    _, cursor = get_connection()
    query = '''
        SELECT id, tanggal, waktu, latitude, longitude, depth, magnitude, remark
        FROM katalog_gempa
        ORDER BY tanggal DESC, waktu DESC
    '''
    cursor.execute(query)
    return cursor.fetchall()

def view_statistics_by_month():
    """Mengambil statistik gempa per bulan"""
    _, cursor = get_connection()
    query = '''
        SELECT 
            bulan,
            jumlah_gempa,
            rata_rata_magnitude,
            magnitude_maksimum,
            magnitude_minimum
        FROM statistik_gempa
        ORDER BY bulan DESC
    '''
    cursor.execute(query)
    return cursor.fetchall()

def view_top_earthquakes(limit=10):
    """Mengambil gempa dengan magnitude tertinggi"""
    _, cursor = get_connection()
    query = '''
        SELECT tanggal, waktu, latitude, longitude, magnitude, remark
        FROM katalog_gempa
        ORDER BY magnitude DESC
        LIMIT %s
    '''
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def view_earthquakes_by_region():
    """Mengambil jumlah gempa per wilayah"""
    _, cursor = get_connection()
    query = '''
        SELECT remark, COUNT(*) as jumlah
        FROM katalog_gempa
        GROUP BY remark
        ORDER BY jumlah DESC
    '''
    cursor.execute(query)
    return cursor.fetchall()

def view_earthquakes_by_magnitude_range(min_mag, max_mag):
    """Mengambil gempa berdasarkan rentang magnitude"""
    _, cursor = get_connection()
    query = '''
        SELECT id, tanggal, waktu, latitude, longitude, depth, magnitude, remark
        FROM katalog_gempa
        WHERE magnitude BETWEEN %s AND %s
        ORDER BY magnitude DESC
    '''
    cursor.execute(query, (min_mag, max_mag))
    return cursor.fetchall()

def view_earthquakes_by_depth_range(min_depth, max_depth):
    """Mengambil gempa berdasarkan rentang kedalaman"""
    _, cursor = get_connection()
    query = '''
        SELECT id, tanggal, waktu, latitude, longitude, depth, magnitude, remark
        FROM katalog_gempa
        WHERE depth BETWEEN %s AND %s
        ORDER BY depth DESC
    '''
    cursor.execute(query, (min_depth, max_depth))
    return cursor.fetchall()

class Config:
    """Konfigurasi database PostgreSQL (backward compatibility)"""
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'earthquake_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    @staticmethod
    def get_connection_string():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    
    @staticmethod
    def get_connection_params():
        return {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }