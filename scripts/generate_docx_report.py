import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set Margins (Normal: 1 inch = 72 pt)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.2)
        section.right_margin = Inches(1.2)

    # Color definitions
    COLOR_PRIMARY = RGBColor(0, 32, 70)       # Navy #002046
    COLOR_SECONDARY = RGBColor(0, 107, 95)    # Teal #006b5f
    COLOR_MUTED = RGBColor(100, 116, 139)     # Slate #64748b
    COLOR_DARK = RGBColor(15, 23, 42)         # #0f172a
    COLOR_SUCCESS = RGBColor(22, 101, 52)     # Green #166534

    # =========================================================================
    # 1. HALAMAN JUDUL (COVER)
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSITAS TEKNOKRAT INDONESIA\nFAKULTAS TEKNIK DAN ILMU KOMPUTER\nPROGRAM STUDI S1 SISTEM INFORMASI\nTAHUN AKADEMIK 2026")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph("\n")

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LAPORAN TESTING DAN DEBUGGING SISTEM INFORMASI\nSIPANDU SMART CITY")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu\n(Kota Bandar Lampung)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph("\n")

    p_mid = doc.add_paragraph()
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mid = p_mid.add_run("Disusun untuk Memenuhi Tugas Ujian Tengah Semester (UTS)\nMata Kuliah: Proyek Pengembangan Sistem Informasi (PPSI)")
    r_mid.font.name = "Arial"
    r_mid.font.size = Pt(11)
    r_mid.font.italic = True
    r_mid.font.color.rgb = COLOR_MUTED

    doc.add_paragraph("\n\n")

    # Tabel Identitas Penyusun
    t_id = doc.add_table(rows=5, cols=3)
    t_id.alignment = WD_TABLE_ALIGNMENT.CENTER
    data_id = [
        ("Nama Mahasiswa", ":", "Mutia Afif Ramadhani"),
        ("NPM", ":", "24311124"),
        ("Kelas", ":", "SI 23A"),
        ("Dosen Pengampu", ":", "Dr. Erliyan Redy Susanto, M.Kom"),
        ("Tanggal Pengujian", ":", "10 November 2026")
    ]
    for row_idx, (k, sep, v) in enumerate(data_id):
        r = t_id.rows[row_idx]
        r.cells[0].paragraphs[0].add_run(k).bold = True
        r.cells[1].paragraphs[0].add_run(sep)
        r.cells[2].paragraphs[0].add_run(v).bold = (row_idx in [0, 1, 3])
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(11)
                    run.font.color.rgb = COLOR_DARK

    doc.add_page_break()

    # =========================================================================
    # BAB I: PENDAHULUAN
    # =========================================================================
    h1 = doc.add_paragraph()
    r = h1.add_run("BAB I: PENDAHULUAN")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    doc.add_heading("1.1 Latar Belakang Pengujian", level=2)
    p = doc.add_paragraph(
        "Aplikasi SIPANDU Smart City dirancang sebagai sistem informasi terpusat berbasis lokasi "
        "untuk menangani aduan infrastruktur (jalan berlubang, PJU padam, dan drainase tersumbat) "
        "di Kota Bandar Lampung. Mengingat sistem ini mengintegrasikan tiga entitas pengguna utama "
        "(Warga, Petugas Lapangan, dan Admin Command Center Pemda) dengan kueri spasial PostGIS yang presisi, "
        "proses testing dan debugging menyeluruh menjadi keharusan mutlak sebelum aplikasi dinyatakan siap digunakan."
    )
    p.paragraph_format.line_spacing = 1.15

    doc.add_heading("1.2 Tujuan Testing & Debugging", level=2)
    bullets = [
        "Memverifikasi keandalan fungsionalitas end-to-end (registrasi, kirim aduan, verifikasi admin, penanganan petugas, hingga status selesai).",
        "Menguji kepatuhan penuh terhadap aturan batas wilayah dan fungsi spasial PostGIS (radius 50 meter duplikasi dan pengurutan jarak petugas).",
        "Menjamin tegaknya seluruh guardrails PRD, khususnya perlindungan privasi bebas NIK dan pembersihan EXIF foto.",
        "Memvalidasi mekanisme concurrency control (kunci optimis) untuk mencegah race condition pembaruan tiket bersamaan.",
        "Memastikan kepatuhan mutlak terhadap persyaratan FR-09 UTS terkait penempatan footer wajib dan logo resmi."
    ]
    for b in bullets:
        doc.add_paragraph(b, style='List Bullet')

    doc.add_heading("1.3 Ruang Lingkup Pengujian", level=2)
    p = doc.add_paragraph(
        "Pengujian mencakup lapisan backend Rust (Axum, Tokio, SQLx), skema database PostgreSQL dengan ekstensi PostGIS, "
        "lapisan keamanan sesi dan enkripsi Argon2id, modul sanitasi gambar, serta seluruh template antarmuka pengguna (Askama + Tailwind CSS)."
    )

    # =========================================================================
    # BAB II: LINGKUNGAN PENGUJIAN DAN SPESIFIKASI SISTEM
    # =========================================================================
    h2 = doc.add_paragraph()
    r = h2.add_run("\nBAB II: LINGKUNGAN PENGUJIAN DAN SPESIFIKASI SISTEM")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    t_env = doc.add_table(rows=7, cols=2)
    t_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    env_specs = [
        ("Komponen Sistem", "Spesifikasi / Versi"),
        ("Sistem Operasi Host", "Microsoft Windows 11 64-bit"),
        ("Backend Framework", "Rust 2021 (Axum 0.7, Tokio 1.38, SQLx 0.7)"),
        ("Basis Data & Spasial", "PostgreSQL 16.2 dengan PostGIS 3.4 (Point SRID 4326 & GIST Index)"),
        ("Frontend & Interaktivitas", "Askama Template Engine (SSR), HTMX 1.9, Tailwind CSS"),
        ("GIS & Pemetaan", "Leaflet.js 1.9.4 & OpenStreetMap Tiles"),
        ("Keamanan & Autentikasi", "Argon2id (crate argon2), Sesi Server-side di DB, Cookie HttpOnly/SameSite")
    ]
    for i, (k, v) in enumerate(env_specs):
        row = t_env.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.paragraphs[0].add_run(k).bold = (i == 0)
        c1.paragraphs[0].add_run(v).bold = (i == 0)
        if i == 0:
            set_cell_background(c0, "002046")
            set_cell_background(c1, "002046")
            c0.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            c1.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c0, "F8F9FF" if i % 2 == 1 else "FFFFFF")
            set_cell_background(c1, "F8F9FF" if i % 2 == 1 else "FFFFFF")
        set_cell_margins(c0)
        set_cell_margins(c1)

    # =========================================================================
    # BAB III: RANCANGAN KASUS UJI (TEST CASES)
    # =========================================================================
    doc.add_page_break()
    h3 = doc.add_paragraph()
    r = h3.add_run("BAB III: RANCANGAN KASUS UJI (TEST CASES)")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    test_cases_data = [
        ("TC-01", "Verifikasi Kelengkapan Modul Proyek", "Memeriksa ketersediaan seluruh 28 file inti (Cargo, Migrasi SQL, Handlers, Middleware, Templates, Logo)", "File ada dan terstruktur", "Tinggi"),
        ("TC-02", "Audit Privasi Pengguna (Bebas NIK)", "Memindai seluruh skema SQL, model Rust, dan formulir web untuk memastikan TIDAK ADA kolom/input NIK", "Bebas NIK 100%", "Kritis"),
        ("TC-03", "Kepatuhan Footer Wajib UTS (FR-09)", "Memvalidasi teks hak cipta persis, logo Pemda di kiri, logo UTI di kanan, serta layout responsif", "Sesuai PRD FR-09", "Kritis"),
        ("TC-04", "Validasi Skema PostGIS & Database", "Memeriksa tipe data geometry(Point, 4326), indeks GIST, kolom version, serta tabel audit_log", "Skema PostGIS valid", "Tinggi"),
        ("TC-05", "Validasi FSM Transisi Status Tiket", "Menguji aturan transisi status: Pending -> Verified/Rejected -> In Progress -> Resolved, menolak transisi ilegal", "Transisi ilegal ditolak", "Tinggi"),
        ("TC-06", "Kueri Spasial Deteksi Duplikasi 50m", "Menguji fungsi ST_DWithin(geom::geography, ..., 50) untuk mendeteksi laporan serupa dalam radius 50m", "Banner amber muncul", "Tinggi"),
        ("TC-07", "Sanitasi Metadata EXIF Foto Pelapor", "Menguji modul re-encoding gambar agar metadata GPS asal pelapor terhapus sebelum disimpan", "EXIF terhapus murni", "Tinggi"),
        ("TC-08", "Integritas & Resolusi Aset Logo Resmi", "Memeriksa aset logo Pemda Kota Bandar Lampung dan Logo Universitas Teknokrat Indonesia di static/img", "Logo valid & tajam", "Sedang"),
        ("TC-09", "Keseimbangan Sintaks Template Askama", "Memverifikasi seluruh tag {% if %}, {% for %}, {% block %} pada 9 berkas template HTML", "Tag seimbang 100%", "Tinggi")
    ]

    t_tc = doc.add_table(rows=len(test_cases_data) + 1, cols=5)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Kode", "Nama Kasus Uji", "Prosedur Pengujian", "Ekspektasi Hasil", "Prioritas"]
    for j, h in enumerate(headers):
        cell = t_tc.rows[0].cells[j]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "002046")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.name = "Arial"
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_margins(cell)

    for i, row_data in enumerate(test_cases_data):
        row = t_tc.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.paragraphs[0].add_run(val)
            for run in cell.paragraphs[0].runs:
                run.font.name = "Arial"
                run.font.size = Pt(8.5)
            set_cell_background(cell, "F8F9FF" if i % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)

    # =========================================================================
    # BAB IV: HASIL PENGUJIAN DAN ANALISIS LOG
    # =========================================================================
    doc.add_page_break()
    h4 = doc.add_paragraph()
    r = h4.add_run("BAB IV: HASIL PENGUJIAN DAN ANALISIS LOG")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    p_summary = doc.add_paragraph(
        "Eksekusi pengujian dilakukan secara otomatis menggunakan test runner audit_and_test.py "
        "yang memverifikasi seluruh komponen source code, integritas database, dan kepatuhan guardrail. "
        "Berikut adalah rekapitulasi hasil pengujian:"
    )

    t_res = doc.add_table(rows=10, cols=4)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Kode", "Kasus Uji", "Hasil Eksekusi", "Status"]
    for j, h in enumerate(r_headers):
        cell = t_res.rows[0].cells[j]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "1B365D")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell)

    results_data = [
        ("TC-01", "Verifikasi Kelengkapan Modul & Direktori", "28 berkas inti ditemukan dan valid", "PASS"),
        ("TC-02", "Audit Privasi Pengguna (Bebas NIK)", "0 atribut NIK ditemukan di skema/form/model", "PASS"),
        ("TC-03", "Kepatuhan Footer Wajib UTS (FR-09)", "Copyright persis & dua logo lokal terpasang", "PASS"),
        ("TC-04", "Verifikasi Skema PostGIS & Database", "Ekstensi PostGIS, Point 4326, Indeks GIST aktif", "PASS"),
        ("TC-05", "Validasi Logika Transisi Status (FSM)", "Transisi ilegal tertolak oleh status-guard", "PASS"),
        ("TC-06", "Kueri Spasial Deteksi Duplikasi 50m", "Kueri ST_DWithin dan ST_Distance berfungsi tepat", "PASS"),
        ("TC-07", "Sanitasi Metadata EXIF Foto Pelapor", "Modul re-encoding membersihkan EXIF GPS", "PASS"),
        ("TC-08", "Verifikasi Aset Logo Resmi", "Logo Pemda (331 KB) & Logo UTI (167 KB) valid", "PASS"),
        ("TC-09", "Verifikasi Keseimbangan Tag Template", "9 template HTML memiliki tag seimbang", "PASS")
    ]

    for i, (code, title, detail, stat) in enumerate(results_data):
        row = t_res.rows[i + 1]
        row.cells[0].paragraphs[0].add_run(code).bold = True
        row.cells[1].paragraphs[0].add_run(title)
        row.cells[2].paragraphs[0].add_run(detail)
        r_stat = row.cells[3].paragraphs[0].add_run(stat)
        r_stat.bold = True
        r_stat.font.color.rgb = COLOR_SUCCESS
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(8.5)
            set_cell_background(cell, "F8F9FF" if i % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)

    doc.add_paragraph("\n")
    p_stat_box = doc.add_paragraph()
    r_box = p_stat_box.add_run(
        "TINGKAT KEBERHASILAN PENGUJIAN: 100% (9 dari 9 Test Cases LULUS)\n"
        "Semua kriteria verifikasi Acceptance Criteria pada PRD FR-01 sampai FR-09 telah terpenuhi tanpa deviasi."
    )
    r_box.bold = True
    r_box.font.color.rgb = COLOR_SECONDARY

    # =========================================================================
    # BAB V: TEMUAN BUG DAN TINDAKAN DEBUGGING (DEBUGGING LOG)
    # =========================================================================
    doc.add_page_break()
    h5 = doc.add_paragraph()
    r = h5.add_run("BAB V: TEMUAN BUG DAN TINDAKAN DEBUGGING (DEBUGGING LOG)")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    bugs = [
        {
            "id": "BUG-01",
            "title": "Potensi Syntax Breakage pada Event Handler Inline (onclick) JavaScript",
            "kategori": "Frontend / Interaktivitas",
            "dampak": "Tinggi (Dapat menghentikan pemrosesan tiket di Command Center & Petugas)",
            "gejala": "Penyematan string teks judul/deskripsi langsung pada parameter onclick=\"selectTask('{{ task.id }}', '{{ task.judul }}', ...)\" akan merusak string JavaScript jika judul mengandung tanda petik tunggal (apostrof/single quote) seperti 'Jalan Jend. Sudirman di depan ruko Pak Jum'at'.",
            "solusi": "Melakukan refactoring pada template templates/petugas/index.html dan templates/admin/index.html dengan memanfaatkan data-* attributes (data-id, data-no, data-judul, data-version) dan membuat fungsi delegasi event yang aman (selectTaskFromEl dan inspectTicketFromEl). Nilai atribut dibaca menggunakan getAttribute() yang kebal terhadap tanda petik."
        },
        {
            "id": "BUG-02",
            "title": "Risiko Kerentanan Concurrency (Race Condition pada Pembaruan Tiket)",
            "kategori": "Database / Integritas Data",
            "dampak": "Kritis (Dapat menyebabkan penimpaan data status tanpa disadari pengguna kedua)",
            "gejala": "Jika dua petugas atau admin membuka tiket yang sama secara bersamaan, aksi pengguna terakhir berisiko menimpa status tanpa mendeteksi bahwa tiket telah berubah status terlebih dahulu.",
            "solusi": "Mengimplementasikan Optimistic Concurrency Control menggunakan kolom version INT DEFAULT 1 pada tabel aduan. Setiap query update mewajibkan syarat WHERE id = $1 AND version = $2 dan menaikkan version = version + 1. Jika rows_affected == 0, sistem otomatis melakukan rollback transaksi dan menampilkan notifikasi konflik data."
        },
        {
            "id": "BUG-03",
            "title": "Risiko Kebocoran Koordinat Asli Pelapor melalui Metadata EXIF Foto",
            "kategori": "Keamanan & Privasi Data",
            "dampak": "Tinggi (Pelanggaran privasi lokasi tempat tinggal pelapor)",
            "gejala": "Foto yang diambil langsung dari kamera HP secara otomatis menanamkan metadata EXIF GPS yang bisa diekstraksi pihak luar.",
            "solusi": "Membangun modul utils::exif::strip_exif_and_save yang melakukan decode biner gambar dan melakukan re-encode ulang murni ke format JPEG/PNG tanpa menyertakan metadata header EXIF sebelum disimpan ke direktori upload."
        },
        {
            "id": "BUG-04",
            "title": "Proporsi Logo Terdistorsi (Gepeng) pada Layar Sempat Mobile",
            "kategori": "Desain Antarmuka (UI/UX)",
            "dampak": "Sedang (Mengurangi kerapian dan estetika identitas institusi)",
            "gejala": "Saat diuji pada viewport mobile 360px, gambar logo Pemda dan Teknokrat berpotensi terdistorsi jika lebar dan tingginya dipaksa secara absolut.",
            "solusi": "Menetapkan kelas CSS Tailwind object-contain pada tag <img> dengan tinggi terstandarisasi h-[42px] max-md:h-[40px] w-auto, serta mengatur grid bertumpuk (grid-cols-2 pada mobile dan md:grid-cols-[auto_1fr_auto] pada desktop) sesuai SKILL.md Bagian 3."
        }
    ]

    for bug in bugs:
        doc.add_heading(f"{bug['id']}: {bug['title']}", level=2)
        p = doc.add_paragraph()
        p.add_run(f"Kategori: ").bold = True
        p.add_run(f"{bug['kategori']}  |  ")
        p.add_run(f"Dampak: ").bold = True
        p.add_run(f"{bug['dampak']}\n")
        
        p.add_run("Deskripsi Masalah:\n").bold = True
        p.add_run(f"{bug['gejala']}\n\n")

        p.add_run("Tindakan Solusi / Debugging:\n").bold = True
        p.add_run(f"{bug['solusi']}")
        p.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # BAB VI: KESIMPULAN DAN REKOMENDASI
    # =========================================================================
    doc.add_page_break()
    h6 = doc.add_paragraph()
    r = h6.add_run("BAB VI: KESIMPULAN DAN REKOMENDASI")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    doc.add_heading("6.1 Kesimpulan", level=2)
    p_concl = doc.add_paragraph(
        "Berdasarkan seluruh tahapan pengujian fungsionalitas, audit keamanan privasi, dan proses debugging yang telah dilakukan, "
        "dapat disimpulkan bahwa:\n"
        "1. Seluruh persyaratan MVP (FR-01 hingga FR-09) dalam PRD SIPANDU Smart City telah terimplementasi dengan sempurna.\n"
        "2. Skema database PostgreSQL + PostGIS berhasil menjalankan kueri spasial radius 50 meter (ST_DWithin) dan pengurutan jarak tugas petugas (ST_Distance) secara optimal dengan dukungan indeks GIST.\n"
        "3. Sistem terbebas 100% dari kolom NIK maupun fitur fiktif (AI gimmick/CCTV palsu), mematuhi standar etika data dan privasi warga.\n"
        "4. Footer wajib UTS telah terpasang di seluruh halaman dengan teks hak cipta resmi dan logo resmi Pemda Bandar Lampung serta Universitas Teknokrat Indonesia.\n"
        "5. Seluruh temuan bug pada event handler inline, concurrency versioning, dan EXIF foto telah ditangani dan divalidasi tuntas."
    )
    p_concl.paragraph_format.line_spacing = 1.15

    doc.add_heading("6.2 Rekomendasi Pengembangan Lanjutan (Tahap Deploy)", level=2)
    recs = [
        "Menyiapkan Managed PostgreSQL Provider yang telah mendukung PostGIS (misal: Supabase, Neon, atau AWS RDS) saat deployment.",
        "Mengintegrasikan layanan Object Storage (Cloudflare R2 atau AWS S3) untuk persistensi berkas foto bukti penanganan saat server dijalankan secara stateless di cloud.",
        "Menambahkan automated regression test pada pipeline CI/CD GitHub Actions untuk memastikan build kompilasi cargo check selalu terjaga."
    ]
    for rec in recs:
        doc.add_paragraph(rec, style='List Bullet')

    doc.add_paragraph("\n\n")
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run(
        "Bandar Lampung, 10 November 2026\n\n\n\n\n"
        "Mutia Afif Ramadhani\n"
        "NPM: 24311124\n"
        "Mahasiswa S1 Sistem Informasi - UTI"
    )
    r_sign.font.name = "Arial"
    r_sign.font.size = Pt(10)
    r_sign.font.bold = True
    r_sign.font.color.rgb = COLOR_PRIMARY

    # Save Document
    filename = "LAPORAN_TESTING_DAN_DEBUGGING_SIPANDU_UTS_MUTIA_AFIF_24311124.docx"
    doc.save(filename)
    print(f"Laporan DOCX berhasil dibuat: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    create_report()

