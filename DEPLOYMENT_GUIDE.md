# 📝 DEPLOYMENT_GUIDE.md

Panduan lengkap untuk deploy Dashboard Katalog Gempa ke Streamlit Cloud dengan Supabase.

## 🎯 Checklist Deployment

### ✅ Persiapan

- [x] Database Supabase sudah dibuat
- [x] Tabel `katalog_gempa` sudah ada
- [x] Data sample sudah diimport (50 data)
- [x] View `statistik_gempa` sudah dibuat
- [ ] Password database Supabase sudah dicatat
- [ ] Repository GitHub sudah di-push

### ✅ File yang Harus Ada

```
praktikumABD-tugas3/
├── main.py                    ✅
├── config.py                  ✅
├── requirements.txt           ✅
├── .gitignore                 ✅
├── README.md                  ✅
├── .streamlit/
│   └── secrets.toml.example   ✅
```

## 🚀 Langkah-langkah Deploy

### 1. Pastikan Database Supabase Ready

1. **Login ke Supabase**: https://supabase.com/dashboard
2. **Pilih project Anda**
3. **SQL Editor** → Jalankan query ini untuk cek data:

```sql
-- Cek jumlah data
SELECT COUNT(*) FROM katalog_gempa;

-- Cek view statistik
SELECT * FROM statistik_gempa LIMIT 5;
```

Jika belum ada data, jalankan file `schema.sql` di SQL Editor.

### 2. Dapatkan Kredensial Database

1. Di Supabase Dashboard → **Settings** → **Database**
2. Scroll ke **Connection string**
3. Pilih mode: **URI**
4. Copy connection string:
   ```
   postgresql://postgres.hpuczdikgdhrtqimoovt:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```
5. Catat:
   - Host: `aws-0-ap-southeast-1.pooler.supabase.com`
   - Port: `6543`
   - Database: `postgres`
   - User: `postgres.hpuczdikgdhrtqimoovt`
   - Password: `[YOUR-PASSWORD]`

### 3. Update File `.env` (Untuk Lokal)

Edit file `.env`:
```env
DB_HOST=aws-0-ap-southeast-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.hpuczdikgdhrtqimoovt
DB_PASSWORD=your_actual_password_here
```

⚠️ **PENTING**: Ganti `your_actual_password_here` dengan password sebenarnya!

### 4. Test Lokal (Opsional)

```bash
# Install dependencies
pip install -r requirements.txt

# Test run lokal
streamlit run main.py
```

Jika berhasil, lanjut ke step berikutnya.

### 5. Push ke GitHub

```bash
# Add semua file (kecuali yang di .gitignore)
git add .

# Commit
git commit -m "Setup Supabase database connection"

# Push ke GitHub
git push origin main
```

### 6. Deploy ke Streamlit Cloud

#### A. Buka Streamlit Cloud

1. Buka: https://share.streamlit.io/
2. Login dengan akun GitHub Anda

#### B. Create New App

1. Klik **New app**
2. Isi form:
   - **Repository**: `shxroi/praktikumABD-tugas3`
   - **Branch**: `main`
   - **Main file path**: `main.py`
3. Klik **Advanced settings** (jangan langsung Deploy)

#### C. Konfigurasi Secrets

1. Di **Advanced settings** → **Secrets**
2. Copy-paste kredensial Supabase Anda:

```toml
DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
DB_PORT = "6543"
DB_NAME = "postgres"
DB_USER = "postgres.hpuczdikgdhrtqimoovt"
DB_PASSWORD = "your_actual_password_here"
```

⚠️ **PENTING**: 
- Ganti `your_actual_password_here` dengan password database Supabase yang sebenarnya
- Pastikan tidak ada typo
- Pastikan format TOML benar (gunakan tanda kutip)

#### D. Deploy

1. Klik **Deploy!**
2. Tunggu proses deployment (2-5 menit)
3. Aplikasi akan otomatis terbuka setelah selesai

### 7. Verifikasi Deployment

Setelah deploy berhasil:

✅ **Cek ini:**
1. Dashboard terbuka tanpa error
2. Data gempa muncul di tabel
3. Semua visualisasi berfungsi
4. Filter bekerja dengan baik
5. Export CSV berfungsi

❌ **Jika ada error:**
1. Klik **Manage app** → **Logs**
2. Lihat error message
3. Perbaiki sesuai error (lihat Troubleshooting di bawah)

## 🔧 Troubleshooting

### Error: "Connection refused" atau "Authentication failed"

**Penyebab**: Password salah atau Secrets belum dikonfigurasi

**Solusi**:
1. Cek Secrets di Streamlit Cloud
2. Pastikan password benar (cek di Supabase Dashboard)
3. Reboot app: **Manage app** → **Reboot app**

### Error: "relation katalog_gempa does not exist"

**Penyebab**: Tabel belum dibuat di Supabase

**Solusi**:
1. Buka Supabase SQL Editor
2. Jalankan file `schema.sql`
3. Reboot app di Streamlit Cloud

### Error: "ModuleNotFoundError"

**Penyebab**: Dependency tidak terinstall

**Solusi**:
1. Pastikan `requirements.txt` ter-push
2. Clear cache di Streamlit Cloud
3. Reboot app

### Dashboard kosong / No data

**Penyebab**: Data belum diimport ke Supabase

**Solusi**:
1. Di Supabase SQL Editor, jalankan bagian INSERT dari `schema.sql`
2. Atau jalankan: `python import_data.py` (dengan kredensial Supabase di `.env`)

## 🎉 Selesai!

Jika semua langkah berhasil, aplikasi Anda sudah online dan bisa diakses publik!

**Share URL aplikasi Anda:**
```
https://your-app-name.streamlit.app
```

## 📋 Post-Deployment

### Update Aplikasi

Setiap kali Anda push ke GitHub, Streamlit Cloud akan otomatis rebuild:

```bash
git add .
git commit -m "Update feature XYZ"
git push origin main
```

### Monitoring

- **Logs**: Streamlit Cloud Dashboard → Logs
- **Usage**: Dashboard → Analytics
- **Errors**: Email notification (jika diaktifkan)

## 🔐 Keamanan

✅ **Yang sudah aman:**
- `.env` tidak ter-push (ada di `.gitignore`)
- `secrets.toml` tidak ter-push (ada di `.gitignore`)
- Password hanya di Streamlit Secrets
- Koneksi Supabase menggunakan SSL

⚠️ **Jangan:**
- Push `.env` ke GitHub
- Hardcode password di code
- Share secrets.toml di public
- Expose API keys di frontend

## 📞 Butuh Bantuan?

Jika masih ada masalah:
1. Cek logs di Streamlit Cloud
2. Cek connection di Supabase Dashboard
3. Buat issue di GitHub repository
4. Hubungi maintainer

---

**Good luck dengan deployment! 🚀**
