use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct AuditLog {
    pub id: Uuid,
    pub user_id: Option<Uuid>,
    pub role: String,
    pub aksi: String,
    pub entitas: String,
    pub entitas_id: Option<Uuid>,
    pub nilai_lama: Option<serde_json::Value>,
    pub nilai_baru: Option<serde_json::Value>,
    pub ip: Option<String>,
    pub waktu: DateTime<Utc>,
}

