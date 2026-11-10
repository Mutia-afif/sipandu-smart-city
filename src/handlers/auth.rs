use askama::Template;
use axum::{
    extract::State,
    http::header,
    response::{Html, IntoResponse, Redirect, Response},
    Form,
};
use chrono::{Duration, Utc};
use rand::{distributions::Alphanumeric, Rng};
use serde::Deserialize;
use uuid::Uuid;

use crate::{
    models::{User, UserRole},
    state::AppState,
};

#[derive(Template)]
#[template(path = "auth/login.html")]
pub struct LoginTemplate {
    pub error_msg: String,
}

#[derive(Template)]
#[template(path = "auth/register.html")]
pub struct RegisterTemplate {
    pub error_msg: String,
}

#[derive(Deserialize)]
pub struct LoginForm {
    pub email: String,
    pub password: String,
}

#[derive(Deserialize)]
pub struct RegisterForm {
    pub nama: String,
    pub email: String,
    pub no_hp: String,
    pub password: String,
}

pub async fn show_login() -> impl IntoResponse {
    Html(LoginTemplate { error_msg: String::new() }.render().unwrap())
}

pub async fn show_register() -> impl IntoResponse {
    Html(RegisterTemplate { error_msg: String::new() }.render().unwrap())
}

pub async fn handle_login(
    State(state): State<AppState>,
    Form(form): Form<LoginForm>,
) -> Response {
    let user = sqlx::query_as::<_, User>(
        "SELECT * FROM users WHERE email = $1 AND is_active = TRUE",
    )
    .bind(&form.email)
    .fetch_optional(&state.db)
    .await;

    let user = match user {
        Ok(Some(u)) => u,
        _ => {
            return Html(
                LoginTemplate {
                    error_msg: "Email atau kata sandi tidak sesuai.".to_string(),
                }
                .render()
                .unwrap(),
            )
            .into_response();
        }
    };

    // Verifikasi password Argon2
    let is_valid = argon2::verify_encoded(&user.password_hash, form.password.as_bytes())
        .unwrap_or(false);

    if !is_valid {
        return Html(
            LoginTemplate {
                error_msg: "Email atau kata sandi salah.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    // Buat token session aman
    let session_token: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(48)
        .map(char::from)
        .collect();

    let expires = Utc::now() + Duration::days(7);

    let _ = sqlx::query!(
        "INSERT INTO sessions (id, user_id, expires_at) VALUES ($1, $2, $3)",
        session_token,
        user.id,
        expires
    )
    .execute(&state.db)
    .await;

    let cookie = format!(
        "sipandu_session={}; Path=/; HttpOnly; SameSite=Lax; Max-Age={}",
        session_token,
        7 * 24 * 3600
    );

    // Redirect sesuai role
    let redirect_url = match user.role {
        UserRole::Warga => "/warga",
        UserRole::Petugas => "/petugas",
        UserRole::Admin => "/admin",
    };

    (
        [(header::SET_COOKIE, cookie)],
        Redirect::to(redirect_url),
    )
        .into_response()
}

pub async fn handle_register(
    State(state): State<AppState>,
    Form(form): Form<RegisterForm>,
) -> Response {
    // Validasi panjang input & keamanan data
    if form.nama.trim().is_empty() || form.nama.len() > 150 {
        return Html(
            RegisterTemplate {
                error_msg: "Nama lengkap wajib diisi dan maksimal 150 karakter.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    if form.email.trim().is_empty() || form.email.len() > 150 || !form.email.contains('@') {
        return Html(
            RegisterTemplate {
                error_msg: "Format alamat email tidak valid.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    if form.no_hp.trim().is_empty() || form.no_hp.len() > 25 {
        return Html(
            RegisterTemplate {
                error_msg: "Nomor HP wajib diisi dan maksimal 25 karakter.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    if form.password.len() < 8 || form.password.len() > 128 {
        return Html(
            RegisterTemplate {
                error_msg: "Kata sandi minimal 8 karakter dan maksimal 128 karakter.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    // Hash password menggunakan Argon2id
    let salt: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(16)
        .map(char::from)
        .collect();

    let config = argon2::Config::default();
    let password_hash = match argon2::hash_encoded(form.password.as_bytes(), salt.as_bytes(), &config) {
        Ok(h) => h,
        Err(_) => {
            return Html(
                RegisterTemplate {
                    error_msg: "Gagal memproses keamanan kata sandi.".to_string(),
                }
                .render()
                .unwrap(),
            )
            .into_response();
        }
    };

    let user_id = Uuid::new_v4();
    let result = sqlx::query!(
        r#"
        INSERT INTO users (id, nama, email, no_hp, password_hash, role)
        VALUES ($1, $2, $3, $4, $5, 'warga')
        "#,
        user_id,
        form.nama,
        form.email,
        form.no_hp,
        password_hash
    )
    .execute(&state.db)
    .await;

    if let Err(_) = result {
        return Html(
            RegisterTemplate {
                error_msg: "Email sudah terdaftar. Silakan gunakan email lain atau login.".to_string(),
            }
            .render()
            .unwrap(),
        )
        .into_response();
    }

    // Otomatis login setelah pendaftaran berhasil
    let session_token: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(48)
        .map(char::from)
        .collect();

    let expires = Utc::now() + Duration::days(7);
    let _ = sqlx::query!(
        "INSERT INTO sessions (id, user_id, expires_at) VALUES ($1, $2, $3)",
        session_token,
        user_id,
        expires
    )
    .execute(&state.db)
    .await;

    let cookie = format!(
        "sipandu_session={}; Path=/; HttpOnly; SameSite=Lax; Max-Age={}",
        session_token,
        7 * 24 * 3600
    );

    ([(header::SET_COOKIE, cookie)], Redirect::to("/warga")).into_response()
}

pub async fn handle_logout(
    State(state): State<AppState>,
    req: axum::extract::Request,
) -> Response {
    if let Some(cookies) = req.headers().get(header::COOKIE).and_then(|v| v.to_str().ok()) {
        for cookie in cookies.split(';') {
            let mut parts = cookie.trim().splitn(2, '=');
            if let (Some("sipandu_session"), Some(token)) = (parts.next(), parts.next()) {
                let _ = sqlx::query!("DELETE FROM sessions WHERE id = $1", token)
                    .execute(&state.db)
                    .await;
            }
        }
    }

    (
        [(
            header::SET_COOKIE,
            "sipandu_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0",
        )],
        Redirect::to("/login"),
    )
        .into_response()
}

