# SIPANDU Smart City - Vibe Coding Rules & System Prompt
## Proyek UTS PPSI - Mutia Afif Ramadhani (24311124) | Dosen: Dr. Erliyan Redy Susanto, M.Kom

File ini adalah aturan baku (system instructions) untuk AI coding assistant (Cursor, Antigravity, Windsurf, Claude Code) saat mengembangkan proyek SIPANDU Smart City Kota Bandar Lampung.

---

### 1. Sumber Kebenaran & Hirarki Dokumen
1. **PRD (`prd.md`)**: Sumber kebenaran tertinggi untuk fitur, role, batasan, siklus status, dan data model.
2. **Design Skill (`SKILL.md`)**: Sumber kebenaran untuk design token Tailwind, pola komponen, dan resolusi UI vs PRD.
3. **HTML Stitch (jika ada)**: Hanya referensi visual. Jangan salin fitur fiktif yang tidak ada di PRD!

---

### 2. Aturan Kritis (Strict Guardrails - JANGAN DILANGGAR)
1. **DILARANG MENGGUNAKAN NIK**:
   - Jangan meminta input NIK, jangan tampilkan NIK, jangan simpan NIK di tabel mana pun.
   - Warga hanya mendaftar dengan Nama, Email (unik), No HP, dan Password.
2. **DILARANG MENGGUNAKAN KLAIM / FITUR FIKTIF**:
   - Jangan gunakan teks atau badge: "AI Validation", "AI Vision", "Integrasi CCTV", "Enkripsi SHA-256", "Live Feed" (kecuali jika ada data nyata/polling).
   - Deteksi duplikasi aduan murni menggunakan kueri spasial PostGIS radius 50 meter (`ST_DWithin`).
3. **FOOTER WAJIB UTS (FR-09)**:
   - Harus tampil di **SEMUA HALAMAN** tanpa terkecuali (Portal Warga, Petugas, Command Center, Login, Register, 404).
   - Teks Copyright **PERSIS**:
     `Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom`
   - Logo lokal (bukan CDN eksternal):
     - Kiri: `/static/img/logo_pemda.png` (alt: `Logo Pemda Kota Bandar Lampung`)
     - Kanan: `/static/img/logo_uti.png` (alt: `Logo Universitas Teknokrat Indonesia`)
   - Tampilan: Desktop 1 baris (Logo - Teks - Logo), HP bertumpuk rata tengah (kedua logo berdampingan di atas, teks di bawah).
4. **SIKLUS STATUS ADUAN (FINITE STATE MACHINE)**:
   - Hanya transisi ini yang valid:
     `Pending` -> `Verified` ATAU `Rejected` (alasan penolakan wajib) -> `In Progress` -> `Resolved` (foto bukti penanganan wajib).
   - Status ditampilkan ke warga sebagai: **Diterima**, **Diverifikasi**, **Dalam Penanganan**, **Selesai**.
   - Concurrency: Gunakan kunci optimis dengan kolom `version` pada tabel `aduan`.
5. **KATEGORI & PRIORITAS RESMI**:
   - 3 Kategori aktif MVP: `Jalan Berlubang`, `PJU Padam`, `Drainase Tersumbat`.
   - Tingkat prioritas: `Tinggi`, `Sedang`, `Rendah` (bukan P1/P2/P3 atau Darurat/Ringan). Prioritas ditentukan oleh Admin saat verifikasi.
6. **SPATIAL & EXIF**:
   - Koordinat disimpan dalam PostGIS `geometry(Point, 4326)`.
   - EXIF foto warga wajib dibersihkan sebelum disimpan.
   - Peta publik tidak boleh menampilkan data pribadi pelapor.

---

### 3. Arsitektur Teknis
- **Backend**: Rust (Axum + Tokio + SQLx + Tower)
- **Database**: PostgreSQL 15+ dengan ekstensi PostGIS
- **Auth**: Server-side session di tabel PostgreSQL + Cookie HTTPOnly/Secure/SameSite=Lax (Password Argon2id).
- **Frontend**: Server-Side Rendering (Askama) + HTMX + Tailwind CSS + Leaflet.js (OpenStreetMap).

---

### 4. Hasil Testing & Debugging (Hardened Standards)
1. **Pencegahan XSS / Broken String pada JS**:
   - Dilarang keras menyematkan teks dinamis pengguna langsung di dalam inline handler seperti `onclick="foo('{{ item.judul }}')"`.
   - Gunakan selalu `data-*` attributes (`data-id`, `data-no`, `data-judul`, `data-version`) pada elemen HTML, dan baca menggunakan `el.getAttribute()`.
2. **Umpan Balik Concurrency Control**:
   - Jika query UPDATE dengan `WHERE version = $current_version` menghasilkan `rows_affected == 0`, selalu rollback transaksi dan berikan redirect dengan parameter `?error=konflik_data`.
   - Tampilkan alert box informatif kepada pengguna bahwa data telah diubah oleh pihak lain.
3. **Validasi Berkas Foto di Lapisan Handler**:
   - Batasi ukuran berkas maksimal 5 MB per foto.
   - Periksa ekstensi/MIME valid (`.jpg`, `.jpeg`, `.png`, `.webp`).
   - Tolak file berlebih (> 3 foto) atau bertipe tidak sah secara eksplisit sebelum memanggil `strip_exif_and_save`.
4. **Kepatuhan Halaman Error (404 & 500)**:
   - Halaman error 404 (`.fallback(handlers::handle_404)`) dan 500 harus mewarisi `layouts/base.html` sehingga Footer Wajib UTS FR-09 tetap tampil utuh di situasi error apa pun.
