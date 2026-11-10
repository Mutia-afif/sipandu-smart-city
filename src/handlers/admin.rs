use askama::Template;
use axum::{
    extract::State,
    response::{Html, IntoResponse, Redirect, Response},
    Extension, Form,
};
use serde::Deserialize;
use uuid::Uuid;

use crate::{
    middleware::{check_role, CurrentUser},
    models::{AduanStatus, PrioritasLevel, UserRole},
    state::AppState,
};

#[derive(Template)]
#[template(path = "admin/index.html")]
pub struct AdminPortalTemplate {
    pub admin_nama: String,
    pub kpi_total: i64,
    pub kpi_pending: i64,
    pub kpi_in_progress: i64,
    pub kpi_resolved: i64,
    pub pending_tickets: Vec<PendingTicketItem>,
    pub dinas_list: Vec<DinasOption>,
    pub audit_logs: Vec<AuditLogItem>,
}

pub struct PendingTicketItem {
    pub id: String,
    pub no_aduan: String,
    pub judul: String,
    pub deskripsi: String,
    pub pelapor_nama: String,
    pub kategori_nama: String,
    pub dinas_default_id: String,
    pub version: i32,
    pub created_at: String,
    pub lat: f64,
    pub lng: f64,
}

pub struct DinasOption {
    pub id: String,
    pub nama: String,
}

pub struct AuditLogItem {
    pub waktu: String,
    pub role: String,
    pub aksi: String,
    pub entitas: String,
    pub deskripsi: String,
    pub ip: String,
}

#[derive(Deserialize)]
pub struct VerifyTicketForm {
    pub aduan_id: String,
    pub version: i32,
    pub dinas_id: String,
    pub prioritas: String,
}

#[derive(Deserialize)]
pub struct RejectTicketForm {
    pub aduan_id: String,
    pub version: i32,
    pub alasan_penolakan: String,
}

