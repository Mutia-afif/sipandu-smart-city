# Multi-Stage Production Dockerfile for SIPANDU Smart City
# Step 10 UTS PPSI - Deployment Architecture
# Mutia Afif Ramadhani (24311124) | Dr. Erliyan Redy Susanto, M.Kom

# 1. Builder Stage
FROM rust:1.78-slim-bookworm AS builder

WORKDIR /app

# Install dependensi sistem yang dibutuhkan untuk kompilasi C / libssl / pkg-config
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Salin manifest dependensi terlebih dahulu untuk layer caching
COPY Cargo.toml Cargo.lock* ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release && rm -rf src

# Salin source code lengkap & aset template
COPY src/ ./src/
COPY templates/ ./templates/
COPY migrations/ ./migrations/

# Sentuh main.rs untuk memaksa kompilasi release penuh
RUN touch src/main.rs && cargo build --release

# 2. Runtime Stage (Minimal Debian Slim)
FROM debian:bookworm-slim AS runtime

WORKDIR /app

# Install runtime dependencies (OpenSSL & CA Certificates)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Buat pengguna non-root demi prinsip Least Privilege
RUN useradd -m -u 1001 -s /bin/bash appuser

# Salin binary dari builder
COPY --from=builder /app/target/release/sipandu-smart-city /app/sipandu-smart-city

# Salin aset statis, template, dan migrasi
COPY static/ /app/static/
COPY templates/ /app/templates/
COPY migrations/ /app/migrations/
COPY .env.example /app/.env

# Buat folder uploads dengan izin write untuk appuser
RUN mkdir -p /app/static/uploads && chown -R appuser:appuser /app

USER appuser

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["/app/sipandu-smart-city"]

