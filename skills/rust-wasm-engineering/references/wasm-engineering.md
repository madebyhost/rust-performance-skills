# Wasm Engineering Reference

## Boundary Design

- Batch data crossing JS/Wasm.
- Prefer typed arrays and shared buffers where practical.
- Avoid calling tiny Rust functions from JS in tight loops.
- Keep serialization formats explicit.

## Size

- Measure final `*_bg.wasm`, not raw compiler output before wasm-bindgen.
- Use `opt-level = "z"` or `"s"` only when size matters more than speed.
- Consider LTO, `panic = "abort"`, `strip`, and `wasm-opt`.
- Audit dependency features; browser bundles pay for what is linked.

## Performance

- Benchmark against optimized JS for the actual workload.
- Use web workers for CPU-heavy work that would block the UI.
- Avoid DOM access from hot Rust loops.
- Separate initialization cost from steady-state throughput.

## Verification

- Test in target browser/runtime.
- Measure load time, wasm size, JS glue size, and hot-path latency.
- Confirm TypeScript declarations and packaging shape.