pub async fn show_admin_portal(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    if let Err(res) = check_role(Some(&cu), UserRole::Admin) {
        return res;
    }

    // 4 KPI Utama
    let kpi_total = sqlx::query_scalar!("SELECT COUNT(*) FROM aduan")
        .fetch_one(&state.db)
        .await
        .unwrap_or(Some(0))
        .unwrap_or(0);

    let kpi_pending = sqlx::query_scalar!("SELECT COUNT(*) FROM aduan WHERE status = 'pending'")
        .fetch_one(&state.db)
        .await
        .unwrap_or(Some(0))
        .unwrap_or(0);

    let kpi_in_progress = sqlx::query_scalar!("SELECT COUNT(*) FROM aduan WHERE status = 'in_progress'")
        .fetch_one(&state.db)
        .await
        .unwrap_or(Some(0))
        .unwrap_or(0);

    let kpi_resolved = sqlx::query_scalar!("SELECT COUNT(*) FROM aduan WHERE status = 'resolved'")
        .fetch_one(&state.db)
        .await
        .unwrap_or(Some(0))
        .unwrap_or(0);

    // Antrean tiket pending
    let pending_rows = sqlx::query!(
        r#"
        SELECT 
            a.id, a.no_aduan, a.judul, a.deskripsi, a.version, a.created_at,
            ST_Y(a.geom::geometry) as lat,
            ST_X(a.geom::geometry) as lng,
            u.nama as pelapor_nama,
            c.nama_kategori as kategori_nama,
            c.dinas_id as dinas_default_id
        FROM aduan a
        JOIN users u ON a.user_id = u.id
        JOIN categories c ON a.category_id = c.id
        WHERE a.status = 'pending'
        ORDER BY a.created_at ASC
        "#
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let mut pending_tickets = Vec::new();
    for r in pending_rows {
        pending_tickets.push(PendingTicketItem {
            id: r.id.to_string(),
            no_aduan: r.no_aduan,
            judul: r.judul,
            deskripsi: r.deskripsi,
            pelapor_nama: r.pelapor_nama,
            kategori_nama: r.kategori_nama,
            dinas_default_id: r.dinas_default_id.to_string(),
            version: r.version,
            created_at: r.created_at.format("%d/%m %H:%M").to_string(),
            lat: r.lat.unwrap_or(-5.4292),
            lng: r.lng.unwrap_or(105.2611),
        });
    }

    // Daftar master dinas
    let dinas_rows = sqlx::query!("SELECT id, nama FROM dinas WHERE is_active = TRUE ORDER BY nama ASC")
        .fetch_all(&state.db)
        .await
        .unwrap_or_default();

    let dinas_list = dinas_rows
        .into_iter()
        .map(|d| DinasOption {
            id: d.id.to_string(),
            nama: d.nama,
        })
        .collect();

    // Audit logs
    let audit_rows = sqlx::query!(
        r#"
        SELECT waktu, role, aksi, entitas, nilai_baru, ip
        FROM audit_log
        ORDER BY waktu DESC
        LIMIT 15
        "#
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let mut audit_logs = Vec::new();
    for a in audit_rows {
        let deskripsi = a.nilai_baru.map(|v| v.to_string()).unwrap_or_default();
        audit_logs.push(AuditLogItem {
            waktu: a.waktu.format("%d %b %H:%M:%S").to_string(),
            role: a.role,
            aksi: a.aksi,
            entitas: a.entitas,
            deskripsi,
            ip: a.ip.unwrap_or_else(|| "127.0.0.1".to_string()),
        });
    }

    Html(
        AdminPortalTemplate {
            admin_nama: cu.user.nama.clone(),
            kpi_total,
            kpi_pending,
            kpi_in_progress,
            kpi_resolved,
            pending_tickets,
            dinas_list,
            audit_logs,
        }
        .render()
        .unwrap(),
    )
    .into_response()
}

pub async fn verify_ticket(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    Form(form): Form<VerifyTicketForm>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    let aid = match Uuid::parse_str(&form.aduan_id) {
        Ok(id) => id,
        Err(_) => return Redirect::to("/admin").into_response(),
    };

    let dinas_id = match Uuid::parse_str(&form.dinas_id) {
        Ok(id) => id,
        Err(_) => return Redirect::to("/admin").into_response(),
    };

    let prioritas = match form.prioritas.as_str() {
        "tinggi" => PrioritasLevel::Tinggi,
        "rendah" => PrioritasLevel::Rendah,
        _ => PrioritasLevel::Sedang,
    };

    let mut tx = match state.db.begin().await {
        Ok(t) => t,
        Err(_) => return Redirect::to("/admin").into_response(),
    };

    // Update status ke verified dengan Optimistic Locking
    let update_res = sqlx::query!(
        r#"
        UPDATE aduan
        SET status = 'verified', dinas_id = $1, prioritas = $2, version = version + 1, updated_at = NOW()
        WHERE id = $3 AND version = $4 AND status = 'pending'
        "#,
        dinas_id,
        prioritas as PrioritasLevel,
        aid,
        form.version
    )
    .execute(&mut *tx)
    .await;

    if let Ok(result) = update_res {
        if result.rows_affected() > 0 {
            let _ = sqlx::query!(
                r#"
                INSERT INTO aduan_logs (aduan_id, changed_by_user_id, status_lama, status_baru, catatan)
                VALUES ($1, $2, 'pending', 'verified', 'Diverifikasi oleh Admin Pemda')
                "#,
                aid,
                cu.user.id
            )
            .execute(&mut *tx)
            .await;

            let _ = sqlx::query!(
                r#"
                INSERT INTO audit_log (user_id, role, aksi, entitas, entitas_id, nilai_baru)
                VALUES ($1, 'admin', 'VERIFIKASI_ADUAN', 'aduan', $2, $3)
                "#,
                cu.user.id,
                aid,
                serde_json::json!({ "dinas_id": dinas_id, "prioritas": prioritas.to_string() })
            )
            .execute(&mut *tx)
            .await;

            let _ = tx.commit().await;
            return Redirect::to("/admin?sukses=verifikasi_berhasil").into_response();
        } else {
            let _ = tx.rollback().await;
            return Redirect::to("/admin?error=konflik_data").into_response();
        }
    }

    Redirect::to("/admin?error=gagal_update").into_response()
}

pub async fn reject_ticket(
    State(state): State<AppState>,
    current_user: Option<Extension<CurrentUser>>,
    Form(form): Form<RejectTicketForm>,
) -> Response {
    let cu = match current_user {
        Some(Extension(u)) => u,
        None => return Redirect::to("/login").into_response(),
    };

    let aid = match Uuid::parse_str(&form.aduan_id) {
        Ok(id) => id,
        Err(_) => return Redirect::to("/admin").into_response(),
    };

    if form.alasan_penolakan.trim().is_empty() {
        return Redirect::to("/admin?error=alasan_wajib").into_response(); // Alasan penolakan wajib diisi
    }

    if form.alasan_penolakan.len() > 1000 {
        return Redirect::to("/admin?error=input_tidak_valid").into_response();
    }

    let mut tx = match state.db.begin().await {
        Ok(t) => t,
        Err(_) => return Redirect::to("/admin").into_response(),
    };

    let update_res = sqlx::query!(
        r#"
        UPDATE aduan
        SET status = 'rejected', alasan_penolakan = $1, version = version + 1, updated_at = NOW()
        WHERE id = $2 AND version = $3 AND status = 'pending'
        "#,
        form.alasan_penolakan,
        aid,
        form.version
    )
    .execute(&mut *tx)
    .await;

    if let Ok(result) = update_res {
        if result.rows_affected() > 0 {
            let _ = sqlx::query!(
                r#"
                INSERT INTO aduan_logs (aduan_id, changed_by_user_id, status_lama, status_baru, catatan)
                VALUES ($1, $2, 'pending', 'rejected', $3)
                "#,
                aid,
                cu.user.id,
                form.alasan_penolakan
            )
            .execute(&mut *tx)
            .await;

            let _ = sqlx::query!(
                r#"
                INSERT INTO audit_log (user_id, role, aksi, entitas, entitas_id, nilai_baru)
                VALUES ($1, 'admin', 'TOLAK_ADUAN', 'aduan', $2, $3)
                "#,
                cu.user.id,
                aid,
                serde_json::json!({ "alasan": form.alasan_penolakan })
            )
            .execute(&mut *tx)
            .await;

            let _ = tx.commit().await;
            return Redirect::to("/admin?sukses=tiket_ditolak").into_response();
        } else {
            let _ = tx.rollback().await;
            return Redirect::to("/admin?error=konflik_data").into_response();
        }
    }

    Redirect::to("/admin?error=gagal_update").into_response()
}

