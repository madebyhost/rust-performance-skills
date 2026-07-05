# pyo3-release-gil-hotloop

## id
pyo3-release-gil-hotloop

## severity
high

## trigger
PyO3 extension functions that perform CPU-bound loops, parsing, compression, graph algorithms, or batch transforms.

## bad
```rust
#[pyfunction]
fn score_rows(rows: Vec<Row>) -> PyResult<Vec<f64>> {
    Ok(rows.iter().map(score).collect())
}
```

## good
```rust
#[pyfunction]
fn score_rows(py: Python<'_>, rows: Vec<Row>) -> PyResult<Vec<f64>> {
    py.detach(|| Ok(rows.par_iter().map(score).collect()))
}
```

## when
Use when work is pure Rust, CPU-bound, and does not touch Python objects inside the hot loop.

## when_not
Do not release the GIL around code that calls Python APIs or holds Python object references without correct ownership.

## verification
Measure Python/Rust boundary overhead, GIL hold time, batch size sensitivity, wheel import tests, and threaded contention.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- PyO3 guide: https://pyo3.rs/
- maturin: https://www.maturin.rs/

## related_rules
- conc-rayon-par-iter
- mem-zero-copy
- err-thiserror-lib
