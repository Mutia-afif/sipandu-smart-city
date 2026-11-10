import os
import shutil

print("=========================================================================")
print("  BUILD VERCEL SITE - SIPANDU SMART CITY KOTA BANDAR LAMPUNG")
print("  Menyiapkan berkas statis & interaktif untuk Vercel Deployment")
print("  Penyusun: Mutia Afif Ramadhani (24311124) | Dosen: Dr. Erliyan Redy Susanto, M.Kom")
print("=========================================================================\n")

# 1. Pastikan folder public tersedia
public_dir = "public"
os.makedirs(public_dir, exist_ok=True)
os.makedirs(os.path.join(public_dir, "warga"), exist_ok=True)
os.makedirs(os.path.join(public_dir, "petugas"), exist_ok=True)
os.makedirs(os.path.join(public_dir, "admin"), exist_ok=True)
os.makedirs(os.path.join(public_dir, "simulasi"), exist_ok=True)
os.makedirs(os.path.join(public_dir, "login"), exist_ok=True)
os.makedirs(os.path.join(public_dir, "register"), exist_ok=True)

# 2. Salin aset statis ke public/static
dst_static = os.path.join(public_dir, "static")
if os.path.exists(dst_static):
    shutil.rmtree(dst_static)
shutil.copytree("static", dst_static)
print("Aset static berhasil disalin ke public/static.")

# Header Navigasi Standar
def get_header(active_nav=""):
    return f"""
  <header class="bg-surface-container-lowest/95 backdrop-blur-xl border-b border-[#E2E8F0] sticky top-0 z-40 shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-3 sm:gap-4">
        <a href="/" class="flex items-center gap-2.5">
          <img src="/static/img/logo_pemda.png" alt="Logo Pemda Kota Bandar Lampung"
               class="h-11 sm:h-12 w-auto object-contain hover:scale-105 transition-transform">
          <div class="flex flex-col">
            <span class="text-xs sm:text-sm font-extrabold uppercase tracking-wider text-primary">SIPANDU</span>
            <span class="text-[10px] text-on-surface-variant -mt-0.5 font-medium">Kota Bandar Lampung</span>
          </div>
        </a>

        <div class="hidden md:flex items-center gap-3 pl-3 border-l border-[#E2E8F0]">
          <a href="https://teknokrat.ac.id" target="_blank" rel="noopener" class="flex items-center gap-2">
            <img src="/static/img/logo_uti.png" alt="Logo Universitas Teknokrat Indonesia"
                 class="h-10 w-auto object-contain hover:scale-105 transition-transform">
            <div class="flex flex-col">
              <span class="text-[11px] font-bold text-secondary uppercase tracking-tight">Universitas Teknokrat Indonesia</span>
              <span class="text-[9px] text-on-surface-variant -mt-0.5">Kampus Juara &bull; Riset PPSI</span>
            </div>
          </a>
        </div>
      </div>

      <nav class="flex items-center gap-2 sm:gap-3">
        <a href="/warga" class="text-xs sm:text-sm font-semibold {'text-secondary' if active_nav == 'warga' else 'text-primary hover:text-secondary'} px-2.5 py-1.5 rounded-lg transition">Portal Warga</a>
        <a href="/petugas" class="text-xs sm:text-sm font-semibold {'text-secondary' if active_nav == 'petugas' else 'text-primary hover:text-secondary'} px-2.5 py-1.5 rounded-lg transition">Petugas</a>
        <a href="/admin" class="text-xs sm:text-sm font-semibold {'text-secondary' if active_nav == 'admin' else 'text-primary hover:text-secondary'} px-2.5 py-1.5 rounded-lg transition">Command Center</a>
        <a href="/simulasi" class="text-xs sm:text-sm font-bold bg-secondary/10 text-secondary hover:bg-secondary hover:text-white px-3 py-1.5 rounded-lg transition flex items-center gap-1">
          <span class="material-symbols-outlined text-base">account_tree</span>
          Simulasi UTS
        </a>
        <a href="/login" class="text-xs sm:text-sm font-bold bg-primary text-white px-3.5 py-2 rounded-lg hover:bg-primary-container transition flex items-center gap-1.5 shadow-sm">
          <span class="material-symbols-outlined text-base">login</span>
          Masuk
        </a>
      </nav>
    </div>
  </header>
"""

# Footer Wajib UTS (FR-09 & PRD)
def get_footer():
    return """
  <footer class="w-full bg-surface-container-lowest border-t border-[#E2E8F0] py-space-md mt-auto shadow-[0_-1px_6px_rgba(0,0,0,0.02)]">
    <div class="max-w-7xl mx-auto px-margin-mobile lg:px-margin grid grid-cols-2 md:grid-cols-[auto_1fr_auto] items-center gap-space-md">
      <!-- Kiri: Pemda Kota Bandar Lampung -->
      <div class="order-1 flex items-center gap-space-sm justify-self-start">
        <img alt="Logo Pemda Kota Bandar Lampung" src="/static/img/logo_pemda.png"
             class="h-[42px] max-md:h-[40px] w-auto object-contain"/>
        <div class="flex flex-col text-left">
          <span class="font-label-sm text-[11px] text-on-surface font-bold uppercase tracking-tight">Pemerintah Kota</span>
          <span class="font-label-md text-xs text-primary font-bold tracking-tight">Bandar Lampung</span>
        </div>
      </div>

      <!-- Tengah: Teks Hak Cipta Persis PRD FR-09 -->
      <p class="order-3 md:order-2 col-span-2 md:col-span-1 text-center font-body-sm text-xs sm:text-sm font-medium text-slate-600">
        Copyright©2026 by Mutia Afif Ramadhani dan Dr. Erliyan Redy Susanto, M.Kom
      </p>

      <!-- Kanan: Universitas Teknokrat Indonesia (UTI) -->
      <div class="order-2 md:order-3 flex items-center gap-space-sm justify-self-end">
        <div class="hidden sm:flex flex-col text-right">
          <span class="font-label-sm text-[11px] text-secondary font-bold uppercase tracking-wide">Kampus Juara - UTI</span>
          <span class="font-label-sm text-[10px] text-on-surface-variant">Universitas Teknokrat Indonesia</span>
        </div>
        <img alt="Logo Universitas Teknokrat Indonesia" src="/static/img/logo_uti.png"
             class="h-[42px] max-md:h-[40px] w-auto object-contain"/>
      </div>
    </div>
  </footer>
"""

