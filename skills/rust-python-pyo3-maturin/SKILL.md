---
name: rust-python-pyo3-maturin
description: "Use when accelerating Python with Rust or building Python extension modules using PyO3, maturin, setuptools-rust, abi3/abi3t, free-threaded Python, GIL management, Python::detach, Rayon, type conversions, wheels, stubs, and Rust/Python API boundaries."
---

# Rust Python PyO3 Maturin

Use this skill when Rust is used to speed up Python or expose Rust libraries to Python. Load `references/pyo3-maturin.md` for detailed guidance.

## Workflow

1. Identify the Python bottleneck and whether Rust can reduce algorithmic cost, CPU time, memory pressure, or boundary crossings.
2. Choose API granularity: batch work across the Python/Rust boundary, not per item.
3. Choose packaging: maturin for new extension modules; setuptools-rust when integrating into an existing package layout.
4. Choose concurrency: use `Python::detach` for CPU-heavy Rust work and audit free-threaded Python support.
5. Benchmark from Python and Rust.

## Output

Include boundary cost, conversion strategy, GIL/free-threading stance, wheel targets, release build command, and benchmark plan.
