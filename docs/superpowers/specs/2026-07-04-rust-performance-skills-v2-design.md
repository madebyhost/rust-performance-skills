# Rust Performance Skills V2 Design

## Goal

Turn `rust-performance-skills` from a compact single-skill plugin into a multi-skill Rust performance engineering distribution for Codex, Claude Code, and other coding agents.

## Architecture

Use a compact router skill plus focused specialist skills. The router keeps invocation cheap and routes agents to domain-specific playbooks only when the task needs them. Specialist skills cover code quality, performance, async/concurrency, HFT/low-latency engineering, PyO3/maturin, Wasm, FFI/bindings, unsafe soundness, architecture patterns, and code review.

Keep the repository skill-first. Add deterministic scripts only where they improve reliability: distribution validation and static project audit. Keep MCP as a roadmap until there are stable deterministic operations worth exposing.

## Components

- `skills/rust-performance-engineering`: primary router and general workflow.
- `skills/rust-code-quality`: idiomatic Rust, API design, clippy, docs, tests, crate hygiene.
- `skills/rust-performance-core`: measurement, Cargo profiles, allocations, cache, bounds checks, data layout.
- `skills/rust-async-concurrency`: Tokio, Rayon, channels, backpressure, scheduling, Send/Sync.
- `skills/rust-low-latency-hft`: ring buffers, multicast, disruptor pattern, CPU/cache/NUMA/network tuning.
- `skills/rust-python-pyo3-maturin`: Rust acceleration for Python, PyO3, maturin, GIL/free-threading, wheel design.
- `skills/rust-wasm-engineering`: wasm-bindgen, wasm-pack-style pipelines, JS boundary costs, code size and runtime performance.
- `skills/rust-ffi-bindings`: C/C++/Node/Python interop, bindgen/cbindgen/napi-rs, ABI safety.
- `skills/rust-unsafe-soundness`: unsafe policy, invariants, Miri/sanitizers, safe wrappers.
- `skills/rust-architecture-patterns`: onion, hexagonal, DDD, ECS, actor, pipeline, disruptor, hot-path exception rules.
- `skills/rust-review-auditor`: Rust PR review workflow for correctness, performance, safety, and maintainability.
- `scripts/rust_project_audit.py`: deterministic static audit for Rust repository signals.
- `scripts/validate_distribution.py`: stronger validator for all skill folders and docs.

## Source Basis

The guidance is based on primary or stable sources: The Rust Performance Book, Cargo profiles, Rust API Guidelines, Clippy documentation, Rustonomicon/FFI material, PyO3 and maturin docs, and Rust/Wasm and wasm-bindgen documentation. The plugin should summarize and operationalize these sources, not copy them.

## Rules

- Do not make low-level tricks the default. Require measurement and explicit constraints.
- Prefer safe, idiomatic Rust until a measured bottleneck justifies more complexity.
- Treat Python and Wasm bindings as boundary-design problems, not just packaging steps.
- Treat `unsafe` and FFI as soundness-critical, not performance shortcuts.
- Keep skills progressively disclosed: frontmatter and `SKILL.md` should route to focused references rather than loading every detail at once.

## Validation

The v2 is complete when:

- all skills have valid frontmatter and `agents/openai.yaml`;
- all router references point to existing files;
- distribution validation passes;
- the audit script has tests covering missing Cargo files, Cargo profile detection, PyO3/maturin detection, Wasm detection, and unsafe/HFT signal detection;
- GitHub CI passes after push.
