use askama::Template;
use axum::{
    extract::{Query, State},
    response::{Html, IntoResponse, Json, Response},
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::state::AppState;

#[derive(Template)]
#[template(path = "warga/duplicate_banner.html")]
pub struct DuplicateBannerTemplate {
    pub is_duplicate: bool,
    pub duplicate_id: String,
    pub duplicate_no: String,
    pub duplicate_title: String,
}

#[derive(Deserialize)]
pub struct DuplicateCheckQuery {
    pub category_id: Option<String>,
    pub latitude: Option<f64>,
    pub longitude: Option<f64>,
}

#[derive(Serialize)]
pub struct MapPoint {
    pub id: String,
    pub no_aduan: String,
    pub judul: String,
    pub status: String,
    pub prioritas: String,
    pub lat: f64,
    pub lng: f64,
}

/// Endpoint HTMX untuk mendeteksi duplikasi laporan dalam radius 50 meter menggunakan PostGIS
pub async fn check_duplicate(
    State(state): State<AppState>,
    Query(query): Query<DuplicateCheckQuery>,
) -> Response {
    let cat_id = query.category_id.and_then(|c| Uuid::parse_str(&c).ok());
    let lat = query.latitude;
    let lng = query.longitude;

    if let (Some(cat), Some(lat), Some(lng)) = (cat_id, lat, lng) {
        let duplicate = sqlx::query!(
            r#"
            SELECT id, no_aduan, judul
            FROM aduan
            WHERE category_id = $1 
              AND status IN ('pending', 'verified', 'in_progress')
              AND ST_DWithin(geom::geography, ST_SetSRID(ST_Point($2, $3), 4326)::geography, 50)
            LIMIT 1
            "#,
            cat,
            lng,
            lat
        )
        .fetch_optional(&state.db)
        .await
        .ok()
        .flatten();

        if let Some(dup) = duplicate {
            return Html(
                DuplicateBannerTemplate {
                    is_duplicate: true,
                    duplicate_id: dup.id.to_string(),
                    duplicate_no: dup.no_aduan,
                    duplicate_title: dup.judul,
                }
                .render()
                .unwrap(),
            )
            .into_response();
        }
    }

    Html(
        DuplicateBannerTemplate {
            is_duplicate: false,
            duplicate_id: String::new(),
            duplicate_no: String::new(),
            duplicate_title: String::new(),
        }
        .render()
        .unwrap(),
    )
    .into_response()
}

/// Endpoint API JSON untuk peta sebaran aduan Leaflet
pub async fn get_map_points(State(state): State<AppState>) -> Json<Vec<MapPoint>> {
    let rows = sqlx::query!(
        r#"
        SELECT 
            id, no_aduan, judul,
            status as "status: _",
            prioritas as "prioritas: _",
            ST_Y(geom::geometry) as lat,
            ST_X(geom::geometry) as lng
        FROM aduan
        ORDER BY created_at DESC
        LIMIT 200
        "#
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let points = rows
        .into_iter()
        .map(|r| MapPoint {
            id: r.id.to_string(),
            no_aduan: r.no_aduan,
            judul: r.judul,
            status: r.status.to_string(),
            prioritas: r.prioritas.to_string(),
            lat: r.lat.unwrap_or(-5.4292),
            lng: r.lng.unwrap_or(105.2611),
        })
        .collect();

    Json(points)
}

#[derive(Template)]
#[template(path = "errors/404.html")]
pub struct NotFoundTemplate;

#[derive(Template)]
#[template(path = "errors/500.html")]
pub struct InternalErrorTemplate;

pub async fn handle_404() -> impl IntoResponse {
    (
        axum::http::StatusCode::NOT_FOUND,
        Html(NotFoundTemplate.render().unwrap_or_else(|_| "404 Halaman Tidak Ditemukan".to_string())),
    )
}


