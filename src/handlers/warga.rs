use askama::Template;
use axum::{
    extract::{Multipart, State},
    response::{Html, IntoResponse, Redirect, Response},
    Extension,
};
use chrono::Utc;
use rand::Rng;
use std::path::Path;
use uuid::Uuid;

use crate::{
    middleware::{check_role, CurrentUser},
    models::{Aduan, UserRole},
    state::AppState,
    utils::exif::strip_exif_and_save,
};

#[derive(Template)]
#[template(path = "warga/index.html")]
pub struct WargaPortalTemplate {
    pub current_user_nama: String,
    pub aduan_list: Vec<AduanViewItem>,
}

pub struct AduanViewItem {
    pub id: String,
    pub no_aduan: String,
    pub nama_kategori: String,
    pub judul: String,
    pub deskripsi: String,
    pub alamat_teks: String,
    pub status: String,
    pub alasan_penolakan: String,
    pub catatan_penanganan: String,
    pub created_at: String,
    pub foto_laporan: String,
    pub foto_penanganan: String,
}

pub async fn show_warga_portal(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    if let Err(res) = check_role(Some(&cu), UserRole::Warga) {
        return res;
    }

    // Ambil daftar aduan milik warga ini
    let rows = sqlx::query!(
        r#"
        SELECT 
            a.id, a.no_aduan, a.judul, a.deskripsi, a.alamat_teks, 
            a.status as "status: _", a.alasan_penolakan, a.catatan_penanganan,
            a.created_at, c.nama_kategori
        FROM aduan a
        JOIN categories c ON a.category_id = c.id
        WHERE a.user_id = $1
        ORDER BY a.created_at DESC
        "#,
        cu.user.id
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let mut aduan_list = Vec::new();

    for r in rows {
        // Ambil foto laporan awal & foto penanganan petugas
        let fotos = sqlx::query!(
            "SELECT jenis, storage_key FROM aduan_foto WHERE aduan_id = $1",
            r.id
        )
        .fetch_all(&state.db)
        .await
        .unwrap_or_default();

        let mut foto_laporan = String::new();
        let mut foto_penanganan = String::new();

        for f in fotos {
            if f.jenis == "laporan" && foto_laporan.is_empty() {
                foto_laporan = f.storage_key;
            } else if f.jenis == "penanganan" && foto_penanganan.is_empty() {
                foto_penanganan = f.storage_key;
            }
        }

        aduan_list.push(AduanViewItem {
            id: r.id.to_string(),
            no_aduan: r.no_aduan,
            nama_kategori: r.nama_kategori,
            judul: r.judul,
            deskripsi: r.deskripsi,
            alamat_teks: r.alamat_teks.unwrap_or_default(),
            status: r.status.to_string(),
            alasan_penolakan: r.alasan_penolakan.unwrap_or_default(),
            catatan_penanganan: r.catatan_penanganan.unwrap_or_default(),
            created_at: r.created_at.format("%d %b %Y, %H:%M WIB").to_string(),
            foto_laporan,
            foto_penanganan,
        });
    }

    Html(
        WargaPortalTemplate {
            current_user_nama: cu.user.nama.clone(),
            aduan_list,
        }
        .render()
        .unwrap(),
    )
    .into_response()
}

pub async fn submit_aduan(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    mut multipart: Multipart,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    let mut category_id: Option<Uuid> = None;
    let mut latitude: Option<f64> = None;
    let mut longitude: Option<f64> = None;
    let mut judul = String::new();
    let mut deskripsi = String::new();
    let mut alamat_teks = String::new();
    let mut uploaded_files: Vec<(String, Vec<u8>)> = Vec::new();

    while let Ok(Some(field)) = multipart.next_field().await {
        let name = field.name().unwrap_or_default().to_string();
        if name == "category_id" {
            if let Ok(text) = field.text().await {
                category_id = Uuid::parse_str(&text).ok();
            }
        } else if name == "latitude" {
            if let Ok(text) = field.text().await {
                latitude = text.parse().ok();
            }
        } else if name == "longitude" {
            if let Ok(text) = field.text().await {
                longitude = text.parse().ok();
            }
        } else if name == "judul" {
            judul = field.text().await.unwrap_or_default();
        } else if name == "deskripsi" {
            deskripsi = field.text().await.unwrap_or_default();
        } else if name == "alamat_teks" {
            alamat_teks = field.text().await.unwrap_or_default();
        } else if name == "foto" {
            let filename = field.file_name().unwrap_or("foto.jpg").to_string();
            let lower_name = filename.to_lowercase();
            // Validasi format file foto (JPG, PNG, WebP)
            let is_valid_ext = lower_name.ends_with(".jpg") 
                || lower_name.ends_with(".jpeg") 
                || lower_name.ends_with(".png") 
                || lower_name.ends_with(".webp");

            if !is_valid_ext && !filename.is_empty() {
                return Redirect::to("/warga?error=format_foto_salah").into_response();
            }

            if let Ok(bytes) = field.bytes().await {
                // Validasi ukuran maks 5 MB (PRD FR-02)
                if bytes.len() > 5 * 1024 * 1024 {
                    return Redirect::to("/warga?error=foto_terlalu_besar").into_response();
                }
                if !bytes.is_empty() {
                    // Validasi Magic Bytes konten biner (Mencegah Web Shell & Polyglot File)
                    if !infer::is_image(&bytes) {
                        return Redirect::to("/warga?error=file_bukan_gambar").into_response();
                    }
                    uploaded_files.push((filename, bytes.to_vec()));
                }
            }
        }
    }

    // Validasi panjang input teks (Mencegah buffer overflow & database payload bloat)
    if judul.trim().is_empty() || judul.len() > 200 || deskripsi.len() > 3000 || alamat_teks.len() > 500 {
        return Redirect::to("/warga?error=input_tidak_valid").into_response();
    }

    let cat_id = match category_id {
        Some(id) => id,
        None => return Redirect::to("/warga?error=gagal_kirim").into_response(),
    };

    let lat = latitude.unwrap_or(-5.4292);
    let lng = longitude.unwrap_or(105.2611);

    // Ambil default dinas dari category
    let dinas_id = sqlx::query_scalar!("SELECT dinas_id FROM categories WHERE id = $1", cat_id)
        .fetch_optional(&state.db)
        .await
        .ok()
        .flatten();

    let aduan_id = Uuid::new_v4();
    let rand_num: u32 = rand::thread_rng().gen_range(1000..9999);
    let no_aduan = format!("BDL-2026-{}", rand_num);

    // Buka transaksi database
    let mut tx = match state.db.begin().await {
        Ok(t) => t,
        Err(_) => return Redirect::to("/warga").into_response(),
    };

    // Simpan ke tabel aduan dengan geometry Point PostGIS (SRID 4326)
    let insert_res = sqlx::query!(
        r#"
        INSERT INTO aduan (
            id, no_aduan, user_id, category_id, dinas_id, judul, deskripsi, alamat_teks,
            geom, status, prioritas, version
        )
        VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8,
            ST_SetSRID(ST_Point($9, $10), 4326),
            'pending', 'sedang', 1
        )
        "#,
        aduan_id,
        no_aduan,
        cu.user.id,
        cat_id,
        dinas_id,
        judul,
        deskripsi,
        alamat_teks,
        lng,
        lat
    )
    .execute(&mut *tx)
    .await;

    if let Err(e) = insert_res {
        tracing::error!("Gagal membuat aduan: {:?}", e);
        let _ = tx.rollback().await;
        return Redirect::to("/warga?error=gagal_kirim").into_response();
    }

    // Buat direktori upload jika belum ada
    let _ = std::fs::create_dir_all(&state.config.upload_dir);

    // Simpan foto dan bersihkan EXIF metadata
    for (i, (_name, bytes)) in uploaded_files.into_iter().take(3).enumerate() {
        let ext = "jpg";
        let filename = format!("{}_{}_{}.{}", aduan_id, i, Utc::now().timestamp(), ext);
        let target_path = Path::new(&state.config.upload_dir).join(&filename);
        let storage_key = format!("/static/uploads/{}", filename);

        if let Ok(size) = strip_exif_and_save(&bytes, &target_path) {
            let _ = sqlx::query!(
                r#"
                INSERT INTO aduan_foto (aduan_id, jenis, storage_key, ukuran, mime, diunggah_oleh)
                VALUES ($1, 'laporan', $2, $3, 'image/jpeg', $4)
                "#,
                aduan_id,
                storage_key,
                size as i32,
                cu.user.id
            )
            .execute(&mut *tx)
            .await;
        }
    }

    // Catat ke audit log secara atomik
    let _ = sqlx::query!(
        r#"
        INSERT INTO audit_log (user_id, role, aksi, entitas, entitas_id, nilai_baru)
        VALUES ($1, 'warga', 'KIRIM_ADUAN', 'aduan', $2, $3)
        "#,
        cu.user.id,
        aduan_id,
        serde_json::json!({ "no_aduan": no_aduan, "judul": judul })
    )
    .execute(&mut *tx)
    .await;

    let _ = tx.commit().await;

    Redirect::to("/warga?sukses=aduan_terkirim").into_response()
}

