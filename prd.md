# PRD: SIPANDU Smart City

Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu

| Atribut | Keterangan |
| --- | --- |
| Mata kuliah | Proyek Pengembangan Sistem Informasi (UTS, Project Individu) |
| Penyusun | Mutia Afif Ramadhani, NPM 24311124, Kelas SI 23A |
| Versi / tanggal | 1.0 / 10 November 2026 |
| Jenis proyek | Prototipe UTS |
| Wilayah layanan | Kota Bandar Lampung (sesuai logo Pemda yang dipakai) |
| Platform | Web responsif (dapat di-install sebagai PWA) |
| Teknologi | Rust (Axum + Tokio), PostgreSQL + PostGIS |
| Deploy | Vercel (dibahas pada langkah 10 UTS, bukan di PRD ini) |

Prinsip dokumen: hal yang belum diketahui (pembagian dinas resmi, SLA, kriteria urgensi, aturan duplikat) tidak dikarang. Semuanya ditandai sebagai Pertanyaan Terbuka (bagian 10). Angka target adalah usulan, bukan ketentuan instansi.

## 1. Problem Statement

Masalah: laporan jalan berlubang, lampu penerangan jalan umum (PJU) padam, dan drainase tersumbat masih masuk lewat surat, telepon, atau media sosial tanpa pencatatan terpusat.

Siapa yang dirugikan:

- Warga: tidak tahu apakah aduannya diterima, diproses, atau diabaikan, sehingga melapor berulang.

- Dinas teknis dan petugas lapangan: tidak punya data lokasi yang akurat dan tidak bisa menentukan prioritas, sehingga penanganan lambat dan tidak terarah.

- Pemda: tidak ada data terpusat untuk mengukur kinerja per wilayah/dinas dan mengenali titik rawan kerusakan.

Kenapa penting: kerusakan jalan, PJU mati, dan drainase tersumbat berdampak langsung pada keselamatan dan banjir. Tanpa transparansi status, kepercayaan warga pada layanan publik menurun.

Warga membutuhkan cara melapor yang cepat dan bisa dipantau, sementara Pemda membutuhkan sistem terpusat berbasis lokasi untuk memverifikasi, meneruskan, dan menuntaskan aduan secara terukur dan terlacak.

## 2. Target User dan Persona

| Pengguna | Peran |
| --- | --- |
| Warga | Mengirim aduan, melacak status, melihat peta sebaran |
| Petugas Lapangan (Dinas teknis) | Menangani tiket, memperbarui status, mengunggah foto bukti |
| Admin Pemda | Verifikasi/tolak aduan, delegasi ke dinas, kelola master data dan akun, lihat dashboard dan laporan |

Persona di bawah bersifat ilustratif (bukan hasil riset) dan divalidasi saat pengujian pengguna.

Persona 1: Bu Sari, warga (ilustratif). Melihat lubang besar di jalan dekat rumah. Ingin melapor dari HP dalam hitungan detik dan tahu kapan diperbaiki. Frustrasi karena laporan sebelumnya lewat media sosial tidak pernah ada kabar.

Persona 2: Pak Dedi, petugas lapangan Dinas PU (ilustratif). Bekerja di lapangan dengan sinyal tidak stabil. Butuh daftar tugas berurutan prioritas dan terdekat, serta cara cepat melampirkan foto bukti. Frustrasi karena tugas datang lewat chat tanpa lokasi jelas.

Persona 3: Bu Rina, admin Pemda (ilustratif). Memantau semua aduan kota. Butuh menyaring spam, meneruskan ke dinas yang tepat, dan melihat tiket yang melewati batas waktu. Frustrasi karena rekap dikerjakan manual dan tidak ada riwayat siapa mengubah apa.

## 3. Goals dan Non-Goals

### Goals

- Warga dapat mengirim aduan dengan lokasi GPS dan foto dalam waktu singkat.

- Status aduan transparan dengan linimasa: Diterima → Diverifikasi → Dalam Penanganan → Selesai.

