import psycopg2
import csv
from datetime import datetime
from config import Config

def connect_db():
    """Membuat koneksi ke database"""
    try:
        conn = psycopg2.connect(**Config.get_connection_params())
        print("✓ Koneksi ke database berhasil!")
        return conn
    except Exception as e:
        print(f"✗ Error koneksi database: {e}")
        return None

def parse_date(date_str):
    """Mengkonversi format tanggal dari CSV"""
    # Format: 1/1/2018 -> 2018-01-01
    parts = date_str.split('/')
    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
    return f"{year:04d}-{month:02d}-{day:02d}"

def parse_time(time_str):
    """Mengkonversi format waktu dari CSV"""
    # Format: 22.48.13 -> 22:48:13
    return time_str.replace('.', ':')

def import_csv_to_db(csv_file):
    """Import data dari CSV ke database"""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            count = 0
            for row in csv_reader:
                try:
                    tanggal = parse_date(row['tgl'])
                    waktu = parse_time(row['ot'])
                    latitude = float(row['lat'])
                    longitude = float(row['lon'])
                    depth = int(row['depth'])
                    magnitude = float(row['mag'])
                    remark = row['remark']
                    
                    cursor.execute("""
                        INSERT INTO katalog_gempa 
                        (tanggal, waktu, latitude, longitude, depth, magnitude, remark)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (tanggal, waktu, latitude, longitude, depth, magnitude, remark))
                    
                    count += 1
                    if count % 100 == 0:
                        print(f"✓ {count} data berhasil diimport...")
                        
                except Exception as e:
                    print(f"✗ Error pada baris: {row}")
                    print(f"  Detail error: {e}")
                    continue
            
            conn.commit()
            print(f"\n✓ Total {count} data berhasil diimport ke database!")
            
    except Exception as e:
        print(f"✗ Error saat import data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def query_example():
    """Contoh query untuk mengambil data"""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Query 1: Gempa dengan magnitude tertinggi
        print("\n=== 10 Gempa dengan Magnitude Tertinggi ===")
        cursor.execute("""
            SELECT tanggal, waktu, latitude, longitude, magnitude, remark
            FROM katalog_gempa
            ORDER BY magnitude DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            print(f"{row[0]} {row[1]} | Mag: {row[4]} | {row[5]}")
        
        # Query 2: Statistik per bulan
        print("\n=== Statistik Gempa per Bulan ===")
        cursor.execute("SELECT * FROM statistik_gempa LIMIT 5")
        
        for row in cursor.fetchall():
            print(f"Bulan: {row[0]} | Jumlah: {row[1]} | Rata-rata Mag: {row[2]:.2f}")
        
        # Query 3: Jumlah gempa per wilayah
        print("\n=== 10 Wilayah dengan Gempa Terbanyak ===")
        cursor.execute("""
            SELECT remark, COUNT(*) as jumlah
            FROM katalog_gempa
            GROUP BY remark
            ORDER BY jumlah DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} gempa")
            
    except Exception as e:
        print(f"✗ Error saat query: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=== Program Import Data Gempa ===\n")
    
    # Import data dari CSV
    csv_file = "katalog_gempa_new.csv"
    import_csv_to_db(csv_file)
    
    # Contoh query
    query_example()
