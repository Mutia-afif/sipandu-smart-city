use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sqlx::Type;
use uuid::Uuid;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Type)]
#[sqlx(type_name = "aduan_status", rename_all = "snake_case")]
pub enum AduanStatus {
    Pending,
    Verified,
    Rejected,
    InProgress,
    Resolved,
}

impl std::fmt::Display for AduanStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AduanStatus::Pending => write!(f, "pending"),
            AduanStatus::Verified => write!(f, "verified"),
            AduanStatus::Rejected => write!(f, "rejected"),
            AduanStatus::InProgress => write!(f, "in_progress"),
            AduanStatus::Resolved => write!(f, "resolved"),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Type)]
#[sqlx(type_name = "prioritas_level", rename_all = "lowercase")]
pub enum PrioritasLevel {
    Rendah,
    Sedang,
    Tinggi,
}

impl std::fmt::Display for PrioritasLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PrioritasLevel::Rendah => write!(f, "rendah"),
            PrioritasLevel::Sedang => write!(f, "sedang"),
            PrioritasLevel::Tinggi => write!(f, "tinggi"),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct Aduan {
    pub id: Uuid,
    pub no_aduan: String,
    pub user_id: Uuid,
    pub category_id: Uuid,
    pub dinas_id: Option<Uuid>,
    pub judul: String,
    pub deskripsi: String,
    pub alamat_teks: Option<String>,
    pub status: AduanStatus,
    pub prioritas: PrioritasLevel,
    pub alasan_penolakan: Option<String>,
    pub catatan_penanganan: Option<String>,
    pub version: i32,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct AduanFoto {
    pub id: Uuid,
    pub aduan_id: Uuid,
    pub jenis: String, // 'laporan' atau 'penanganan'
    pub storage_key: String,
    pub ukuran: i32,
    pub mime: String,
    pub diunggah_oleh: Uuid,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct AduanLog {
    pub id: Uuid,
    pub aduan_id: Uuid,
    pub changed_by_user_id: Uuid,
    pub status_lama: Option<AduanStatus>,
    pub status_baru: AduanStatus,
    pub catatan: Option<String>,
    pub created_at: DateTime<Utc>,
}