- Tiket diteruskan otomatis ke dinas berdasarkan kategori, dengan opsi koreksi oleh Admin.

- Petugas memiliki daftar tugas berprioritas dan dapat membuktikan hasil kerja dengan foto.

- Admin memiliki peta sebaran dan dashboard dasar untuk memantau kinerja.

- Semua perubahan status tercatat dan tidak dapat diubah (audit trail).

- Identitas aplikasi (logo Pemda, logo Universitas Teknokrat Indonesia, footer copyright) tampil sesuai ketentuan UTS.

### Non-Goals (MVP)

- Aplikasi mobile native.

- Notifikasi WhatsApp dan email (email di v2).

- Rating/masukan warga atas hasil pekerjaan (v2).

- Routing otomatis berdasarkan polygon wilayah administratif (nanti).

- Integrasi dengan LAPOR!/SP4N atau sistem pemerintah lain.

- Pembayaran, pengelolaan anggaran perbaikan, dan manajemen proyek konstruksi.

- Pemantauan sensor IoT (PJU pintar, sensor banjir).

## 4. User Stories

### Warga

- Sebagai warga, saya ingin membuat akun dan login, supaya aduan saya tercatat atas nama saya.

- Sebagai warga, saya ingin mengirim aduan dengan lokasi GPS, foto, dan deskripsi, supaya petugas tahu persis letak masalahnya.

- Sebagai warga, saya ingin memilih kategori aduan (jalan berlubang, PJU padam, drainase), supaya aduan diteruskan ke dinas yang tepat.

- Sebagai warga, saya ingin melihat status dan linimasa aduan saya, supaya saya tidak perlu bertanya ke instansi.

- Sebagai warga, saya ingin melihat peta sebaran aduan umum, supaya saya tahu apakah masalah yang sama sudah dilaporkan.

- Sebagai warga, saya ingin melihat alasan jika aduan saya ditolak, supaya saya bisa memperbaiki laporan.

- Sebagai warga, saya ingin melihat foto hasil perbaikan, supaya saya yakin aduan sudah ditangani.

### Petugas Lapangan

- Sebagai petugas, saya ingin daftar tugas berurut prioritas dan jarak, supaya saya bekerja efisien.

- Sebagai petugas, saya ingin mengubah status tiket menjadi Dalam Penanganan dan Selesai, supaya progres terlihat.

- Sebagai petugas, saya ingin mengunggah foto setelah perbaikan dan catatan teknis, supaya hasil kerja terbukti.

### Admin Pemda

- Sebagai admin, saya ingin memverifikasi atau menolak aduan dengan alasan, supaya spam tidak masuk ke dinas.

- Sebagai admin, saya ingin mengubah dinas tujuan dan prioritas tiket, supaya penanganan tepat sasaran.

- Sebagai admin, saya ingin melihat dashboard dan peta kepadatan aduan, supaya titik rawan terlihat.

- Sebagai admin, saya ingin mengelola kategori dan akun petugas, supaya sistem sesuai struktur dinas.

- Sebagai admin, saya ingin melihat audit log dan mengekspor laporan berkala, supaya kinerja dapat dipertanggungjawabkan.

## 5. Daftar Fitur

| Tingkat | Fitur |
| --- | --- |
| MVP | Registrasi/login; kirim aduan (GPS, foto, deskripsi, kategori); tracker status 4 tahap; verifikasi/tolak oleh Admin; routing tiket ke dinas berdasarkan kategori (dapat dikoreksi Admin); prioritas tiket (diatur Admin); daftar tugas petugas (prioritas + jarak); foto bukti penanganan; peta sebaran aduan; dashboard dasar; audit log; manajemen kategori, dinas, dan akun internal; branding wajib (logo + footer) |
| v2 | Heatmap lanjutan; laporan SLA dan ekspor berkala; rating/masukan warga; notifikasi email; buka kembali (reopen) aduan; deteksi duplikat otomatis yang lebih canggih |
| Nanti | Notifikasi WhatsApp; aplikasi native; integrasi LAPOR!/SP4N; routing berdasarkan polygon kecamatan/kelurahan; kategori tambahan (sampah, pohon tumbang, dll.); antrean offline (PWA sync) |

