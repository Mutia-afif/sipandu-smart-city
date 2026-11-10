# 🎓 PANDUAN DEMONSTRASI & UJIAN TENGAH SEMESTER (UTS) PPSI
## Proyek: SIPANDU Smart City Kota Bandar Lampung
**Mahasiswa:** Mutia Afif Ramadhani (NPM: 24311124)  
**Kelas:** SI 23A — S1 Sistem Informasi  
**Dosen Pengampu:** Dr. Erliyan Redy Susanto, M.Kom  
**Mata Kuliah:** Proyek Pengembangan Sistem Informasi (PPSI)  
**Tautan Live Vercel:** [https://sipandu-smart-city.vercel.app](https://sipandu-smart-city.vercel.app)  

---

## 1. Ringkasan Eksekutif Sistem (Elevator Pitch)
> *"Selamat pagi/siang Bapak Dr. Erliyan Redy Susanto, M.Kom. Pada kesempatan UTS PPSI ini, saya mempresentasikan **SIPANDU Smart City**, yaitu Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu untuk Pemerintah Kota Bandar Lampung yang dikembangkan bekerja sama secara akademik dengan Universitas Teknokrat Indonesia.*  
>  
> *Sistem ini dibangun dengan arsitektur berperforma tinggi menggunakan **Rust (Axum + Tokio)** dan basis data spasial **PostgreSQL 16 + PostGIS**. SIPANDU menyelesaikan masalah laten pelaporan infrastruktur kota: penanganan lambat, ketiadaan transparansi status tiket, dan risiko duplikasi laporan tanpa menggunakan fitur fiktif maupun pengumpulan NIK yang melanggar UU PDP."*

---

## 2. Alur Demonstrasi Praktis (Demo Script)

Saat diminta mendemonstrasikan sistem di hadapan dosen, buka langsung URL:  
👉 **`https://sipandu-smart-city.vercel.app/simulasi`**

### Skenario A: Alur Ideal Penanganan Aduan (Tuntas Disposisi)
1. **Langkah 1 (Sisi Warga):**
   - Tunjukkan kartu warga di panel kiri.
   - Jelaskan bahwa warga membuat laporan *"Jalan Berlubang di Depan Teknokrat"*.
   - Tekan tombol **"Skenario A: Alur Ideal"**.
   - Tunjukkan linimasa status warga berubah bertahap dari **Diterima (Pending)** &rarr; **Diverifikasi** &rarr; **Dalam Penanganan** &rarr; **Selesai**.
2. **Langkah 2 (Sisi Command Center Admin):**
   - Tunjukkan panel tengah (Admin Dispatcher).
   - Jelaskan bahwa Admin memverifikasi kebenaran laporan, menetapkan **Prioritas TINGGI**, dan mendisposisikannya ke **Dinas Pekerjaan Umum**.
   - Tunjukkan stempel audit log mencatat aksi `VERIFIKASI_ADUAN`.
3. **Langkah 3 (Sisi Petugas Lapangan Dinas PU):**
   - Tunjukkan panel kanan (Meja Kerja Petugas).
   - Jelaskan bahwa petugas menerima tugas terurut berdasarkan jarak terdekat (*ST_Distance* spasial).
   - Petugas mengambil tugas (*In Progress*) dan menutupnya dengan **wajib melampirkan foto bukti penanganan selesai**.
   - Di sisi warga, muncul callout hijau konfirmasi pekerjaan selesai beserta kutipan catatan teknis penambalan aspal.

### Skenario B: Aduan Ditolak (Bukan Kewenangan Pemkot)
1. Tekan tombol **"Skenario B: Ditolak"**.
2. Jelaskan kasus nyata: warga melaporkan kerusakan di jalan lintas nasional (kewenangan Kementerian PUPR, bukan Pemkot Bandar Lampung).
3. Admin menolak tiket dengan **alasan resmi wajib diisi** demi asas transparansi publik.
4. Di sisi warga, tiket masuk status akhir **Ditolak (Rejected)** dengan kotak merah alasan penolakan yang jelas.

---

## 3. Fitur Unggulan Spasial & Guardrails PRD (Poin Nilai Tambah)

1. **Deteksi Duplikasi Spasial 50 Meter Real-Time (PostGIS `ST_DWithin`):**
   - Buka `/warga`.
   - Geser pin penanda peta Leaflet ke dekat gerbang Teknokrat (`-5.3812, 105.2571`).
   - Tunjukkan munculnya **banner amber**: *"Peringatan Spasial PostGIS ST_DWithin (Radius 50m): Terdeteksi aduan aktif berjarak ~32 meter di lokasi ini"*.
   - Jelaskan ke dosen: *"Sistem tidak menggunakan AI fiktif, melainkan murni kalkulasi geospasial bola bumi PostGIS pada tipe data geography."*

2. **Kepatuhan Privasi Data Pribadi Bebas NIK (UU No. 27/2022 UU PDP):**
   - Buka `/register`.
   - Tunjukkan formulir pendaftaran: hanya meminta Nama Lengkap, Email, No HP, dan Kata Sandi.
   - Jelaskan: *"Sesuai PRD Section 6 FR-01 dan UU PDP, pengumpulan NIK dilarang untuk meminimalisasi risiko kebocoran identitas kependudukan warga."*

3. **Pembersihan Metadata EXIF GPS:**
   - Jelaskan: *"Foto yang diunggah warga sering memuat metadata GPS lokasi rumah pelapor. Modul `strip_exif_and_save` pada backend Rust melakukan decode biner dan re-encoding murni sehingga privasi pelapor terlindungi."*

4. **Optimistic Concurrency Control (OCC):**
   - Jelaskan: *"Tabel aduan memiliki kolom `version INT`. Jika dua petugas/admin memperbarui tiket bersamaan, pembaruan kedua otomatis terdeteksi konflik dan di-rollback secara atomik tanpa menimpa data diam-diam."*

5. **Footer Resmi UTS (FR-09):**
   - Tunjukkan footer di bagian bawah layar:
     * Kiri: Logo Pemkot Bandar Lampung (`logo_pemda.png`).
     * Tengah: Teks persis: `Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom`.
     * Kanan: Logo Universitas Teknokrat Indonesia (`logo_uti.png`).
   - Tunjukkan bahwa tata letak responsif: 1 baris di desktop, dan bertumpuk rapi di tampilan mobile (<768px).

---

## 4. Antisipasi Pertanyaan Dosen Pengampu & Kunci Jawaban

| Kemungkinan Pertanyaan Dosen | Kunci Jawaban Teknis & Arsitektural |
|:---|:---|
| **"Mengapa memilih stack Rust Axum dibanding framework populer seperti Express.js atau Laravel?"** | *"Rust memberikan jaminan keamanan memori (memory safety) tanpa garbage collector, konsumsi RAM yang sangat efisien (<30 MB), serta performa konkurensi asinkron berbasis Tokio. Framework Axum didukung penuh oleh tim pengembang Tokio dengan arsitektur modular Tower middleware."* |
| **"Bagaimana sistem memastikan query SQL aman dari serangan SQL Injection?"** | *"Seluruh akses database menggunakan SQLx dengan parameterized queries ($1, $2, ...). SQLx melakukan verifikasi tipe saat compile-time dan menolak konkatenasi string SQL mentah secara fundamental."* |
| **"Mengapa menggunakan Server-side Sessions di PostgreSQL daripada JWT?"** | *"Sesuai kajian PRD, aplikasi web yang me-render halaman secara server-side (SSR) tidak membutuhkan kompleksitas JWT. Sesi server-side memudahkan pencabutan (revocation) instan saat logout, dan token disimpan dalam cookie dengan atribut HttpOnly dan SameSite=Lax untuk menangkal XSS dan CSRF."* |
| **"Bagaimana cara sistem menangani race condition saat dua admin mengedit tiket yang sama?"** | *"Menggunakan Optimistic Concurrency Control dengan klausa `WHERE id = $1 AND version = $2`. Saat pembaruan terjadi, versi dinaikkan (`version = version + 1`). Jika versi di database sudah berubah, `rows_affected` bernilai 0, sistem mengeksekusi `tx.rollback().await`, dan menampilkan flash banner konflik ke pengguna."* |
| **"Bagaimana pengujian sistem ini dilakukan?"** | *"Sistem telah diuji melalui automated test suite `scripts/audit_and_test.py` (9/9 Kasus Uji Lulus / 100%) dan automated security audit `scripts/security_audit.py` (10/10 OWASP Top 10 Compliant). Dokumentasinya tersusun lengkap dalam 4 berkas laporan resmi `.docx`."* |

---

## 5. Berkas Laporan Resmi UTS yang Siap Diserahkan

1. 📄 **`LAPORAN_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`** (43 KB)
2. 📄 **`LAPORAN_PERBAIKAN_HASIL_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`** (44 KB)
3. 📄 **`LAPORAN_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`** (43 KB)
4. 📄 **`LAPORAN_PERBAIKAN_HASIL_AUDIT_SECURITY_SIPANDU_UTS_MUTIA_AFIF_24311124.docx`** (42 KB)

---
*Semoga sukses dalam ujian dan demonstrasi UTS PPSI! Universitas Teknokrat Indonesia — Kampus Sang Juara.*

