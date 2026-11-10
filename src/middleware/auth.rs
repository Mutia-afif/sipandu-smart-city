use axum::{
    extract::{Request, State},
    http::header,
    middleware::Next,
    response::{IntoResponse, Redirect, Response},
};
use chrono::Utc;
use crate::{models::{User, UserRole}, state::AppState};

#[derive(Clone, Debug)]
pub struct CurrentUser {
    pub user: User,
}

pub async fn auth_middleware(
    State(state): State<AppState>,
    mut req: Request,
    next: Next,
) -> Response {
    // Cari cookie session
    let session_id = req
        .headers()
        .get(header::COOKIE)
        .and_then(|val| val.to_str().ok())
        .and_then(|cookies| {
            cookies.split(';').find_map(|c| {
                let mut parts = c.trim().splitn(2, '=');
                let name = parts.next()?;
                let val = parts.next()?;
                if name == "sipandu_session" {
                    Some(val.to_string())
                } else {
                    None
                }
            })
        });

    if let Some(token) = session_id {
        let user = sqlx::query_as::<_, User>(
            r#"
            SELECT u.* FROM users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.id = $1 AND s.expires_at > $2 AND u.is_active = TRUE
            "#,
        )
        .bind(token)
        .bind(Utc::now())
        .fetch_optional(&state.db)
        .await
        .ok()
        .flatten();

        if let Some(user) = user {
            req.extensions_mut().insert(CurrentUser { user });
        }
    }

    next.run(req).await
}

/// Helper untuk memeriksa hak akses berdasarkan Role
pub fn check_role(current_user: Option<&CurrentUser>, required_role: UserRole) -> Result<(), Response> {
    match current_user {
        Some(cu) if cu.user.role == required_role => Ok(()),
        Some(_) => Err(Redirect::to("/login").into_response()),
        None => Err(Redirect::to("/login").into_response()),
    }
}

