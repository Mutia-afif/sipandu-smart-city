-- Migrasi Awal: SIPANDU Smart City (Kota Bandar Lampung)
-- Proyek UTS PPSI: Mutia Afif Ramadhani (24311124) | Dosen: Dr. Erliyan Redy Susanto, M.Kom

-- 1. Ekstensi
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 2. Tipe ENUM
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('warga', 'petugas', 'admin');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE aduan_status AS ENUM ('pending', 'verified', 'rejected', 'in_progress', 'resolved');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE prioritas_level AS ENUM ('rendah', 'sedang', 'tinggi');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Tabel Master Dinas
CREATE TABLE IF NOT EXISTS dinas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama VARCHAR(120) NOT NULL UNIQUE,
    deskripsi TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Tabel Pengguna (Users) - TIDAK ADA NIK
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    no_hp VARCHAR(25) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'warga',
    dinas_id UUID REFERENCES dinas(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Tabel Kategori Aduan
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama_kategori VARCHAR(100) NOT NULL UNIQUE,
    dinas_id UUID NOT NULL REFERENCES dinas(id) ON DELETE RESTRICT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Tabel Aduan Utama (dengan kolom geom PostGIS dan version untuk Optimistic Lock)
CREATE TABLE IF NOT EXISTS aduan (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    no_aduan VARCHAR(30) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    dinas_id UUID REFERENCES dinas(id) ON DELETE SET NULL,
    judul VARCHAR(200) NOT NULL,
    deskripsi TEXT NOT NULL,
    geom geometry(Point, 4326) NOT NULL,
    alamat_teks TEXT,
    status aduan_status NOT NULL DEFAULT 'pending',
    prioritas prioritas_level NOT NULL DEFAULT 'sedang',
    alasan_penolakan TEXT,
    catatan_penanganan TEXT,
    version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Tabel Foto Aduan (Pelapor & Penanganan Petugas)
CREATE TABLE IF NOT EXISTS aduan_foto (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aduan_id UUID NOT NULL REFERENCES aduan(id) ON DELETE CASCADE,
    jenis VARCHAR(20) NOT NULL CHECK (jenis IN ('laporan', 'penanganan')),
    storage_key VARCHAR(255) NOT NULL,
    ukuran INT NOT NULL,
    mime VARCHAR(50) NOT NULL,
    diunggah_oleh UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Tabel Log Perubahan Status Aduan
CREATE TABLE IF NOT EXISTS aduan_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aduan_id UUID NOT NULL REFERENCES aduan(id) ON DELETE CASCADE,
    changed_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status_lama aduan_status,
    status_baru aduan_status NOT NULL,
    catatan TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 9. Tabel Audit Trail Sistem (Immutable)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    role VARCHAR(20) NOT NULL,
    aksi VARCHAR(100) NOT NULL,
    entitas VARCHAR(50) NOT NULL,
    entitas_id UUID,
    nilai_lama JSONB,
    nilai_baru JSONB,
    ip VARCHAR(45),
    waktu TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 10. Tabel Sesi Server-Side
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(128) PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. Indeks Spasial & Kueri Cepat
CREATE INDEX IF NOT EXISTS idx_aduan_geom ON aduan USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_aduan_status_created ON aduan(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_aduan_dinas_status ON aduan(dinas_id, status);
CREATE INDEX IF NOT EXISTS idx_aduan_user_id ON aduan(user_id);
CREATE INDEX IF NOT EXISTS idx_aduan_logs_aduan_id ON aduan_logs(aduan_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- 12. Seeder Data Awal
-- A. Dinas
INSERT INTO dinas (id, nama, deskripsi) VALUES
('11111111-1111-1111-1111-111111111111', 'Dinas Pekerjaan Umum', 'Penanganan jalan berlubang, drainase, dan fasilitas umum')
ON CONFLICT (nama) DO NOTHING;

INSERT INTO dinas (id, nama, deskripsi) VALUES
('22222222-2222-2222-2222-222222222222', 'Dinas Perumahan dan Kawasan Permukiman', 'Penanganan permukiman dan tata ruang kota')
ON CONFLICT (nama) DO NOTHING;

INSERT INTO dinas (id, nama, deskripsi) VALUES
('33333333-3333-3333-3333-333333333333', 'Dinas Perhubungan', 'Penanganan Penerangan Jalan Umum (PJU) dan marka lalu lintas')
ON CONFLICT (nama) DO NOTHING;

-- B. 3 Kategori MVP
INSERT INTO categories (id, nama_kategori, dinas_id) VALUES
('44444444-4444-4444-4444-444444444444', 'Jalan Berlubang', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (nama_kategori) DO NOTHING;

INSERT INTO categories (id, nama_kategori, dinas_id) VALUES
('55555555-5555-5555-5555-555555555555', 'PJU Padam', '33333333-3333-3333-3333-333333333333')
ON CONFLICT (nama_kategori) DO NOTHING;

INSERT INTO categories (id, nama_kategori, dinas_id) VALUES
('66666666-6666-6666-6666-666666666666', 'Drainase Tersumbat', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (nama_kategori) DO NOTHING;

-- C. Akun Dummy (Password hash default menggunakan argon2id untuk testing)
-- Password default: 'rahasia123' -> $argon2id$v=19$m=19456,t=2,p=1$u320sB3NfO... (placeholder kompatibel)
INSERT INTO users (id, nama, email, no_hp, password_hash, role, dinas_id) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Admin Command Center', 'admin@bandarlampung.go.id', '081234567890', '$argon2id$v=19$m=19456,t=2,p=1$ZGVmYXVsdHNhbHQ$WJ7k1Kpzr+jN1o/P5s03Z/7c97P6pG1r9jNqL8uKx7k', 'admin', NULL)
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, nama, email, no_hp, password_hash, role, dinas_id) VALUES
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Pak Dedi (Petugas PU)', 'petugas.pu@bandarlampung.go.id', '081234567891', '$argon2id$v=19$m=19456,t=2,p=1$ZGVmYXVsdHNhbHQ$WJ7k1Kpzr+jN1o/P5s03Z/7c97P6pG1r9jNqL8uKx7k', 'petugas', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, nama, email, no_hp, password_hash, role, dinas_id) VALUES
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Bu Sari (Warga)', 'warga@gmail.com', '081234567892', '$argon2id$v=19$m=19456,t=2,p=1$ZGVmYXVsdHNhbHQ$WJ7k1Kpzr+jN1o/P5s03Z/7c97P6pG1r9jNqL8uKx7k', 'warga', NULL)
ON CONFLICT (email) DO NOTHING;

