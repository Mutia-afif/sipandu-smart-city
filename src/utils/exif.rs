use std::path::Path;
use image::io::Reader as ImageReader;
use std::io::Cursor;

/// Membersihkan EXIF metadata dari foto pelapor dengan decode & re-encode ulang gambar murni.
/// Hal ini melindungi privasi titik GPS asal warga (FR-02 & PRD 11.1).
pub fn strip_exif_and_save(bytes: &[u8], target_path: &Path) -> Result<usize, String> {
    let reader = ImageReader::new(Cursor::new(bytes))
        .with_guessed_format()
        .map_err(|e| format!("Format gambar tidak dikenali: {}", e))?;

    let img = reader
        .decode()
        .map_err(|e| format!("Gagal memproses gambar: {}", e))?;

    // Encode ulang ke format PNG atau JPEG murni tanpa EXIF headers
    img.save(target_path)
        .map_err(|e| format!("Gagal menyimpan file gambar: {}", e))?;

    Ok(bytes.len())
}

