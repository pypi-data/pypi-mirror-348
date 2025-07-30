use pyo3::prelude::*;

/// Read QR code data from image file.
#[pyfunction]
#[pyo3(name = "read_qrcode")]
fn read_qr_function(filename: &str) -> PyResult<String> {
    let img = image::open(filename)
        .map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to open image: {}", e))
        })?
        .to_luma8();
    let mut img = rqrr::PreparedImage::prepare(img);
    let grids = img.detect_grids();
    if grids.len() != 1 {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Expected 1 QR code, found {}",
            grids.len()
        )));
    }
    let (_meta, content) = grids[0].decode().map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to decode QR code: {}", e))
    })?;
    Ok(content)
}

#[pymodule]
fn read_qrcode(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_qr_function, m)?)?;
    Ok(())
}
