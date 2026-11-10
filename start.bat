@echo off
echo =========================================================================
echo    SIPANDU Smart City - Kota Bandar Lampung (UTS PPSI 2026)
echo    Mutia Afif Ramadhani (24311124) ^| Dr. Erliyan Redy Susanto, M.Kom
echo =========================================================================
echo.

if not exist .env (
    echo [INFO] Menyalin .env.example ke .env...
    copy .env.example .env
)

echo [1/2] Menyalakan container database PostgreSQL + PostGIS...
docker compose up -d

echo.
echo [2/2] Menjalankan backend server Rust Axum...
echo Server akan aktif di http://127.0.0.1:3000
echo.
cargo run

pause

