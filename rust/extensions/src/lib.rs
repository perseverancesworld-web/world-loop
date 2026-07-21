use pyo3::prelude::*;

#[pyfunction]
fn parallel_evaluate(genomes: Vec<String>) -> Vec<f64> {
    // Placeholder for high-perf fitness evaluation
    genomes.iter().map(|_| rand::random::<f64>() * 100.0).collect()
}

#[pymodule]
fn worldloop_extensions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parallel_evaluate, m)?)?;
    Ok(())
}