use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct Dinas {
    pub id: Uuid,
    pub nama: String,
    pub deskripsi: Option<String>,
    pub is_active: bool,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct Category {
    pub id: Uuid,
    pub nama_kategori: String,
    pub dinas_id: Uuid,
    pub is_active: bool,
    pub created_at: DateTime<Utc>,
}

