# =========================================================================
#    SIPANDU Smart City - Kota Bandar Lampung (UTS PPSI 2026)
#    Mutia Afif Ramadhani (24311124) | Dr. Erliyan Redy Susanto, M.Kom
# =========================================================================

Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "   SIPANDU Smart City - Kota Bandar Lampung (UTS PPSI 2026)" -ForegroundColor Green
Write-Host "   Penyusun: Mutia Afif Ramadhani (24311124) | Dosen: Dr. Erliyan Redy Susanto, M.Kom" -ForegroundColor Yellow
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Pastikan file .env ada
if (-not (Test-Path ".env")) {
    Write-Host "[1/3] Menyalin .env.example ke .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
} else {
    Write-Host "[1/3] File .env sudah tersedia." -ForegroundColor Gray
}

# 2. Menjalankan Docker PostGIS
Write-Host "[2/3] Menyalakan database PostgreSQL + PostGIS via Docker..." -ForegroundColor Yellow
try {
    docker compose up -d
    Write-Host "Container PostGIS aktif pada port 5432." -ForegroundColor Green
} catch {
    Write-Host "Peringatan: Pastikan Docker Desktop sudah aktif." -ForegroundColor Red
}

# 3. Menjalankan Server Rust Axum
Write-Host ""
Write-Host "[3/3] Menjalankan backend server Rust Axum..." -ForegroundColor Yellow
Write-Host "Aplikasi akan dapat diakses di: http://127.0.0.1:3000" -ForegroundColor Cyan
Write-Host ""

cargo run

