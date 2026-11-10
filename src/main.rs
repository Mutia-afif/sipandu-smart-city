use axum::{
    middleware,
    response::Redirect,
    routing::{get, post},
    Router,
};
use sqlx::postgres::PgPoolOptions;
use std::net::SocketAddr;
use tower_http::{
    cors::CorsLayer,
    services::ServeDir,
    trace::TraceLayer,
};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod handlers;
mod middleware as app_middleware;
mod models;
mod state;
mod utils;

use config::Config;
use state::AppState;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Inisialisasi logging
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "sipandu_smart_city=info,tower_http=info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // 2. Load konfigurasi lingkungan
    let config = Config::from_env();
    tracing::info!("Menghubungkan ke database PostgreSQL: {}", &config.database_url);

    // 3. Inisialisasi pool database PostgreSQL
    let db = PgPoolOptions::new()
        .max_connections(20)
        .connect(&config.database_url)
        .await
        .expect("Gagal menghubungkan ke database PostgreSQL");

    // 4. Jalankan migrasi skema SQL otomatis
    tracing::info!("Menjalankan migrasi PostGIS...");
    sqlx::migrate!("./migrations")
        .run(&db)
        .await
        .expect("Gagal menjalankan migrasi database");
    tracing::info!("Migrasi database PostGIS sukses.");

    // Pastikan folder upload tersedia
    let _ = std::fs::create_dir_all(&config.upload_dir);

    let state = AppState::new(db, config.clone());

    // 5. Susun router aplikasi
    let app = Router::new()
        // Halaman Utama -> Redirect ke login atau warga
        .route("/", get(|| async { Redirect::to("/warga") }))
        // Autentikasi (Tanpa NIK)
        .route("/login", get(handlers::show_login).post(handlers::handle_login))
        .route("/register", get(handlers::show_register).post(handlers::handle_register))
        .route("/logout", get(handlers::handle_logout))
        // Portal Warga
        .route("/warga", get(handlers::show_warga_portal))
        .route("/warga/aduan", post(handlers::submit_aduan))
        // Portal Petugas Lapangan
        .route("/petugas", get(handlers::show_petugas_portal))
        .route("/petugas/take", post(handlers::take_task))
        .route("/petugas/resolve", post(handlers::resolve_task))
        // Command Center Admin Pemda
        .route("/admin", get(handlers::show_admin_portal))
        .route("/admin/verify", post(handlers::verify_ticket))
        .route("/admin/reject", post(handlers::reject_ticket))
        // API Spasial & HTMX Helper
        .route("/api/aduan/check-duplicate", get(handlers::check_duplicate))
        .route("/api/aduan/points", get(handlers::get_map_points))
        // Layani file statis (CSS, JS, Logo, Upload Foto)
        .nest_service("/static", ServeDir::new("static"))
        // Fallback 404 (Memuat Footer Wajib UTS FR-09)
        .fallback(handlers::handle_404)
        // Middleware Auth Sesi Server-Side
        .layer(middleware::from_fn_with_state(
            state.clone(),
            app_middleware::auth_middleware,
        ))
        // Middleware Pengerasan Keamanan HTTP (Security Headers OWASP)
        .layer(middleware::from_fn(security_headers_middleware))
        .layer(TraceLayer::new_for_http())
        .layer(CorsLayer::permissive())
        .with_state(state);

    // 6. Jalankan web server Axum
    let addr = SocketAddr::new(
        config.host.parse().expect("Host tidak valid"),
        config.port,
    );
    tracing::info!("SIPANDU Smart City aktif melayani di http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}

/// Middleware Pengerasan Header Keamanan HTTP (OWASP Top 10 Security Headers)
async fn security_headers_middleware(
    req: axum::extract::Request,
    next: axum::middleware::Next,
) -> axum::response::Response {
    let mut response = next.run(req).await;
    let headers = response.headers_mut();
    
    // Mencegah browser menebak MIME-type secara sepihak (MIME sniffing attack)
    headers.insert(
        axum::http::header::HeaderName::from_static("x-content-type-options"),
        axum::http::HeaderValue::from_static("nosniff"),
    );
    // Mencegah Clickjacking dengan melarang rendering di dalam frame/iframe situs lain
    headers.insert(
        axum::http::header::HeaderName::from_static("x-frame-options"),
        axum::http::HeaderValue::from_static("SAMEORIGIN"),
    );
    // Mengaktifkan filter XSS di browser lawas
    headers.insert(
        axum::http::header::HeaderName::from_static("x-xss-protection"),
        axum::http::HeaderValue::from_static("1; mode=block"),
    );
    // Mengontrol pengiriman informasi perujuk saat navigasi keluar domain
    headers.insert(
        axum::http::header::HeaderName::from_static("referrer-policy"),
        axum::http::HeaderValue::from_static("strict-origin-when-cross-origin"),
    );
    // Content Security Policy (CSP) untuk membatasi sumber script, style, dan font sah
    headers.insert(
        axum::http::header::HeaderName::from_static("content-security-policy"),
        axum::http::HeaderValue::from_static(
            "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://*.tile.openstreetmap.org https://tile.openstreetmap.org blob:; connect-src 'self';",
        ),
    );

    response
}

