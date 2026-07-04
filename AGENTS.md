# Agent Instructions

When working on Rust code in this repository or in a project that installed this repository, use `$rust-performance-engineering` for performance-sensitive Rust design, implementation, or review tasks. Load specialist skills for PyO3/maturin, Wasm, FFI, unsafe, async, HFT, architecture, or review work when the router indicates them.

Always preserve the measurement-first workflow:

1. Identify latency, throughput, memory, and correctness constraints.
2. Inspect the actual Rust code, Cargo profiles, dependencies, runtime, and benchmarks.
3. Choose patterns from the skill references only when they fit the constraints.
4. Validate with tests, benchmarks, profiling, or targeted review evidence.

For repository orientation, run `python3 scripts/rust_project_audit.py . --json` when command execution is available.
