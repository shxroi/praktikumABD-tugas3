
-- Membuat tabel katalog_gempa
CREATE TABLE katalog_gempa (
    id SERIAL PRIMARY KEY,
    tanggal DATE NOT NULL,
    waktu TIME NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    depth INTEGER NOT NULL,
    magnitude DECIMAL(3, 1) NOT NULL,
    remark VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Membuat index untuk mempercepat query
CREATE INDEX idx_tanggal ON katalog_gempa(tanggal);
CREATE INDEX idx_magnitude ON katalog_gempa(magnitude);
CREATE INDEX idx_location ON katalog_gempa(latitude, longitude);
CREATE INDEX idx_remark ON katalog_gempa(remark);

-- Membuat view untuk statistik gempa per bulan
CREATE VIEW statistik_gempa AS
SELECT 
    DATE_TRUNC('month', tanggal) as bulan,
    COUNT(*) as jumlah_gempa,
    AVG(magnitude) as rata_rata_magnitude,
    MAX(magnitude) as magnitude_maksimum,
    MIN(magnitude) as magnitude_minimum
FROM katalog_gempa
GROUP BY DATE_TRUNC('month', tanggal)
ORDER BY bulan;

-- ============================
-- DML - Insert Data Sample (20 data pertama)
-- ============================

INSERT INTO katalog_gempa (tanggal, waktu, latitude, longitude, depth, magnitude, remark) VALUES
('2018-01-01', '22:48:13', -0.01, 122.55, 158, 2.4, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '22:28:09', -0.20, 125.41, 10, 3.3, 'Southern Molucca Sea'),
('2018-01-01', '18:32:23', -8.30, 123.53, 10, 2.9, 'Flores Region - Indonesia'),
('2018-01-01', '17:46:55', 1.01, 132.52, 10, 3.3, 'Irian Jaya Region - Indonesia'),
('2018-01-01', '17:38:34', 0.27, 121.83, 170, 2.6, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '16:32:39', -8.49, 121.30, 181, 4.5, 'Flores Region - Indonesia'),
('2018-01-01', '16:25:36', -7.96, 116.84, 288, 4.5, 'Bali Sea'),
('2018-01-01', '16:16:03', -9.82, 124.25, 10, 3.1, 'Timor Region'),
('2018-01-01', '16:05:55', -7.66, 119.28, 19, 3.5, 'Flores Sea'),
('2018-01-01', '15:55:24', -9.48, 118.11, 22, 3.1, 'Sumbawa Region - Indonesia'),
('2018-01-01', '10:40:24', -6.90, 106.83, 10, 3.3, 'Java - Indonesia'),
('2018-01-01', '09:17:58', -3.51, 119.10, 22, 2.5, 'Sulawesi - Indonesia'),
('2018-01-01', '09:04:34', -0.28, 125.35, 10, 4.0, 'Southern Molucca Sea'),
('2018-01-01', '09:03:10', -0.72, 131.12, 17, 2.5, 'Irian Jaya Region - Indonesia'),
('2018-01-01', '07:48:02', 0.59, 122.34, 61, 1.7, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '07:32:00', -0.23, 122.94, 12, 2.7, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '07:26:02', -4.41, 102.14, 43, 4.8, 'Southern Sumatra - Indonesia'),
('2018-01-01', '06:22:42', -6.46, 101.70, 10, 4.9, 'Southwest of Sumatra - Indonesia'),
('2018-01-01', '05:22:39', 0.19, 121.95, 155, 2.4, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '04:59:02', 2.31, 97.06, 59, 2.9, 'Northern Sumatra - Indonesia'),
('2018-01-01', '04:30:53', -0.24, 123.07, 63, 2.3, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '03:32:14', -3.24, 128.84, 10, 3.5, 'Seram - Indonesia'),
('2018-01-01', '03:24:54', -6.11, 130.34, 157, 4.3, 'Banda Sea'),
('2018-01-01', '03:07:10', 1.42, 122.04, 17, 1.9, 'Minahassa Peninsula - Sulawesi'),
('2018-01-01', '03:03:26', -9.42, 117.90, 24, 2.4, 'Sumbawa Region - Indonesia'),
('2018-01-01', '02:47:54', -1.40, 120.47, 10, 2.4, 'Sulawesi - Indonesia'),
('2018-01-01', '00:52:33', -0.33, 123.73, 112, 5.1, 'Minahassa Peninsula - Sulawesi'),
('2018-01-02', '23:35:04', -3.02, 127.74, 57, 3.1, 'Seram - Indonesia'),
('2018-01-02', '23:24:28', -5.27, 104.51, 82, 3.1, 'Southern Sumatra - Indonesia'),
('2018-01-02', '21:14:17', -7.61, 128.40, 12, 4.3, 'Banda Sea'),
('2018-01-02', '20:58:34', -7.02, 107.77, 295, 2.7, 'Java - Indonesia'),
('2018-01-02', '20:47:28', -0.15, 123.55, 12, 2.5, 'Minahassa Peninsula - Sulawesi'),
('2018-01-02', '20:30:51', 0.74, 120.30, 12, 3.0, 'Minahassa Peninsula - Sulawesi'),
('2018-01-02', '17:47:12', -0.02, 123.52, 120, 4.5, 'Minahassa Peninsula - Sulawesi'),
('2018-01-02', '17:33:08', -2.93, 127.78, 28, 3.7, 'Ceram Sea'),
('2018-01-02', '15:33:09', -8.29, 115.50, 11, 2.4, 'Bali Region - Indonesia'),
('2018-01-02', '14:40:32', 2.34, 98.93, 129, 3.4, 'Northern Sumatra - Indonesia'),
('2018-01-02', '13:44:38', -8.68, 118.36, 106, 3.3, 'Sumbawa Region - Indonesia'),
('2018-01-02', '13:23:46', -8.74, 118.35, 92, 2.9, 'Sumbawa Region - Indonesia'),
('2018-01-02', '11:54:33', -6.52, 129.86, 172, 4.2, 'Banda Sea'),
('2018-01-02', '09:53:01', 3.72, 126.58, 12, 3.7, 'Talaud Islands - Indonesia'),
('2018-01-02', '09:50:56', -9.32, 122.43, 14, 2.8, 'Savu Sea'),
('2018-01-02', '07:11:57', 1.40, 99.70, 185, 4.3, 'Northern Sumatra - Indonesia'),
('2018-01-02', '06:46:06', 0.29, 122.48, 12, 2.8, 'Minahassa Peninsula - Sulawesi'),
('2018-01-02', '03:52:52', -9.98, 124.96, 18, 3.0, 'Timor Region'),
('2018-01-02', '02:27:03', 4.56, 124.45, 10, 3.5, 'Celebes Sea'),
('2018-01-02', '02:21:30', -8.29, 119.99, 172, 3.9, 'Flores Region - Indonesia'),
('2018-01-02', '01:47:45', -7.31, 128.29, 196, 4.1, 'Banda Sea'),
('2018-01-02', '01:40:50', -9.62, 115.48, 17, 3.1, 'South of Bali - Indonesia');

-- Menampilkan struktur tabel
\d katalog_gempa
