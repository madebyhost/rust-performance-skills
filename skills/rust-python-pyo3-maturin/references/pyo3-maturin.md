# PyO3 And Maturin Reference

## Performance Principles

- Move coarse-grained CPU work into Rust; avoid crossing the Python/Rust boundary per item.
- Prefer Python-native borrowed types when conversion cost dominates.
- Convert to Rust types when native-speed processing and `Python::detach` outweigh conversion cost.
- Use `cast` over broad `extract` chains when checking concrete Python types and ignoring conversion errors.
- Release interpreter attachment with `Python::detach` for long-running CPU work.

## Packaging

- Use `maturin develop -r` for local optimized extension testing.
- Use `maturin build -r` for release wheels.
- Use `abi3` for broad CPython compatibility when PyO3 features allow it.
- Consider `abi3t` and free-threaded builds for Python versions that support them.
- Keep module names aligned between `[package]`, `[lib]`, and `pyproject.toml`.

## Free-Threading

- Audit `#[pyclass]` for `Send` and `Sync`.
- Do not rely on the historical GIL as a synchronization guarantee.
- Use `#[pymodule(gil_used = false)]` only when exposed data structures are thread-safe.

## Verification

- Benchmark the Python caller, not only Rust internals.
- Compare pure Python, Rust extension, and boundary batching variants.
- Test wheel import across targeted Python versions.
