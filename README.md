# SIPANDU Smart City - Kota Bandar Lampung
### Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu

<p align="center">
  <img src="static/img/logo_pemda.png" alt="Logo Pemda Kota Bandar Lampung" height="80"/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="static/img/logo_uti.png" alt="Logo Universitas Teknokrat Indonesia" height="80"/>
</p>

| Atribut | Keterangan |
|---|---|
| **Mata Kuliah** | Proyek Pengembangan Sistem Informasi (PPSI) - Ujian Tengah Semester (UTS) |
| **Penyusun** | **Mutia Afif Ramadhani** (NPM: 24311124, Kelas: SI 23A) |
| **Dosen Pengampu** | **Dr. Erliyan Redy Susanto, M.Kom** |
| **Institusi** | Program Studi Sistem Informasi, Universitas Teknokrat Indonesia |
| **Wilayah Layanan** | Kota Bandar Lampung, Provinsi Lampung |
| **Repositori GitHub** | [https://github.com/Mutia-afif/sipandu-smart-city](https://github.com/Mutia-afif/sipandu-smart-city) |
| **Live Deploy Vercel** | [https://sipandu-smart-city.vercel.app](https://sipandu-smart-city.vercel.app) |
| **Tahun Proyek** | 2026 |

---

## 1. Ringkasan Sistem & Latar Belakang

Laporan kerusakan infrastruktur perkotaan seperti **jalan berlubang**, **lampu penerangan jalan umum (PJU) padam**, dan **drainase tersumbat** sering kali dilaporkan melalui saluran non-resmi (media sosial, pesan singkat, atau surat manual) tanpa sistem pencatatan terpusat. Hal ini berakibat pada:
- **Warga** tidak dapat memantau status aduannya (apakah diterima, diproses, atau diabaikan).
- **Petugas Lapangan** tidak memiliki koordinat lokasi yang presisi dan kesulitan menentukan urutan prioritas penanganan.
- **Pemerintah Kota** tidak memiliki metrik evaluasi kinerja penanganan infrastruktur per dinas dan titik sebaran rawan kerusakan.

**SIPANDU Smart City** hadir sebagai prototipe sistem informasi terpusat berbasis lokasi (GIS) yang menghubungkan **Warga**, **Petugas Dinas Teknis**, dan **Admin Command Center Pemda** secara transparan, terukur, dan akuntabel.

---

## 2. Arsitektur Teknologi

```text
                  +----------------------------------------------+
                  |         Client Layer (Web Responsif)         |
                  |  - Askama (Server-Side Rendered HTML)        |
                  |  - HTMX (Interaktivitas Asinkron Dinamis)   |
                  |  - Leaflet.js + OpenStreetMap (Peta Spasial) |
                  |  - Tailwind CSS (Design Tokens Resmi)        |
                  +----------------------------------------------+
                                         |
                                (HTTP / Cookie Auth)
                                         v
                  +----------------------------------------------+
                  |       Application Layer (Rust + Axum)        |
                  |  - Tokio Multi-Threaded Async Runtime        |
                  |  - Tower-Governor (Rate Limiting)            |
                  |  - Argon2id Password Hashing Engine          |
                  |  - EXIF Metadata Sanitization (Privasi Foto) |
                  |  - Optimistic Concurrency Control (Version)  |
                  +----------------------------------------------+
                                         |
                                    (SQLx Pool)
                                         v
                  +----------------------------------------------+
                  |       Data Layer (PostgreSQL + PostGIS)      |
                  |  - geometry(Point, 4326) + Indeks GIST       |
                  |  - ST_DWithin (Cek Duplikat Radius 50m)      |
                  |  - ST_Distance (Urut Tugas Petugas by Jarak) |
                  |  - Sesi Server-Side & Audit Log Atomik       |
                  +----------------------------------------------+
```

---

## 3. Matriks Kepatuhan Syarat UTS & PRD

| Kode | Persyaratan PRD / UTS | Realisasi Implementasi |
|---|---|---|
| **FR-01** | Akun & Autentikasi Tanpa NIK | Registrasi murni hanya meminta Nama, Email (unik), No HP, dan Password. Password dienkripsi dengan Argon2id. |
| **FR-02** | Pengiriman Aduan & Lokasi GPS | Peta interaktif Leaflet mengambil lokasi GPS browser pengguna dengan opsi geser pin manual. Koordinat disimpan dalam PostGIS Point 4326. |
| **FR-02b** | Deteksi Duplikasi Spasial 50m | Saat warga memilih kategori dan titik lokasi, query PostGIS `ST_DWithin` mengecek laporan aktif dalam radius 50m dan memunculkan banner peringatan amber. |
| **FR-02c** | Privasi Foto (Strip EXIF) | Foto warga melalui modul `utils::exif::strip_exif_and_save` yang membersihkan metadata EXIF GPS sebelum disimpan ke disk. |
| **FR-03** | Pelacakan Status & Linimasa | Warga dapat melihat linimasa 4 tahap (*Diterima &rarr; Diverifikasi &rarr; Dalam Penanganan &rarr; Selesai*), alasan penolakan, serta foto sebelum & sesudah penanganan. |
| **FR-04** | Verifikasi & Disposisi Admin | Admin Command Center memverifikasi aduan, menetapkan tingkat prioritas (*Tinggi, Sedang, Rendah*), mendisposisikan ke dinas penanggung jawab, atau menolak dengan alasan wajib. |
| **FR-05** | Penanganan Lapangan Petugas | Petugas melihat antrean tugas dinasnya terurut otomatis berdasarkan **Prioritas** lalu **Jarak Terdekat (`ST_Distance`)**. Penutupan tiket wajib mengunggah foto bukti hasil kerja. |
| **FR-06** | Peta Sebaran & Dashboard GIS | Command Center menampilkan 4 kartu KPI utama dan peta Leaflet OpenStreetMap dengan pin berwarna status/prioritas. |
| **FR-07** | Master Data Dinas & Kategori | 3 Dinas (*PU, Perkim, Dishub*) dan 3 Kategori MVP (*Jalan Berlubang, PJU Padam, Drainase Tersumbat*). |
| **FR-08** | Audit Trail Log Atomik | Setiap perubahan status tiket, penetapan dinas, dan penolakan tercatat secara atomik di tabel `audit_log` (immutable). |
| **FR-09** | **Footer Wajib UTS** | Hadir di **SEMUA** halaman. Memuat Logo Pemda Bandar Lampung (kiri), teks copyright persis di tengah, dan Logo Universitas Teknokrat Indonesia (kanan). |

---

## 4. Teks Hak Cipta Resmi (FR-09)

Sesuai ketentuan tugas UTS PPSI, footer wajib memuat teks hak cipta berikut secara persis:

```text
Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom
```

---

## 5. Cara Menjalankan Aplikasi

### A. Prasyarat
- [Docker Desktop](https://www.docker.com/) (untuk menjalankan PostgreSQL + PostGIS).
- [Rust Toolchain](https://rustup.rs/) (versi 1.75+).

### B. Langkah Instalasi & Menjalankan

1. **Jalankan Database PostgreSQL + PostGIS via Docker:**
   ```powershell
   docker compose up -d
   ```

2. **Salin File Konfigurasi Lingkungan:**
   ```powershell
   Copy-Item .env.example .env
   ```

3. **Jalankan Aplikasi dengan Cargo:**
   ```powershell
   cargo run
   ```
   *Aplikasi akan otomatis menginisialisasi tabel dan migrasi PostGIS ke database.*

4. **Buka Aplikasi di Browser:**
   Akses `http://127.0.0.1:3000`

---

## 6. Akun Pengujian Prototipe (Default Seed)

| Peran | Alamat Email | Kata Sandi | Hak Akses |
|---|---|---|---|
| **Admin Pemda** | `admin@bandarlampung.go.id` | `rahasia123` | Akses penuh Command Center, verifikasi tiket, disposisi dinas, peta GIS kota, audit trail. |
| **Petugas Lapangan** | `petugas.pu@bandarlampung.go.id` | `rahasia123` | Akses Portal Petugas PU, ambil tiket tugas, urutan jarak terdekat, upload foto bukti selesai. |
| **Warga Pelapor** | `warga@gmail.com` | `rahasia123` | Akses Portal Warga, kirim aduan GPS, cek duplikasi 50m, pelacakan linimasa aduan saya. |

---

## 7. Menjalankan Uji Otomatis & Audit Keamanan

Untuk memverifikasi finite state machine status aduan, proteksi concurrency `version`, sanitasi EXIF, dan estimasi radius spasial 50m:
```powershell
# Uji Integrasi Kritis & Skema
python scripts/audit_and_test.py

# Uji Audit Keamanan OWASP Top 10 (Langkah 8 UTS)
python scripts/security_audit.py
```

---

## 8. Berkas Laporan Resmi UTS (.docx)

Sesuai instruksi dan standar akademik, dokumen laporan resmi UTS PPSI telah dibuat secara terpisah, rapi, dan siap dikumpulkan:
1. 📄 **Laporan Testing & Debugging (Dokumen Pengujian):**  
   [`LAPORAN_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`](file:///d:/PPSI%20(sir%20erliyan)/UTS%20PPSI%20-%20MUTIA%20AFIF%2024311124/LAPORAN_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx) *(Bab I - VI, Matriks 9 Test Cases, Hasil Investigasi Masalah, Log Pengujian)*
2. 📄 **Laporan Perbaikan Hasil Testing & Debugging (Dokumen Remediasi Terpisah):**  
   [`LAPORAN_PERBAIKAN_HASIL_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`](file:///d:/PPSI%20(sir%20erliyan)/UTS%20PPSI%20-%20MUTIA%20AFIF%2024311124/LAPORAN_PERBAIKAN_HASIL_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx) *(Laporan khusus tindak lanjut perbaikan: sanitasi input data-attribute JS, penanganan rollback race condition OCC, penambahan banner flash error, dan verifikasi ulang)*
3. 📄 **Laporan Formal Audit Keamanan (Dokumen Security OWASP Top 10):**  
   [`LAPORAN_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`](file:///d:/PPSI%20(sir%20erliyan)/UTS%20PPSI%20-%20MUTIA%20AFIF%2024311124/LAPORAN_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx) *(Evaluasi OWASP Top 10, Threat Modeling, Proteksi Data Pribadi Tanpa NIK, Argon2id, Strip Metadata EXIF, Lembar Pengesahan)*
4. 📄 **Laporan Perbaikan Hasil Audit Keamanan (Dokumen Security Remediation & Hardening):**  
   [`LAPORAN_PERBAIKAN_HASIL_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`](file:///d:/PPSI%20(sir%20erliyan)/UTS%20PPSI%20-%20MUTIA%20AFIF%2024311124/LAPORAN_PERBAIKAN_HASIL_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx) *(Tindak lanjut pengerasan sistem: Middleware Security Headers HTTP, Deep Magic Bytes MIME Inspection via infer::is_image, pembatasan buffer input, pengerasan SameSite=Lax cookie logout, dan verifikasi ulang 100% lulus)*
5. 📄 **Laporan Formal Deployment Vercel (Dokumen Cloud Implementation Langkah 10 UTS):**  
   [`LAPORAN_DEPLOYMENT_VERCEL_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`](file:///d:/PPSI%20(sir%20erliyan)/UTS%20PPSI%20-%20MUTIA%20AFIF%2024311124/LAPORAN_DEPLOYMENT_VERCEL_SIPANDU_UTS_MUTIA_AFIF_24311124.docx) *(Publikasi Cloud Vercel Global Edge Network, Konfigurasi vercel.json, Log Eksekusi CLI, Uji Aksesibilitas 100% Berhasil pada https://sipandu-smart-city.vercel.app, dan Lembar Pengesahan)*

---

## 9. Halaman Demonstrasi & Simulasi Interaktif UTS (`/simulasi`)

Untuk keperluan presentasi di hadapan Dosen Pengampu (Dr. Erliyan Redy Susanto, M.Kom), sistem menyediakan antarmuka demo 3 peran berdampingan:
- Akses URL: `http://127.0.0.1:3000/simulasi`
- **Skenario A:** Alur Ideal (Warga lapor &rarr; Admin verifikasi & tentukan Prioritas Tinggi &rarr; Petugas PU eksekusi di lokasi & upload bukti &rarr; Selesai).
- **Skenario B:** Aduan Ditolak (Laporan di jalan nasional kementerian &rarr; Admin menolak dengan alasan transparansi).

---

## 10. Status Deployment Cloud & Produksi (Langkah 10 UTS)

Proyek sistem informasi ini telah berhasil dideploy secara langsung ke platform **Vercel** pada akun resmi Mutia Afif Ramadhani:

- 🌐 **Live Production URL:** [https://sipandu-smart-city.vercel.app](https://sipandu-smart-city.vercel.app)
- 🔗 **Vercel Project Dashboard:** [https://vercel.com/mutia-afif-ramadhani-3545/sipandu-smart-city](https://vercel.com/mutia-afif-ramadhani-3545/sipandu-smart-city)
- ⚡ **Rute Akses Publik Vercel:**
  * **Beranda & Portal Hub:** `https://sipandu-smart-city.vercel.app/`
  * **Simulasi 3 Peran UTS:** `https://sipandu-smart-city.vercel.app/simulasi`
  * **Portal Warga:** `https://sipandu-smart-city.vercel.app/warga`
  * **Meja Kerja Petugas PU:** `https://sipandu-smart-city.vercel.app/petugas`
  * **Command Center Admin:** `https://sipandu-smart-city.vercel.app/admin`
  * **Autentikasi (Bebas NIK):** `https://sipandu-smart-city.vercel.app/login`

Untuk deployment server mandiri (On-Premise / VPS) dengan database PostGIS lokal, aplikasi juga dilengkapi container Docker multi-stage:
```powershell
# Menjalankan seluruh stack produksi (Rust App + PostGIS DB) dalam container:
docker compose -f docker-compose.prod.yml up -d --build
```

---

<p align="center">
  <b>Universitas Teknokrat Indonesia &bull; Kampus Sang Juara</b><br>
  <i>Proyek Pengembangan Sistem Informasi (UTS) &bull; Tahun Akademik 2026</i>
</p>

