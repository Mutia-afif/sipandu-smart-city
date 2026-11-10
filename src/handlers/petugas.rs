use askama::Template;
use axum::{
    extract::{Multipart, Query, State},
    response::{Html, IntoResponse, Redirect, Response},
    Extension, Form,
};
use chrono::Utc;
use serde::Deserialize;
use std::path::Path;
use uuid::Uuid;

use crate::{
    middleware::{check_role, CurrentUser},
    models::{AduanStatus, UserRole},
    state::AppState,
    utils::exif::strip_exif_and_save,
};

#[derive(Template)]
#[template(path = "petugas/index.html")]
pub struct PetugasPortalTemplate {
    pub petugas_nama: String,
    pub dinas_nama: String,
    pub count_total: i64,
    pub count_pending: i64,
    pub count_in_progress: i64,
    pub count_resolved: i64,
    pub task_list: Vec<PetugasTaskItem>,
}

pub struct PetugasTaskItem {
    pub id: String,
    pub no_aduan: String,
    pub judul: String,
    pub deskripsi: String,
    pub alamat_teks: String,
    pub status: String,
    pub prioritas: String,
    pub version: i32,
    pub jarak_meter: i64,
}

#[derive(Deserialize)]
pub struct PetugasLocationQuery {
    pub lat: Option<f64>,
    pub lng: Option<f64>,
}

#[derive(Deserialize)]
pub struct TakeTaskForm {
    pub aduan_id: String,
    pub version: i32,
}

pub async fn show_petugas_portal(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    Query(query): Query<PetugasLocationQuery>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    if let Err(res) = check_role(Some(&cu), UserRole::Petugas) {
        return res;
    }

    let dinas_id = match cu.user.dinas_id {
        Some(id) => id,
        None => return Redirect::to("/login").into_response(),
    };

    let dinas_nama = sqlx::query_scalar!("SELECT nama FROM dinas WHERE id = $1", dinas_id)
        .fetch_one(&state.db)
        .await
        .unwrap_or_else(|_| "Dinas Teknis".to_string());

    let ref_lat = query.lat.unwrap_or(-5.4292);
    let ref_lng = query.lng.unwrap_or(105.2611);

    // Kueri tugas dinas diurutkan Prioritas (Tinggi > Sedang > Rendah) lalu Jarak PostGIS ST_Distance
    let rows = sqlx::query!(
        r#"
        SELECT 
            a.id, a.no_aduan, a.judul, a.deskripsi, a.alamat_teks,
            a.status as "status: AduanStatus",
            a.prioritas as "prioritas: _",
            a.version,
            ROUND(ST_Distance(a.geom::geography, ST_SetSRID(ST_Point($2, $3), 4326)::geography))::bigint as jarak_meter
        FROM aduan a
        WHERE a.dinas_id = $1 AND a.status IN ('verified', 'in_progress')
        ORDER BY 
            CASE a.prioritas 
                WHEN 'tinggi' THEN 1 
                WHEN 'sedang' THEN 2 
                ELSE 3 
            END ASC,
            jarak_meter ASC
        "#,
        dinas_id,
        ref_lng,
        ref_lat
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let mut task_list = Vec::new();
    for r in rows {
        task_list.push(PetugasTaskItem {
            id: r.id.to_string(),
            no_aduan: r.no_aduan,
            judul: r.judul,
            deskripsi: r.deskripsi,
            alamat_teks: r.alamat_teks.unwrap_or_default(),
            status: r.status.to_string(),
            prioritas: r.prioritas.to_string(),
            version: r.version,
            jarak_meter: r.jarak_meter.unwrap_or(0),
        });
    }

    // Hitung counter dinas
    let count_total = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM aduan WHERE dinas_id = $1",
        dinas_id
    )
    .fetch_one(&state.db)
    .await
    .unwrap_or(Some(0))
    .unwrap_or(0);

    let count_pending = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM aduan WHERE dinas_id = $1 AND status = 'verified'",
        dinas_id
    )
    .fetch_one(&state.db)
    .await
    .unwrap_or(Some(0))
    .unwrap_or(0);

    let count_in_progress = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM aduan WHERE dinas_id = $1 AND status = 'in_progress'",
        dinas_id
    )
    .fetch_one(&state.db)
    .await
    .unwrap_or(Some(0))
    .unwrap_or(0);

    let count_resolved = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM aduan WHERE dinas_id = $1 AND status = 'resolved'",
        dinas_id
    )
    .fetch_one(&state.db)
    .await
    .unwrap_or(Some(0))
    .unwrap_or(0);

    Html(
        PetugasPortalTemplate {
            petugas_nama: cu.user.nama.clone(),
            dinas_nama,
            count_total,
            count_pending,
            count_in_progress,
            count_resolved,
            task_list,
        }
        .render()
        .unwrap(),
    )
    .into_response()
}