## 6. Functional Requirements (MVP)

### 6.1 Role dan permission

| Aksi | Warga | Petugas | Admin |
| --- | --- | --- | --- |
| Registrasi, login, kelola profil sendiri | ✔ | ✔ | ✔ |
| Kirim aduan | ✔ | – | – |
| Lihat aduan milik sendiri + linimasa | ✔ | – | – |
| Lihat peta sebaran umum (tanpa identitas pelapor) | ✔ | ✔ | ✔ |
| Lihat tiket dinas sendiri | – | ✔ | ✔ |
| Ubah status Dalam Penanganan / Selesai (tiket dinasnya) | – | ✔ | ✔ |
| Verifikasi atau tolak aduan | – | – | ✔ |
| Ubah dinas tujuan dan prioritas | – | – | ✔ |
| Dashboard dan laporan | – | – | ✔ |
| Kelola kategori, dinas, akun internal | – | – | ✔ |
| Lihat audit log | – | – | ✔ |

### 6.2 Status aduan

Pending → Verified atau Rejected (alasan wajib) → In Progress → Resolved (foto bukti wajib).

- Pending, Verified, In Progress, Resolved ditampilkan ke warga sebagai Diterima, Diverifikasi, Dalam Penanganan, Selesai.

- Hanya transisi di atas yang diizinkan; transisi lain ditolak oleh sistem.