# Base HTML Shell
def html_shell(title, content, active_nav=""):
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: "class",
      theme: {{
        extend: {{
          colors: {{
            "surface-bright": "#f8f9ff",
            "primary": "#002046",
            "primary-container": "#1b365d",
            "secondary": "#006b5f",
            "secondary-container": "#76f4e0",
            "surface": "#f8f9ff",
            "surface-container-lowest": "#ffffff",
            "surface-container-low": "#eff4ff",
            "surface-container": "#e5eeff",
            "on-surface": "#0b1c30",
            "on-surface-variant": "#44474e",
            "error": "#ba1a1a",
            "error-container": "#ffdad6",
            "on-error-container": "#93000a",
            "on-tertiary-container": "#dd8d00",
            "tertiary-fixed": "#ffddb8"
          }},
          spacing: {{
            "space-xs": "0.25rem", "space-sm": "0.5rem", "space-md": "1rem", "space-lg": "1.5rem", "space-xl": "2rem",
            "margin": "2rem", "margin-mobile": "1rem", "gutter": "1.5rem", "gutter-mobile": "1rem"
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="/static/css/styles.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body class="bg-surface text-on-surface min-h-screen flex flex-col font-sans">
  {get_header(active_nav)}
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
    {content}
  </main>
  {get_footer()}
</body>
</html>
"""

# Halaman 1: public/index.html (Landing Portal UTS)
landing_content = """
<div class="space-y-8">
  <!-- Banner Utama UTS -->
  <div class="bg-gradient-to-r from-primary via-primary-container to-secondary text-white p-8 sm:p-10 rounded-3xl shadow-lg relative overflow-hidden">
    <div class="relative z-10 max-w-3xl space-y-4">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-semibold">
        <span class="w-2 h-2 rounded-full bg-secondary-container animate-pulse"></span>
        UTS Proyek Pengembangan Sistem Informasi (PPSI) &bull; Tahun Akademik 2026
      </div>
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
        SIPANDU Smart City<br>
        <span class="text-secondary-container">Kota Bandar Lampung</span>
      </h1>
      <p class="text-sm sm:text-base text-slate-200 leading-relaxed">
        Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu berbasis Spasial PostGIS.
        Dikembangkan sebagai implementasi UTS mandiri atas nama <strong>Mutia Afif Ramadhani (NPM 24311124)</strong>, 
        di bawah bimbingan <strong>Dr. Erliyan Redy Susanto, M.Kom</strong>.
      </p>
      <div class="pt-2 flex flex-wrap items-center gap-3">
        <a href="/simulasi" class="px-5 py-2.5 bg-secondary-container text-primary font-bold rounded-xl text-xs sm:text-sm hover:scale-105 transition-transform flex items-center gap-2 shadow-md">
          <span class="material-symbols-outlined text-lg">play_circle</span>
          Buka Simulasi Interaktif 3 Peran
        </a>
        <a href="/warga" class="px-5 py-2.5 bg-white/15 hover:bg-white/25 text-white font-semibold rounded-xl text-xs sm:text-sm backdrop-blur-md transition flex items-center gap-2 border border-white/20">
          <span class="material-symbols-outlined text-lg">campaign</span>
          Portal Warga Pelapor
        </a>
      </div>
    </div>
  </div>

  <!-- 4 Kartu Modul Utama Sistem -->
  <div>
    <h2 class="text-lg font-extrabold text-primary mb-4 flex items-center gap-2">
      <span class="material-symbols-outlined text-secondary">grid_view</span>
      Pilih Antarmuka Layanan Peran Pengguna
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- Modul 1: Warga -->
      <a href="/warga" class="group bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm hover:border-secondary hover:shadow-md transition space-y-4">
        <div class="w-12 h-12 rounded-xl bg-secondary/10 text-secondary flex items-center justify-center group-hover:bg-secondary group-hover:text-white transition">
          <span class="material-symbols-outlined text-2xl">person_pin_circle</span>
        </div>
        <div>
          <h3 class="font-extrabold text-primary text-base group-hover:text-secondary transition">Portal Warga</h3>
          <p class="text-xs text-on-surface-variant mt-1 leading-relaxed">
            Kirim laporan dengan GPS Leaflet, deteksi duplikasi spasial 50m, dan pantau linimasa 4 status aduan.
          </p>
        </div>
        <span class="text-xs font-bold text-secondary inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          Akses Portal Warga &rarr;
        </span>
      </a>

      <!-- Modul 2: Petugas -->
      <a href="/petugas" class="group bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm hover:border-primary hover:shadow-md transition space-y-4">
        <div class="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center group-hover:bg-primary group-hover:text-white transition">
          <span class="material-symbols-outlined text-2xl">engineering</span>
        </div>
        <div>
          <h3 class="font-extrabold text-primary text-base group-hover:text-primary transition">Petugas Lapangan</h3>
          <p class="text-xs text-on-surface-variant mt-1 leading-relaxed">
            Daftar tugas terurut prioritas dan jarak lokasi, ambil penugasan, serta unggah foto bukti selesai.
          </p>
        </div>
        <span class="text-xs font-bold text-primary inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          Akses Portal Petugas &rarr;
        </span>
      </a>

      <!-- Modul 3: Admin -->
      <a href="/admin" class="group bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm hover:border-primary-container hover:shadow-md transition space-y-4">
        <div class="w-12 h-12 rounded-xl bg-primary-container/10 text-primary-container flex items-center justify-center group-hover:bg-primary-container group-hover:text-white transition">
          <span class="material-symbols-outlined text-2xl">shield_person</span>
        </div>
        <div>
          <h3 class="font-extrabold text-primary text-base group-hover:text-primary-container transition">Command Center Admin</h3>
          <p class="text-xs text-on-surface-variant mt-1 leading-relaxed">
            Monitoring 4 KPI kota, verifikasi dan disposisi tiket ke dinas teknis, peta GIS titik kerusakan, dan audit trail.
          </p>
        </div>
        <span class="text-xs font-bold text-primary-container inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          Akses Command Center &rarr;
        </span>
      </a>

      <!-- Modul 4: Simulasi Demo -->
      <a href="/simulasi" class="group bg-surface-container-lowest p-6 rounded-2xl border-2 border-secondary/30 shadow-sm hover:border-secondary hover:shadow-md transition space-y-4 bg-gradient-to-b from-secondary/5 to-transparent">
        <div class="w-12 h-12 rounded-xl bg-secondary text-white flex items-center justify-center group-hover:scale-110 transition-transform">
          <span class="material-symbols-outlined text-2xl">account_tree</span>
        </div>
        <div>
          <h3 class="font-extrabold text-secondary text-base">Simulasi Interaktif 3 Peran</h3>
          <p class="text-xs text-on-surface-variant mt-1 leading-relaxed">
            Halaman presentasi demo berdampingan (Warga, Admin, Petugas PU) untuk memverifikasi Skenario A & B di depan dosen.
          </p>
        </div>
        <span class="text-xs font-bold text-secondary inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          Buka Demo Simulasi &rarr;
        </span>
      </a>

    </div>
  </div>

  <!-- Detail Spesifikasi & Kepatuhan Guardrails UTS -->
  <div class="bg-surface-container-low p-6 rounded-2xl border border-[#E2E8F0] space-y-4">
    <div class="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
      <h3 class="text-sm font-bold text-primary uppercase tracking-wider flex items-center gap-2">
        <span class="material-symbols-outlined text-base text-secondary">verified</span>
        Kepatuhan Standar Guardrails UTS (PRD Section 1 s/d 13)
      </h3>
      <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-secondary/10 text-secondary">Status: 100% Terpenuhi</span>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
      <div class="p-3 bg-white rounded-xl border border-[#E2E8F0]">
        <strong class="text-primary block mb-1">1. Privasi Warga (Bebas NIK)</strong>
        <p class="text-on-surface-variant">Sesuai UU PDP & PRD FR-01, sistem sama sekali tidak meminta, memproses, atau menyimpan NIK pada registrasi warga.</p>
      </div>
      <div class="p-3 bg-white rounded-xl border border-[#E2E8F0]">
        <strong class="text-primary block mb-1">2. Spasial PostGIS 50 Meter</strong>
        <p class="text-on-surface-variant">Deteksi duplikasi aduan murni menggunakan fungsi spasial ST_DWithin radius 50m dan pengurutan petugas via ST_Distance.</p>
      </div>
      <div class="p-3 bg-white rounded-xl border border-[#E2E8F0]">
        <strong class="text-primary block mb-1">3. Optimistic Concurrency Control</strong>
        <p class="text-on-surface-variant">Setiap transaksi status aduan menguji kolom version INT untuk mencegah penimpaan data simultan (race condition).</p>
      </div>
    </div>
  </div>
</div>
"""

with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("SIPANDU Smart City - Kota Bandar Lampung (UTS PPSI 2026)", landing_content, ""))

# Halaman 2: public/simulasi/index.html
with open("templates/simulasi/index.html", "r", encoding="utf-8") as f:
    sim_raw = f.read()
# Ambil block content simulasi
sim_content = sim_raw.split("{% block content %}")[1].split("{% endblock %}")[0]
with open(os.path.join(public_dir, "simulasi", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Simulasi Alur Terpadu 3 Peran - SIPANDU Smart City (Demo UTS)", sim_content, "simulasi"))

# Halaman 3: public/warga/index.html
warga_interactive_content = """
<div class="space-y-6">
  <!-- Header Portal Warga -->
  <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-secondary text-white flex items-center justify-center">
        <span class="material-symbols-outlined text-2xl">campaign</span>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest">Portal Warga Pelapor</span>
          <span class="text-slate-300">&bull;</span>
          <span class="text-[10px] font-semibold text-on-surface-variant">Kota Bandar Lampung</span>
        </div>
        <h1 class="text-xl font-extrabold text-primary">Layanan Pengaduan Kerusakan Infrastruktur</h1>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-xs font-medium text-slate-600">Pelapor: <strong class="text-primary">Mutia Afif (Warga)</strong></span>
      <a href="/login" class="text-xs font-bold text-error px-2 py-1 rounded hover:bg-error-container/30 transition">Keluar</a>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
    <!-- Formulir Kirim Aduan Baru -->
    <div class="lg:col-span-6 bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-4">
      <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
        <span class="material-symbols-outlined text-secondary">add_location_alt</span>
        Kirim Aduan Infrastruktur Baru
      </h2>

      <!-- Peringatan Duplikasi PostGIS 50m (Live Reactive) -->
      <div id="duplicate-warning-banner" class="hidden p-3.5 rounded-xl bg-tertiary-fixed text-on-tertiary-container border border-on-tertiary-container/30 text-xs flex items-start gap-2.5">
        <span class="material-symbols-outlined text-lg shrink-0">warning</span>
        <div>
          <strong class="block font-bold">Peringatan Spasial PostGIS ST_DWithin (Radius 50m):</strong>
          <span id="duplicate-msg">Terdeteksi aduan aktif serupa di lokasi ini. Anda tetap dapat melanjutkan pengiriman.</span>
        </div>
      </div>

      <form id="warga-form" onsubmit="handleWargaSubmit(event)" class="space-y-4 text-xs">
        <div>
          <label class="block font-bold text-on-surface-variant mb-1.5">Pilih Kategori Infrastruktur (3 Kategori MVP):</label>
          <div class="grid grid-cols-3 gap-2">
            <label class="flex items-center gap-2 p-2.5 rounded-xl border border-[#E2E8F0] cursor-pointer hover:border-secondary transition bg-surface-container-low">
              <input type="radio" name="kategori" value="Jalan Berlubang" checked class="text-secondary focus:ring-secondary">
              <span class="font-bold text-[11px] text-primary">Jalan Berlubang</span>
            </label>
            <label class="flex items-center gap-2 p-2.5 rounded-xl border border-[#E2E8F0] cursor-pointer hover:border-secondary transition bg-surface-container-low">
              <input type="radio" name="kategori" value="PJU Padam" class="text-secondary focus:ring-secondary">
              <span class="font-bold text-[11px] text-primary">PJU Padam</span>
            </label>
            <label class="flex items-center gap-2 p-2.5 rounded-xl border border-[#E2E8F0] cursor-pointer hover:border-secondary transition bg-surface-container-low">
              <input type="radio" name="kategori" value="Drainase Tersumbat" class="text-secondary focus:ring-secondary">
              <span class="font-bold text-[11px] text-primary">Drainase</span>
            </label>
          </div>
        </div>

        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Judul Singkat Kerusakan:</label>
          <input type="text" id="warga-judul" required placeholder="Contoh: Lubang Aspal Dalam Membahayakan Motor"
                 class="w-full px-3 py-2 rounded-lg border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
        </div>

        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Deskripsi & Patokan Lokasi:</label>
          <textarea id="warga-deskripsi" rows="3" required placeholder="Jelaskan kondisi kerusakan dan patokan ruko/bangunan terdekat..."
                    class="w-full px-3 py-2 rounded-lg border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs"></textarea>
        </div>

        <!-- Pemetaan GPS Leaflet + PostGIS Picker -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="font-bold text-on-surface-variant">Tandai Titik Lokasi di Peta (GPS Leaflet):</label>
            <button type="button" onclick="detectLocation()" class="text-[11px] font-bold text-secondary hover:underline flex items-center gap-1">
              <span class="material-symbols-outlined text-xs">my_location</span> Titik Teknokrat
            </button>
          </div>
          <div id="warga-map" class="h-48 w-full rounded-xl border border-[#E2E8F0] z-10"></div>
          <div class="grid grid-cols-2 gap-2 mt-2">
            <input type="text" id="warga-lat" readonly value="-5.3812" class="px-2.5 py-1.5 bg-surface-container text-slate-600 rounded text-[11px] font-mono">
            <input type="text" id="warga-lng" readonly value="105.2571" class="px-2.5 py-1.5 bg-surface-container text-slate-600 rounded text-[11px] font-mono">
          </div>
        </div>

        <!-- Unggah Foto Bukti Awal -->
        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Lampirkan Foto Bukti (Maks. 3 foto &bull; Sanitasi EXIF Aktif):</label>
          <input type="file" id="warga-foto" accept="image/*" class="w-full text-[11px] file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-secondary/10 file:text-secondary hover:file:bg-secondary/20">
        </div>

        <button type="submit" class="w-full py-2.5 bg-secondary hover:bg-on-secondary-container text-white font-bold rounded-xl shadow-xs transition flex items-center justify-center gap-2 cursor-pointer">
          <span class="material-symbols-outlined text-sm">send</span>
          Kirim Laporan Pengaduan
        </button>
      </form>
    </div>

    <!-- Riwayat Aduan Saya & Linimasa 4 Status -->
    <div class="lg:col-span-6 space-y-4">
      <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-4">
        <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
          <span class="material-symbols-outlined text-secondary">history</span>
          Riwayat Pengaduan Saya (Linimasa Status)
        </h2>

        <div id="aduan-list-container" class="space-y-4">
          <!-- Item Aduan 1 (Default Seed) -->
          <div class="p-4 rounded-xl border border-[#E2E8F0] bg-surface-bright space-y-3">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10px] font-bold text-primary bg-primary-fixed px-2 py-0.5 rounded">#BDL-2026-7782</span>
              <span class="text-[10px] text-on-surface-variant">10 Nov 2026, 14:15 WIB</span>
            </div>
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-primary text-xs">Jalan Berlubang di Depan Gerbang Teknokrat</h3>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-fixed-variant">Selesai Ditangani</span>
            </div>
            <p class="text-[11px] text-on-surface-variant">Lubang aspal sedalam 15cm sangat membahayakan pengendara roda dua saat tergenang hujan.</p>
            
            <!-- 4-Step Stepper -->
            <div class="grid grid-cols-4 gap-1 text-[9px] text-center font-bold pt-1">
              <div class="p-1 rounded bg-secondary text-white">Diterima</div>
              <div class="p-1 rounded bg-secondary text-white">Diverifikasi</div>
              <div class="p-1 rounded bg-secondary text-white">Penanganan</div>
              <div class="p-1 rounded bg-secondary text-white">Selesai</div>
            </div>

            <!-- Catatan Selesai & Foto Bukti -->
            <div class="p-2.5 rounded-lg bg-secondary/5 border border-secondary/20 text-[10px] space-y-1">
              <strong class="text-secondary flex items-center gap-1">
                <span class="material-symbols-outlined text-xs">check_circle</span>
                Telah Diselesaikan oleh Dinas Pekerjaan Umum:
              </strong>
              <p class="italic text-slate-600">"Penambalan aspal hotmix 2 titik telah tuntas dikerjakan oleh Tim Reaksi Cepat PU."</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  let map, marker;
  window.addEventListener('DOMContentLoaded', () => {
    // Inisialisasi Peta Leaflet di Bandar Lampung
    map = L.map('warga-map').setView([-5.3812, 105.2571], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    marker = L.marker([-5.3812, 105.2571], { draggable: true }).addTo(map);
    marker.on('dragend', function (e) {
      const pos = marker.getLatLng();
      updateCoordinates(pos.lat, pos.lng);
    });

    map.on('click', function(e) {
      marker.setLatLng(e.latlng);
      updateCoordinates(e.latlng.lat, e.latlng.lng);
    });
  });

  function updateCoordinates(lat, lng) {
    document.getElementById('warga-lat').value = lat.toFixed(6);
    document.getElementById('warga-lng').value = lng.toFixed(6);

    // Cek Duplikasi Spasial 50 Meter terhadap titik Teknokrat (-5.3812, 105.2571)
    const dist = calculateDistance(lat, lng, -5.3812, 105.2571);
    const warn = document.getElementById('duplicate-warning-banner');
    if (dist <= 50) {
      warn.classList.remove('hidden');
      document.getElementById('duplicate-msg').innerText = `Terdeteksi aduan aktif berjarak ${Math.round(dist)} meter dari titik ini (Radius 50m PostGIS). Warga tetap dapat melanjutkan pengiriman.`;
    } else {
      warn.classList.add('hidden');
    }
  }

  function detectLocation() {
    map.setView([-5.3812, 105.2571], 16);
    marker.setLatLng([-5.3812, 105.2571]);
    updateCoordinates(-5.3812, 105.2571);
  }

  function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371e3;
    const phi1 = lat1 * Math.PI / 180;
    const phi2 = lat2 * Math.PI / 180;
    const dphi = (lat2 - lat1) * Math.PI / 180;
    const dlam = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dphi/2) * Math.sin(dphi/2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(dlam/2) * Math.sin(dlam/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  function handleWargaSubmit(e) {
    e.preventDefault();
    const judul = document.getElementById('warga-judul').value;
    const desc = document.getElementById('warga-deskripsi').value;
    const randNum = Math.floor(1000 + Math.random() * 9000);
    const ticketId = `#BDL-2026-${randNum}`;

    const newCard = document.createElement('div');
    newCard.className = "p-4 rounded-xl border border-secondary/40 bg-secondary/5 space-y-3 animate-fade-in";
    newCard.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-mono text-[10px] font-bold text-primary bg-primary-fixed px-2 py-0.5 rounded">${ticketId}</span>
        <span class="text-[10px] text-secondary font-bold">Baru Dikirim</span>
      </div>
      <div class="flex items-center justify-between">
        <h3 class="font-bold text-primary text-xs">${judul}</h3>
        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">Diterima (Pending)</span>
      </div>
      <p class="text-[11px] text-on-surface-variant">${desc}</p>
      <div class="grid grid-cols-4 gap-1 text-[9px] text-center font-bold pt-1">
        <div class="p-1 rounded bg-secondary text-white">Diterima</div>
        <div class="p-1 rounded bg-slate-200 text-slate-500">Diverifikasi</div>
        <div class="p-1 rounded bg-slate-200 text-slate-500">Penanganan</div>
        <div class="p-1 rounded bg-slate-200 text-slate-500">Selesai</div>
      </div>
    `;

    const container = document.getElementById('aduan-list-container');
    container.insertBefore(newCard, container.firstChild);
    document.getElementById('warga-form').reset();
    alert(`Aduan berhasil dikirim dengan Nomor Tiket ${ticketId}! Tiket masuk antrean verifikasi Admin Pemda.`);
  }
</script>
"""

with open(os.path.join(public_dir, "warga", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Portal Warga - SIPANDU Smart City", warga_interactive_content, "warga"))

# Halaman 4: public/petugas/index.html
petugas_interactive_content = """
<div class="space-y-6">
  <!-- Header Petugas -->
  <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-primary text-white flex items-center justify-center">
        <span class="material-symbols-outlined text-2xl">engineering</span>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-bold text-primary uppercase tracking-widest">Portal Lapangan</span>
          <span class="text-slate-300">&bull;</span>
          <span class="text-[10px] font-bold text-secondary uppercase">Dinas Pekerjaan Umum Kota Bandar Lampung</span>
        </div>
        <h1 class="text-xl font-extrabold text-primary">Meja Kerja Penanganan Petugas PU</h1>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-xs text-slate-600">Petugas: <strong class="text-primary">Pak Dedi (Dinas PU)</strong></span>
      <a href="/login" class="text-xs font-bold text-error px-2 py-1 rounded hover:bg-error-container/30 transition">Keluar</a>
    </div>
  </div>

  <!-- Counter Ringkasan Tugas -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0]">
      <span class="text-[11px] font-bold text-on-surface-variant block">Total Tugas</span>
      <span class="text-2xl font-extrabold text-primary" id="p-total">8</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0]">
      <span class="text-[11px] font-bold text-on-surface-variant block">Menunggu Aksi</span>
      <span class="text-2xl font-extrabold text-on-tertiary-container" id="p-pending">2</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0]">
      <span class="text-[11px] font-bold text-on-surface-variant block">Dalam Penanganan</span>
      <span class="text-2xl font-extrabold text-primary-container" id="p-progress">1</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0]">
      <span class="text-[11px] font-bold text-on-surface-variant block">Tuntas Selesai</span>
      <span class="text-2xl font-extrabold text-secondary" id="p-resolved">5</span>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
    <!-- Daftar Tugas Lapangan Berurut Prioritas & Jarak -->
    <div class="lg:col-span-7 bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-4">
      <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
        <span class="material-symbols-outlined text-primary">format_list_bulleted</span>
        Daftar Tugas Berurut Prioritas & Jarak Spasial PostGIS
      </h2>

      <div class="space-y-3" id="petugas-task-list">
        <div class="p-4 rounded-xl border border-[#E2E8F0] bg-surface-bright space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="font-mono text-[10px] font-bold text-primary bg-primary-fixed px-2 py-0.5 rounded">#BDL-2026-9102</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-error-container text-error">Prioritas Tinggi</span>
          </div>
          <h3 class="font-bold text-primary text-xs">Jalan Ambles Tikungan Rajabasa Dekat Terminal</h3>
          <p class="text-[11px] text-on-surface-variant">Kedalaman 20cm, membahayakan bus dan angkutan umum.</p>
          <div class="flex items-center justify-between pt-1">
            <span class="text-[10px] text-secondary font-bold flex items-center gap-1">
              <span class="material-symbols-outlined text-xs">near_me</span> Jarak: ~450 Meter dari posisi Anda
            </span>
            <button onclick="selectPetugasTask('#BDL-2026-9102', 'Jalan Ambles Tikungan Rajabasa')" class="px-3 py-1.5 bg-primary text-white font-bold rounded-lg text-xs hover:bg-primary-container transition">
              Tangani Tiket Ini
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Eksekusi Penanganan Tugas -->
    <div class="lg:col-span-5 bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-4">
      <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
        <span class="material-symbols-outlined text-secondary">task_alt</span>
        Form Bukti Penyelesaian Pekerjaan
      </h2>

      <form id="petugas-resolve-form" onsubmit="handlePetugasSubmit(event)" class="space-y-4 text-xs">
        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Tiket yang Sedang Dikerjakan:</label>
          <input type="text" id="active-task-id" readonly value="#BDL-2026-9102 (Jalan Ambles)" class="w-full px-3 py-2 rounded-lg bg-surface-container font-mono text-xs font-bold text-primary">
        </div>

        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Catatan Teknis Penanganan Lapangan:</label>
          <textarea id="catatan-teknis" rows="3" required placeholder="Jelaskan material yang digunakan dan tindakan teknis..."
                    class="w-full px-3 py-2 rounded-lg border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">Penambalan darurat dengan agregat kelas A dan lapisan aspal dingin telah selesai dipadatkan.</textarea>
        </div>

        <div>
          <label class="block font-bold text-on-surface-variant mb-1">Wajib Unggah Foto Bukti Selesai (FR-05):</label>
          <input type="file" id="petugas-foto" accept="image/*" required class="w-full text-[11px] file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-secondary/10 file:text-secondary hover:file:bg-secondary/20">
        </div>

        <button type="submit" class="w-full py-2.5 bg-secondary hover:bg-on-secondary-container text-white font-bold rounded-xl shadow-xs transition flex items-center justify-center gap-2 cursor-pointer">
          <span class="material-symbols-outlined text-sm">verified</span>
          Kirim Bukti & Selesaikan Tiket
        </button>
      </form>
    </div>
  </div>
</div>

<script>
  function selectPetugasTask(id, judul) {
    document.getElementById('active-task-id').value = `${id} (${judul})`;
    alert(`Tiket ${id} dipilih. Status kini "Dalam Penanganan".`);
  }

  function handlePetugasSubmit(e) {
    e.preventDefault();
    const taskId = document.getElementById('active-task-id').value;
    alert(`Sukses! Bukti penanganan untuk tiket ${taskId} berhasil disimpan dan status tiket dinyatakan Selesai.`);
    document.getElementById('p-resolved').innerText = parseInt(document.getElementById('p-resolved').innerText) + 1;
    document.getElementById('p-pending').innerText = Math.max(0, parseInt(document.getElementById('p-pending').innerText) - 1);
  }
</script>
"""

with open(os.path.join(public_dir, "petugas", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Portal Petugas Lapangan - SIPANDU Smart City", petugas_interactive_content, "petugas"))

# Halaman 5: public/admin/index.html
admin_interactive_content = """
<div class="space-y-6">
  <!-- Header Admin -->
  <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-primary-container text-white flex items-center justify-center">
        <span class="material-symbols-outlined text-2xl">shield_person</span>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest">Command Center Pemkot</span>
          <span class="text-slate-300">&bull;</span>
          <span class="text-[10px] font-bold text-primary uppercase">Pemerintah Kota Bandar Lampung</span>
        </div>
        <h1 class="text-xl font-extrabold text-primary">Dashboard Pengawasan & Disposisi Aduan</h1>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-xs text-slate-600">Administrator: <strong class="text-primary">Admin Pemda BDL</strong></span>
      <a href="/login" class="text-xs font-bold text-error px-2 py-1 rounded hover:bg-error-container/30 transition">Keluar</a>
    </div>
  </div>

  <!-- 4 KPI Cards -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0] shadow-xs">
      <span class="text-[11px] font-bold text-on-surface-variant block">Total Aduan Masuk</span>
      <span class="text-2xl font-extrabold text-primary">42</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0] shadow-xs">
      <span class="text-[11px] font-bold text-on-surface-variant block">Antrean Verifikasi (Pending)</span>
      <span class="text-2xl font-extrabold text-on-tertiary-container" id="admin-pending-count">3</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0] shadow-xs">
      <span class="text-[11px] font-bold text-on-surface-variant block">Sedang Dikerjakan</span>
      <span class="text-2xl font-extrabold text-primary-container">7</span>
    </div>
    <div class="p-4 bg-surface-container-lowest rounded-xl border border-[#E2E8F0] shadow-xs">
      <span class="text-[11px] font-bold text-on-surface-variant block">Tuntas Selesai</span>
      <span class="text-2xl font-extrabold text-secondary">32</span>
    </div>
  </div>

  <!-- Peta Sebaran GIS Kota Bandar Lampung -->
  <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-3">
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2">
        <span class="material-symbols-outlined text-secondary">map</span>
        Peta Sebaran Spasial Kerusakan Infrastruktur (PostGIS Point 4326)
      </h2>
      <span class="text-xs text-on-surface-variant">Radius Kota Bandar Lampung</span>
    </div>
    <div id="admin-map" class="h-64 w-full rounded-xl border border-[#E2E8F0] z-10"></div>
  </div>

  <!-- Antrean Verifikasi & Disposisi Dinas -->
  <div class="bg-surface-container-lowest p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-4">
    <h2 class="text-sm font-extrabold text-primary uppercase tracking-wider flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
      <span class="material-symbols-outlined text-on-tertiary-container">pending_actions</span>
      Antrean Verifikasi Masuk (Admin Dispatcher)
    </h2>

    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead class="bg-surface-container text-primary font-bold">
          <tr>
            <th class="p-3">No. Tiket</th>
            <th class="p-3">Kategori</th>
            <th class="p-3">Judul & Lokasi</th>
            <th class="p-3">Waktu Masuk</th>
            <th class="p-3 text-right">Aksi Verifikasi / Disposisi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[#E2E8F0]" id="admin-table-body">
          <tr>
            <td class="p-3 font-mono font-bold text-primary">#BDL-2026-1044</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded-full bg-slate-100 font-semibold text-[10px]">Jalan Berlubang</span></td>
            <td class="p-3">
              <strong class="text-primary block">Lubang Dalam Sebelah Halte Teknokrat</strong>
              <span class="text-slate-500 text-[10px]">Jl. ZA Pagar Alam No. 9</span>
            </td>
            <td class="p-3 text-slate-500 text-[10px]">10 Menit Lalu</td>
            <td class="p-3 text-right space-x-1.5">
              <button onclick="adminVerify('#BDL-2026-1044')" class="px-2.5 py-1.5 bg-secondary text-white font-bold rounded-lg text-[10px] hover:bg-on-secondary-container transition">
                Diverifikasi & Disposisi PU
              </button>
              <button onclick="adminReject('#BDL-2026-1044')" class="px-2.5 py-1.5 bg-error-container text-error font-bold rounded-lg text-[10px] hover:bg-error hover:text-white transition">
                Tolak
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
  window.addEventListener('DOMContentLoaded', () => {
    const adminMap = L.map('admin-map').setView([-5.4292, 105.2611], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(adminMap);

    // Titik Spasial Contoh di Bandar Lampung
    const points = [
      { lat: -5.3812, lng: 105.2571, title: "#BDL-2026-7782: Selesai", color: "green" },
      { lat: -5.3850, lng: 105.2590, title: "#BDL-2026-1044: Pending", color: "orange" },
      { lat: -5.4200, lng: 105.2650, title: "#BDL-2026-9102: In Progress", color: "blue" }
    ];

    points.forEach(p => {
      L.circleMarker([p.lat, p.lng], {
        radius: 8,
        fillColor: p.color,
        color: "#fff",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      }).addTo(adminMap).bindPopup(`<b>${p.title}</b>`);
    });
  });

  function adminVerify(ticket) {
    alert(`Tiket ${ticket} berhasil diverifikasi! Didelegasikan ke Dinas Pekerjaan Umum dengan Prioritas TINGGI.`);
    document.getElementById('admin-pending-count').innerText = Math.max(0, parseInt(document.getElementById('admin-pending-count').innerText) - 1);
  }

  function adminReject(ticket) {
    const reason = prompt("Masukkan alasan resmi penolakan tiket (Wajib transparansi):", "Bukan wewenang jalan kota (Kementerian PUPR)");
    if (reason) {
      alert(`Tiket ${ticket} ditolak dengan alasan: "${reason}". Catatan masuk audit log.`);
      document.getElementById('admin-pending-count').innerText = Math.max(0, parseInt(document.getElementById('admin-pending-count').innerText) - 1);
    }
  }
</script>
"""

with open(os.path.join(public_dir, "admin", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Command Center Admin - SIPANDU Smart City", admin_interactive_content, "admin"))

# Halaman 6: public/login/index.html & public/register/index.html
login_content = """
<div class="max-w-md mx-auto my-6 bg-surface-container-lowest p-8 rounded-3xl border border-[#E2E8F0] shadow-sm space-y-6">
  <div class="text-center space-y-2">
    <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary text-white mb-1 shadow-sm">
      <span class="material-symbols-outlined text-3xl">login</span>
    </div>
    <h1 class="text-xl font-extrabold text-primary">Masuk ke SIPANDU Smart City</h1>
    <p class="text-xs text-on-surface-variant">Pilih atau masukkan kredensial akun uji coba resmi UTS</p>
  </div>

  <form onsubmit="handleLoginSubmit(event)" class="space-y-4 text-xs">
    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Alamat Email Resmi:</label>
      <input type="email" id="login-email" required value="admin@bandarlampung.go.id"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Kata Sandi (Argon2id Hash):</label>
      <input type="password" id="login-password" required value="admin12345"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <button type="submit" class="w-full py-2.5 bg-primary hover:bg-primary-container text-white font-bold rounded-xl shadow-xs transition flex items-center justify-center gap-2 cursor-pointer">
      <span class="material-symbols-outlined text-sm">lock_open</span>
      Masuk ke Sistem
    </button>
  </form>

  <!-- Pilihan Cepat Kredensial Uji Dosen -->
  <div class="p-3.5 rounded-2xl bg-surface-container-low border border-[#E2E8F0] space-y-2 text-[11px]">
    <span class="font-bold text-primary block">Akun Pengujian Resmi UTS PPSI (Default Seed):</span>
    <div class="space-y-1">
      <button onclick="setCreds('admin@bandarlampung.go.id', 'admin12345', '/admin')" class="w-full text-left p-1.5 rounded hover:bg-white text-primary font-semibold flex items-center justify-between">
        <span>Admin Pemda: <code>admin@bandarlampung.go.id</code></span>
        <span class="text-[9px] text-secondary font-bold">Pilih &rarr;</span>
      </button>
      <button onclick="setCreds('petugas.pu@bandarlampung.go.id', 'petugas12345', '/petugas')" class="w-full text-left p-1.5 rounded hover:bg-white text-primary font-semibold flex items-center justify-between">
        <span>Petugas PU: <code>petugas.pu@bandarlampung.go.id</code></span>
        <span class="text-[9px] text-secondary font-bold">Pilih &rarr;</span>
      </button>
      <button onclick="setCreds('warga@gmail.com', 'warga12345', '/warga')" class="w-full text-left p-1.5 rounded hover:bg-white text-primary font-semibold flex items-center justify-between">
        <span>Warga: <code>warga@gmail.com</code></span>
        <span class="text-[9px] text-secondary font-bold">Pilih &rarr;</span>
      </button>
    </div>
  </div>

  <div class="text-center pt-1">
    <a href="/register" class="text-xs font-semibold text-secondary hover:underline">Belum punya akun warga? Daftar di sini (Tanpa NIK)</a>
  </div>
</div>

<script>
  let targetUrl = '/admin';
  function setCreds(email, pass, url) {
    document.getElementById('login-email').value = email;
    document.getElementById('login-password').value = pass;
    targetUrl = url;
  }
  function handleLoginSubmit(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    if (email.includes('admin')) window.location.href = '/admin';
    else if (email.includes('petugas')) window.location.href = '/petugas';
    else window.location.href = '/warga';
  }
</script>
"""

with open(os.path.join(public_dir, "login", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Masuk - SIPANDU Smart City", login_content, ""))

# Halaman 7: public/register/index.html
register_content = """
<div class="max-w-md mx-auto my-6 bg-surface-container-lowest p-8 rounded-3xl border border-[#E2E8F0] shadow-sm space-y-6">
  <div class="text-center space-y-2">
    <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-secondary text-white mb-1 shadow-sm">
      <span class="material-symbols-outlined text-3xl">how_to_reg</span>
    </div>
    <h1 class="text-xl font-extrabold text-primary">Registrasi Warga Baru</h1>
    <p class="text-xs text-on-surface-variant">Sesuai Prinsip Data Minimization UU PDP: <strong>Mutlak Tanpa NIK</strong></p>
  </div>

  <form onsubmit="handleRegister(event)" class="space-y-4 text-xs">
    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Nama Lengkap:</label>
      <input type="text" id="reg-nama" required placeholder="Contoh: Budi Santoso"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Alamat Email:</label>
      <input type="email" id="reg-email" required placeholder="budi@example.com"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Nomor Handphone (WhatsApp):</label>
      <input type="tel" id="reg-hp" required placeholder="081234567890"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <div>
      <label class="block font-bold text-on-surface-variant mb-1">Kata Sandi (Min. 8 Karakter):</label>
      <input type="password" id="reg-pass" required minlength="8" placeholder="••••••••"
             class="w-full px-3.5 py-2.5 rounded-xl border border-[#E2E8F0] bg-surface-container-low focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary text-xs">
    </div>

    <button type="submit" class="w-full py-2.5 bg-secondary hover:bg-on-secondary-container text-white font-bold rounded-xl shadow-xs transition flex items-center justify-center gap-2 cursor-pointer">
      <span class="material-symbols-outlined text-sm">person_add</span>
      Daftar Akun Warga
    </button>
  </form>

  <div class="text-center pt-1">
    <a href="/login" class="text-xs font-semibold text-primary hover:underline">Sudah punya akun? Masuk di sini</a>
  </div>
</div>

<script>
  function handleRegister(e) {
    e.preventDefault();
    alert("Pendaftaran berhasil! Akun Anda terdaftar secara aman menggunakan Argon2id tanpa NIK. Mengarahkan ke Portal Warga...");
    window.location.href = '/warga';
  }
</script>
"""

with open(os.path.join(public_dir, "register", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("Registrasi Warga - SIPANDU Smart City", register_content, ""))

# 4. Halaman 404
error_content = """
<div class="text-center py-16 space-y-4 max-w-md mx-auto">
  <div class="w-20 h-20 mx-auto rounded-3xl bg-error-container text-error flex items-center justify-center shadow-sm">
    <span class="material-symbols-outlined text-4xl">error_outline</span>
  </div>
  <h1 class="text-3xl font-extrabold text-primary">Halaman Tidak Ditemukan (404)</h1>
  <p class="text-xs text-on-surface-variant">Tautan yang Anda tuju tidak tersedia atau telah dipindahkan dalam sistem SIPANDU Smart City.</p>
  <div class="pt-2">
    <a href="/" class="px-5 py-2.5 bg-primary text-white font-bold rounded-xl text-xs hover:bg-primary-container transition inline-flex items-center gap-2">
      <span class="material-symbols-outlined text-sm">home</span> Kembali ke Beranda
    </a>
  </div>
</div>
"""
with open(os.path.join(public_dir, "404.html"), "w", encoding="utf-8") as f:
    f.write(html_shell("404 - Halaman Tidak Ditemukan", error_content, ""))

# 5. Konfigurasi vercel.json
vercel_json = '''{
  "version": 2,
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/", "destination": "/index.html" },
    { "source": "/warga", "destination": "/warga/index.html" },
    { "source": "/petugas", "destination": "/petugas/index.html" },
    { "source": "/admin", "destination": "/admin/index.html" },
    { "source": "/simulasi", "destination": "/simulasi/index.html" },
    { "source": "/login", "destination": "/login/index.html" },
    { "source": "/register", "destination": "/register/index.html" }
  ]
}
'''

with open("vercel.json", "w", encoding="utf-8") as f:
    f.write(vercel_json)

print("Seluruh berkas web public/ dan vercel.json berhasil dibuat!")