pub async fn take_task(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    Form(form): Form<TakeTaskForm>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    let aduan_id = match Uuid::parse_str(&form.aduan_id) {
        Ok(id) => id,
        Err(_) => return Redirect::to("/petugas").into_response(),
    };

    let mut tx = match state.db.begin().await {
        Ok(t) => t,
        Err(_) => return Redirect::to("/petugas").into_response(),
    };

    // Update status ke in_progress dengan Optimistic Locking
    let res = sqlx::query!(
        r#"
        UPDATE aduan
        SET status = 'in_progress', version = version + 1, updated_at = NOW()
        WHERE id = $1 AND version = $2 AND status = 'verified'
        "#,
        aduan_id,
        form.version
    )
    .execute(&mut *tx)
    .await;

    if let Ok(result) = res {
        if result.rows_affected() > 0 {
            let _ = sqlx::query!(
                r#"
                INSERT INTO aduan_logs (aduan_id, changed_by_user_id, status_lama, status_baru, catatan)
                VALUES ($1, $2, 'verified', 'in_progress', 'Petugas mulai menangani di lapangan')
                "#,
                aduan_id,
                cu.user.id
            )
            .execute(&mut *tx)
            .await;

            let _ = sqlx::query!(
                r#"
                INSERT INTO audit_log (user_id, role, aksi, entitas, entitas_id)
                VALUES ($1, 'petugas', 'MULAI_PENANGANAN', 'aduan', $2)
                "#,
                cu.user.id,
                aduan_id
            )
            .execute(&mut *tx)
            .await;

            let _ = tx.commit().await;
            return Redirect::to("/petugas?sukses=tugas_diambil").into_response();
        } else {
            let _ = tx.rollback().await;
            return Redirect::to("/petugas?error=konflik_data").into_response();
        }
    }

    Redirect::to("/petugas?error=gagal_update").into_response()
}

pub async fn resolve_task(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    mut multipart: Multipart,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    let mut aduan_id: Option<Uuid> = None;
    let mut version: Option<i32> = None;
    let mut catatan_teknis = String::new();
    let mut proof_photo_bytes: Option<Vec<u8>> = None;

    while let Ok(Some(field)) = multipart.next_field().await {
        let name = field.name().unwrap_or_default().to_string();
        if name == "aduan_id" {
            if let Ok(text) = field.text().await {
                aduan_id = Uuid::parse_str(&text).ok();
            }
        } else if name == "version" {
            if let Ok(text) = field.text().await {
                version = text.parse().ok();
            }
        } else if name == "catatan_teknis" {
            catatan_teknis = field.text().await.unwrap_or_default();
        } else if name == "foto_bukti" {
            if let Ok(bytes) = field.bytes().await {
                if !bytes.is_empty() {
                    proof_photo_bytes = Some(bytes.to_vec());
                }
            }
        }
    }

    let (aid, ver, photo_bytes) = match (aduan_id, version, proof_photo_bytes) {
        (Some(a), Some(v), Some(p)) if !p.is_empty() => {
            // Validasi ukuran batas maksimal 5 MB
            if p.len() > 5 * 1024 * 1024 {
                return Redirect::to("/petugas?error=foto_terlalu_besar").into_response();
            }
            // Validasi Magic Bytes konten biner (Mencegah Web Shell & Polyglot File)
            if !infer::is_image(&p) {
                return Redirect::to("/petugas?error=file_bukan_gambar").into_response();
            }
            // Validasi batas panjang catatan teknis
            if catatan_teknis.len() > 3000 {
                return Redirect::to("/petugas?error=input_tidak_valid").into_response();
            }
            (a, v, p)
        },
        _ => return Redirect::to("/petugas?error=foto_bukti_wajib").into_response(), // Wajib ada foto bukti
    };

    let mut tx = match state.db.begin().await {
        Ok(t) => t,
        Err(_) => return Redirect::to("/petugas").into_response(),
    };

    // Update status ke resolved dengan Optimistic Locking
    let update_res = sqlx::query!(
        r#"
        UPDATE aduan
        SET status = 'resolved', catatan_penanganan = $1, version = version + 1, updated_at = NOW()
        WHERE id = $2 AND version = $3 AND status = 'in_progress'
        "#,
        catatan_teknis,
        aid,
        ver
    )
    .execute(&mut *tx)
    .await;

    if let Ok(result) = update_res {
        if result.rows_affected() > 0 {
            // Simpan foto bukti penanganan
            let _ = std::fs::create_dir_all(&state.config.upload_dir);
            let filename = format!("bukti_{}_{}.jpg", aid, Utc::now().timestamp());
            let target_path = Path::new(&state.config.upload_dir).join(&filename);
            let storage_key = format!("/static/uploads/{}", filename);

            if let Ok(size) = strip_exif_and_save(&photo_bytes, &target_path) {
                let _ = sqlx::query!(
                    r#"
                    INSERT INTO aduan_foto (aduan_id, jenis, storage_key, ukuran, mime, diunggah_oleh)
                    VALUES ($1, 'penanganan', $2, $3, 'image/jpeg', $4)
                    "#,
                    aid,
                    storage_key,
                    size as i32,
                    cu.user.id
                )
                .execute(&mut *tx)
                .await;
            }

            let _ = sqlx::query!(
                r#"
                INSERT INTO aduan_logs (aduan_id, changed_by_user_id, status_lama, status_baru, catatan)
                VALUES ($1, $2, 'in_progress', 'resolved', $3)
                "#,
                aid,
                cu.user.id,
                catatan_teknis
            )
            .execute(&mut *tx)
            .await;

            let _ = sqlx::query!(
                r#"
                INSERT INTO audit_log (user_id, role, aksi, entitas, entitas_id, nilai_baru)
                VALUES ($1, 'petugas', 'SELESAIKAN_ADUAN', 'aduan', $2, $3)
                "#,
                cu.user.id,
                aid,
                serde_json::json!({ "catatan": catatan_teknis })
            )
            .execute(&mut *tx)
            .await;

            let _ = tx.commit().await;
            return Redirect::to("/petugas?sukses=tugas_selesai").into_response();
        } else {
            let _ = tx.rollback().await;
            return Redirect::to("/petugas?error=konflik_data").into_response();
        }
    }

    Redirect::to("/petugas?error=gagal_update").into_response()
}