- Rejected dan Resolved bersifat akhir pada MVP. Membuka kembali aduan masuk v2 (lihat Pertanyaan Terbuka #10).

### FR-01 Akun dan autentikasi

- Registrasi warga dengan nama, email, nomor HP, password. NIK tidak diwajibkan. Email unik.

- Password minimal 8 karakter, disimpan dengan Argon2id.

- Login diarahkan ke halaman sesuai role. Akun petugas dan admin dibuat oleh Admin.

- Rate limit pada login dan pengiriman aduan. Akun nonaktif tidak dapat login.

### FR-02 Kirim aduan

- Input: kategori (wajib), judul, deskripsi, lokasi, foto (minimal 1).

- Lokasi diambil dari GPS perangkat dan dapat digeser di peta oleh warga sebelum dikirim. Jika GPS ditolak, warga menandai lokasi manual di peta.

- Koordinat harus valid dan berada di dalam wilayah layanan (batas: Pertanyaan Terbuka #4).

- Foto: format JPG/PNG/WebP, usulan maks. 5 MB per foto dan maks. 3 foto (Pertanyaan Terbuka #6). Tipe divalidasi dari isi file, bukan hanya ekstensi. Metadata EXIF dibuang sebelum disimpan.

- Setelah terkirim: nomor aduan unik dan status Pending.

- Sistem memperingatkan jika ada aduan aktif berkategori sama dalam radius tertentu (usulan 50 m; Pertanyaan Terbuka #5); warga boleh tetap mengirim.

### FR-03 Pelacakan status

- Warga melihat daftar aduan miliknya dan linimasa tiap aduan (status, waktu, catatan petugas, foto penanganan).

- Alasan penolakan ditampilkan jika Rejected.

### FR-04 Verifikasi dan routing (Admin)

- Antrean aduan Pending dengan filter kategori, tanggal, dan wilayah.

- Admin memilih Verified (alasan opsional) atau Rejected (alasan wajib).

- Saat Verified, dinas tujuan terisi otomatis dari dinas penanggung jawab kategori; Admin dapat mengubahnya dan menetapkan prioritas Rendah/Sedang/Tinggi (kriteria: Pertanyaan Terbuka #2).

### FR-05 Penanganan (Petugas)

- Daftar tugas tiket dinasnya, diurutkan prioritas lalu jarak ke posisi petugas (jika izin lokasi diberikan; jika tidak, diurutkan prioritas lalu waktu).

- Petugas mengambil tiket (In Progress) dan menutupnya (Resolved) dengan foto bukti dan catatan teknis. Resolved tanpa foto bukti ditolak.

### FR-06 Peta dan dashboard

- Peta interaktif (Leaflet + OpenStreetMap) menampilkan aduan sesuai filter status/kategori. Peta publik tidak menampilkan identitas pelapor.

- Dashboard Admin: jumlah aduan per status, per kategori, per dinas; tiket tertunda terlama; peta kepadatan aduan.

### FR-07 Manajemen master data

- Admin mengelola kategori (nama, dinas penanggung jawab, aktif/nonaktif), data dinas, dan akun internal.

- Kategori dengan tiket aktif tidak dapat dihapus, hanya dinonaktifkan.

### FR-08 Audit log

- Setiap perubahan status, penetapan dinas/prioritas, dan perubahan master data/akun tercatat: pelaku, role, aksi, objek, nilai sebelum/sesudah, catatan, waktu, IP.

- Pencatatan terjadi dalam transaksi yang sama dengan perubahannya. Hanya Admin yang dapat melihat; log tidak dapat diubah atau dihapus lewat aplikasi.

### FR-09 Footer wajib (syarat UTS)

Kedua logo dan teks copyright diletakkan bersama di footer aplikasi, pada semua halaman termasuk login dan registrasi.

- Isi footer: logo Pemda (Kota Bandar Lampung), logo Universitas Teknokrat Indonesia, dan teks tepat berikut: Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom

- Tata letak desktop: satu baris dengan garis pemisah di atasnya; logo Pemda di kiri, teks copyright di tengah (rata tengah), logo Universitas Teknokrat Indonesia di kanan.

- Tata letak HP (layar sempit): bertumpuk dan rata tengah; kedua logo berdampingan di atas, teks copyright di bawahnya.

- Ukuran logo: tinggi seragam (usulan 40 px), rasio aspek terjaga, jarak sama, dengan teks alternatif (“Logo Pemda Kota Bandar Lampung” dan “Logo Universitas Teknokrat Indonesia”).

- Posisi: footer berada di bagian paling bawah halaman (menempel di dasar layar jika konten pendek, mengikuti akhir konten jika panjang).

- Acceptance criteria: footer lengkap (dua logo + teks) terlihat rapi di tampilan HP dan desktop; tidak dapat dihilangkan oleh pengguna biasa; diuji pada setiap halaman utama. Aturan penggunaan lambang daerah: Pertanyaan Terbuka #9.

## 7. Sketsa Data Model

| Entitas | Field kunci |
| --- | --- |
| users | id (UUID PK), nama, email (unik), no_hp, password_hash (Argon2id), role (warga/petugas/admin), dinas_id (FK, hanya petugas), is_active, created_at |
| dinas | id, nama, is_active |
| categories | id, nama_kategori, dinas_id (FK dinas penanggung jawab), is_active |
| aduan | id (UUID PK), no_aduan (unik), user_id (FK), category_id (FK), dinas_id (FK, terisi saat Verified), judul, deskripsi, geom (geometry Point, SRID 4326), alamat_teks (opsional), status (enum), prioritas (enum), version (untuk kunci optimis), created_at, updated_at |
| aduan_foto | id, aduan_id (FK), jenis (laporan/penanganan), storage_key, ukuran, mime, diunggah_oleh, created_at |
| aduan_logs | id, aduan_id (FK), changed_by_user_id (FK), status_lama, status_baru, catatan, created_at |
| audit_log | id, user_id, role, aksi, entitas, entitas_id, nilai_lama (jsonb), nilai_baru (jsonb), ip, waktu |
| sessions | id, user_id, expires_at, created_at (sesi server-side) |

```text
users 1──N aduan N──1 categories N──1 dinas 1──N users(petugas)
aduan 1──N aduan_foto
aduan 1──N aduan_logs
users 1──N audit_log
```

Indeks yang dibutuhkan: GIST pada aduan.geom; indeks pada aduan(status, created_at), aduan(dinas_id, status), aduan(user_id), dan aduan_logs(aduan_id, created_at).

## 8. Edge Case dan Failure State

| Situasi | Perilaku yang diharapkan |
| --- | --- |
| Izin GPS ditolak / akurasi rendah | Warga menandai lokasi manual di peta; peringatan jika akurasi rendah |
| Koordinat di luar wilayah layanan | Pengiriman ditolak dengan pesan jelas |
| Foto >batas ukuran, tipe salah, rusak, atau mencurigakan | Ditolak dengan pesan spesifik; file tidak disimpan |
| Foto membawa EXIF lokasi pelapor | EXIF dibuang sebelum disimpan |
| Koneksi putus saat mengirim | Data formulir tidak hilang; warga dapat mengirim ulang; tidak terbentuk aduan setengah jadi |
| Aduan serupa sudah ada di sekitar | Peringatan duplikat; warga boleh tetap mengirim |
| Kiriman beruntun (spam/bot) | Dibatasi rate limit; admin dapat menolak dengan alasan |
| Transisi status tidak valid (mis. Pending langsung Resolved) | Ditolak oleh sistem |
| Resolved tanpa foto bukti | Ditolak |
| Dua pengguna mengubah tiket yang sama bersamaan | Penyimpan kedua mendapat peringatan konflik (kunci optimis); tidak menimpa diam-diam |
| Kategori dinonaktifkan saat tiket aktif | Tiket aktif tetap berjalan; kategori tidak muncul untuk aduan baru |
| Petugas dinonaktifkan saat memegang tiket | Tiket kembali ke antrean dinas; Admin diberi tahu |
| Dinas tujuan kosong (kategori belum dipetakan) | Tiket tetap Verified, ditandai “perlu delegasi” ke Admin |
| Warga menghapus akun | Data pribadi dianonimkan; aduan dan log tetap ada |
| Penyimpanan foto penuh/tidak tersedia | Pengiriman ditolak dengan pesan umum; kejadian dicatat |
| Database tidak tersedia | Pesan error umum, tanpa detail teknis |
| Dashboard/peta tanpa data | Menampilkan keadaan kosong, bukan error |

## 9. Success Metrics

Semua angka adalah usulan untuk prototipe UTS, bukan ketentuan instansi.

### Kriteria uji prototipe

- Alur end-to-end (kirim aduan → verifikasi → penanganan → selesai) berjalan tanpa error pada data uji 1.000 aduan.

- Kueri radius terdekat dan peta sebaran pada 1.000 aduan ≤ 500 ms.

- Halaman utama dan daftar aduan termuat ≤ 3 detik dengan 50 pengguna bersamaan.

- Warga dapat menyelesaikan pengiriman aduan ≤ 60 detik pada uji dengan 3–5 pengguna.

- 100% perubahan status dan perubahan master data tercatat di audit log.

- 100% test otorisasi kritis lulus (warga hanya melihat aduannya, petugas hanya tiket dinasnya, hanya Admin dapat verifikasi/kelola akun).

- Footer (dua logo + teks copyright) tampil rapi di 100% halaman utama.

### Produk (jika kelak dipakai instansi)

| Metrik | Target usulan |
| --- | --- |
| Waktu verifikasi aduan sejak masuk | Diukur (target SLA ditetapkan Pemda) |
| Persentase aduan selesai dalam SLA | Diukur setelah SLA ditetapkan |
| Persentase aduan ditolak karena spam | Dipantau |
| Warga yang melacak status tanpa menghubungi instansi | ≥ 90% |

## 10. Pertanyaan Terbuka

Prioritas: [B] Blocker · [P] Penting · [T] Bisa ditunda.

- [B] Dinas mana yang bertanggung jawab atas tiap kategori (jalan, PJU, drainase) di Kota Bandar Lampung? Brainstorming menyebut Dinas PU, Perkim, dan Satpol PP, tetapi pembagian resminya belum diketahui. Untuk prototipe dipakai data contoh berlabel asumsi.

- [P] Kriteria tingkat urgensi dan SLA per kategori (target waktu verifikasi dan penanganan)?

- [P] Apakah kategori selain tiga yang ada perlu masuk MVP (mis. sampah, pohon tumbang)?

- [P] Batas wilayah layanan: data batas Kota Bandar Lampung yang dipakai untuk validasi koordinat?

- [P] Aturan aduan duplikat: radius, rentang waktu, dan perlakuan (hanya peringatan atau digabung)?

- [P] Batas foto: format, ukuran, dan jumlah per aduan?

- [P] Siapa yang berwenang menutup tiket: petugas langsung (default), atau perlu konfirmasi Admin/warga?

- [P] Apakah semua aduan tampil di peta publik, dan apakah aduan yang ditolak disembunyikan? Informasi apa yang boleh terlihat publik?

- [P] Ketentuan penggunaan lambang Pemda pada aplikasi, bahkan untuk prototipe akademik?

- [P] Bolehkah aduan yang sudah Resolved dibuka kembali, dan oleh siapa?

- [T] Kebijakan retensi data aduan dan foto.

- [T] Notifikasi: apakah in-app cukup pada MVP, dan email (butuh layanan SMTP) di v2?

- [P] Penyedia PostgreSQL dengan PostGIS dan object storage untuk foto saat deploy (dibahas pada langkah 10 UTS).

- [T] Apakah dosen menetapkan format atau rubrik khusus untuk PRD?

- [T] Apakah perlu integrasi dengan LAPOR!/SP4N pada tahap berikutnya?

## 11. Validasi Teknologi: Rust dan PostgreSQL

Kesimpulan: layak. Seluruh kebutuhan MVP dapat dipenuhi dengan Rust dan PostgreSQL + PostGIS, dengan tiga penyesuaian terhadap brainstorming awal (Lampiran A).

### 11.1 Pemetaan kebutuhan ke teknologi

| Kebutuhan | Solusi | Status |
| --- | --- | --- |
| API asinkron dan validasi payload | Axum + Tokio; serde dan crate validator | Cocok |
| Query aman dari SQL injection | SQLx (query berparameter, async, PostgreSQL native) | Cocok |
| Migrasi skema | sqlx migrate | Cocok |
| Penyimpanan koordinat | PostGIS geometry(Point, 4326) + indeks GIST | Cocok, ekstensi harus aktif di hosting DB |
| Cari aduan radius terdekat dan deteksi duplikat | ST_DWithin pada tipe geography (satuan meter) | Cocok |
| Urut tugas petugas berdasarkan jarak | ST_Distance terhadap posisi petugas | Cocok |
| Heatmap | Agregasi grid (ST_SnapToGrid + COUNT) keluaran GeoJSON, ditampilkan Leaflet | Cocok |
| Hash password | crate argon2 (Argon2id) | Cocok |
| Autentikasi | Sesi server-side di PostgreSQL + cookie HttpOnly/Secure/SameSite | Cocok, mengganti JWT (lihat Lampiran A) |
| Rate limit | Middleware tower (mis. tower_governor) | Cocok |
| Upload foto | Axum multipart; cek tipe dari isi file (mis. crate infer); batas ukuran; buang EXIF dengan encode ulang gambar | Cocok, butuh object storage |
| Status ENUM dan transisi valid | ENUM PostgreSQL + enum Rust; transisi divalidasi di lapisan layanan | Cocok |
| Audit trail atomik | Transaksi SQLx: ubah status dan tulis log sekaligus | Cocok |
| Konflik edit bersamaan | Kunci optimis (UPDATE ... WHERE version = $n) | Cocok |
| Antarmuka | Template server-side (Askama atau Maud), HTMX, Leaflet + OpenStreetMap | Cocok |
| Pengujian | cargo test, sqlx::test untuk uji integrasi dengan database uji | Cocok |
| Skala uji (1.000 aduan, 50 pengguna bersamaan) | Jauh di bawah kapasitas Axum + PostgreSQL; titik rawan hanya kueri tanpa indeks | Cocok |

### 11.2 Risiko teknis

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Kurva belajar Rust (ownership, tipe ketat) saat vibe coding | Proses lebih lambat, error kompilasi sering | Pecah per modul kecil; tentukan struktur proyek dan crate sejak awal; gunakan SQLx dan Axum yang umum dipakai |
| Waktu kompilasi Rust | Siklus uji lambat | Pakai cargo check untuk iterasi; build release hanya saat deploy |
| Ekstensi PostGIS tidak tersedia di penyedia database | Fitur spasial tidak jalan | Pastikan penyedia mendukung PostGIS sebelum dipilih (Pertanyaan Terbuka #13) |
| Foto tidak dapat disimpan di filesystem server | Upload foto gagal | Object storage terpisah sejak awal |
| Deploy Rust di Vercel | Runtime Rust Vercel berstatus Beta; DB dan storage harus di luar Vercel | Dikaji penuh pada langkah 10 UTS; siapkan alternatif bila terkendala |

## 12. Non-Functional Requirements

- Keamanan: otorisasi berbasis role di setiap endpoint; query berparameter; Argon2id; perlindungan CSRF; cookie sesi HttpOnly/Secure/SameSite; validasi dan sanitasi input; rate limit; file upload divalidasi dan tidak dapat dieksekusi; audit security formal pada langkah 8 UTS.

- Privasi: NIK tidak dikumpulkan; peta publik tanpa identitas pelapor; EXIF foto dibuang; hak akses data pribadi dibatasi sesuai role.

- Kinerja: target pada bagian 9.

- Keandalan: data tidak hilang saat restart; log audit durable.

- Kegunaan: responsif untuk HP; bahasa Indonesia; pesan error spesifik.

- Keterlacakan: semua aksi kritis tercatat.

## 13. Definition of Done (PRD dan Prototipe)

- Seluruh requirement MVP (FR-01 sampai FR-09) berjalan pada data uji.

- Tiga peran (Warga, Petugas, Admin) dapat menjalankan alur penuh aduan.

- Test otorisasi dan kriteria uji pada bagian 9 terpenuhi.

- Footer berisi logo Pemda, logo Universitas Teknokrat Indonesia, dan teks copyright tampil rapi di semua halaman utama (desktop dan HP).

- Stack Rust + PostgreSQL/PostGIS terbukti menjalankan seluruh fitur MVP.

- Pertanyaan terbuka berprioritas Blocker terdokumentasi dan menggunakan asumsi berlabel.

# Lampiran A: Perbedaan dari Brainstorming dan Alasannya

| No | Brainstorming awal | Di PRD | Alasan |
| --- | --- | --- | --- |
| 1 | Tabel aduan menyimpan latitude, longitude, dan geom | Hanya geom (koordinat diturunkan darinya) | Menghindari data ganda yang bisa tidak sinkron |
| 2 | Otentikasi JWT | Sesi server-side di PostgreSQL + cookie aman | Aplikasi web render server tidak butuh JWT; sesi mudah dicabut. JWT dipakai bila kelak ada aplikasi native |
| 3 | users.nik | Dihapus dari MVP | NIK adalah data pribadi sensitif dan tidak diperlukan untuk mengirim aduan |
| 4 | Foto hanya foto_url di aduan | Tabel aduan_foto | Satu aduan dapat memiliki beberapa foto laporan dan foto penanganan |
| 5 | Status Pending/Verified/In Progress/Resolved | Ditambah Rejected | Penolakan spam perlu status akhir yang jelas |
| 6 | Routing otomatis berdasarkan kategori dan zona wilayah | Kategori saja (zona = nanti) | Butuh data batas wilayah (polygon) yang belum tersedia |
| 7 | “Web dan mobile” | Web responsif/PWA | Realistis untuk proyek individu dan stack Rust |
| 8 | Rating/masukan warga | v2 | Menjaga MVP tetap terjangkau |
| 9 | Tidak ada entitas dinas | Ditambah dinas | Diperlukan untuk routing dan hak akses petugas |
| 10 | Tidak ada kunci edit bersamaan dan audit umum | version di aduan dan audit_log | Mencegah konflik dan melacak perubahan master data |

Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom
