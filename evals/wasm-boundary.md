# Eval: Wasm Boundary

Ask the agent to review a Rust/Wasm package that copies large buffers across the JS boundary.

Expected behavior:

- Loads `rust-wasm-engineering`, `rust-performance-core`, and `rust-testing-verification`.
- Focuses on boundary crossing, memory transfer, generated JS glue, bundle size, and browser/node targets.
- Recommends `wasm-pack test`, `wasm-pack build --release`, and size/perf measurement.
