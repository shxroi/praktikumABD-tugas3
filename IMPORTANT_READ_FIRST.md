# ⚠️ PENTING - BACA INI SEBELUM DEPLOY! ⚠️

## 🔐 Yang Harus Anda Lakukan SEKARANG:

### 1. Update Password di File `.env` (LOKAL)

Buka file `.env` dan ganti `YOUR_SUPABASE_PASSWORD` dengan password database Supabase Anda yang sebenarnya:

```env
DB_PASSWORD=password_asli_anda_dari_supabase
```

**Cara mendapatkan password:**
1. Buka: https://supabase.com/dashboard
2. Pilih project Anda
3. Settings → Database
4. Lihat "Connection string" → mode URI
5. Password ada di connection string setelah `postgres.hpuczdikgdhrtqimoovt:`

### 2. Update Password di `.streamlit/secrets.toml` (LOKAL)

Buka file `.streamlit/secrets.toml` dan ganti `YOUR_SUPABASE_PASSWORD` dengan password yang sama:

```toml
DB_PASSWORD = "password_asli_anda_dari_supabase"
```

### 3. Test Aplikasi Lokal

Jalankan untuk memastikan koneksi berhasil:

```bash
streamlit run main.py
```

Jika muncul error "password authentication failed", berarti password salah.

## 🚀 Deploy ke Streamlit Cloud

### Langkah 1: Buka Streamlit Cloud
https://share.streamlit.io/

### Langkah 2: New App
- Repository: `shxroi/praktikumABD-tugas3`
- Branch: `main`
- Main file: `main.py`

### Langkah 3: SECRETS (PALING PENTING!)

Di Advanced Settings → Secrets, copy-paste ini dan GANTI PASSWORD:

```toml
DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
DB_PORT = "6543"
DB_NAME = "postgres"
DB_USER = "postgres.hpuczdikgdhrtqimoovt"
DB_PASSWORD = "password_asli_anda_dari_supabase"
```

⚠️ GANTI `password_asli_anda_dari_supabase` dengan password Supabase Anda!

### Langkah 4: Deploy!

Klik tombol **Deploy** dan tunggu 2-5 menit.

## ✅ Checklist

- [ ] Password sudah diganti di `.env`
- [ ] Password sudah diganti di `.streamlit/secrets.toml`
- [ ] Test lokal berhasil (`streamlit run main.py`)
- [ ] Tabel sudah ada di Supabase (cek di SQL Editor)
- [ ] Data sudah diimport ke Supabase (50 rows)
- [ ] Deploy ke Streamlit Cloud
- [ ] Secrets sudah dikonfigurasi di Streamlit Cloud
- [ ] Aplikasi berhasil online tanpa error

## 🆘 Jika Ada Error

1. **Authentication failed**: Password salah di Secrets
2. **Connection refused**: Cek Supabase masih aktif
3. **Table not found**: Jalankan `schema.sql` di Supabase
4. **No data**: Insert data dari `schema.sql`

## 📞 Link Penting

- Supabase Dashboard: https://supabase.com/dashboard
- Streamlit Cloud: https://share.streamlit.io/
- GitHub Repo: https://github.com/shxroi/praktikumABD-tugas3
- Deployment Guide: Lihat `DEPLOYMENT_GUIDE.md`

---

**INGAT: Jangan push file `.env` atau `secrets.toml` ke GitHub!**
(Sudah ada di `.gitignore` jadi aman)
