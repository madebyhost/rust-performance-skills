# Eval: PyO3 Optimization

Ask the agent to speed up a Python loop with Rust while preserving packaging quality.

Expected behavior:

- Loads `rust-python-pyo3-maturin`, `rust-performance-core`, and `rust-crate-release-engineering`.
- Avoids crossing the Python/Rust boundary per item in a hot loop.
- Mentions conversion cost, GIL/free-threading behavior, wheel build, import tests, and benchmark design.
- Recommends `maturin build --release` and a Python caller benchmark.
