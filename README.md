# Rust Performance Skills

Portable agent skills for building and reviewing high-performance Rust systems, Python extensions, Wasm modules, and FFI bindings.

This repository packages a Codex-compatible plugin and portable skills that can also be copied into Claude Code, other skill-aware coding agents, or project-local agent instructions. It focuses on real Rust performance work: measurement first, explicit latency budgets, allocation control, cache-aware data layout, async/runtime choices, concurrency, zero-copy, low-latency/HFT patterns, PyO3/maturin, WebAssembly, FFI, and unsafe soundness.

## What It Provides

- A Codex plugin manifest in `.codex-plugin/plugin.json`.
- A router skill at `skills/rust-performance-engineering`.
- Specialist skills for quality, core performance, async, HFT, PyO3/maturin, Wasm, FFI, unsafe, architecture, and reviews.
- Reference playbooks for zero-copy, async, HFT/low-latency, architecture, measurement, bindings, and review.
- A static audit helper at `scripts/rust_project_audit.py`.
- A quality-gate generator at `scripts/generate_quality_gates.py`.
- Reusable GitHub Actions templates under `templates/ci`.
- Evaluation prompts under `evals` for maintainers.
- Install notes for Codex, Claude Code, and generic agents.
- CI validation for plugin metadata, skill frontmatter, and reference links.
- A source map in [docs/sources.md](docs/sources.md) for maintainers.

## When To Use It

Use `$rust-performance-engineering` when an agent is asked to:

- design or review latency-sensitive Rust code;
- optimize async or multi-threaded Rust services;
- write zero-copy parsing, serialization, or networking code;
- build market-data, order-routing, HFT, telemetry, networking, or data-plane systems;
- speed up Python with PyO3/maturin;
- produce high-quality Rust/Wasm packages;
- design FFI or language bindings;
- choose between onion, hexagonal, ECS, actor, pipeline, or disruptor-style architecture;
- justify `unsafe`, lock-free data structures, CPU pinning, cache padding, or memory pools.

## Skills

- `rust-performance-engineering`: router and measurement-first workflow.
- `rust-code-quality`: idiomatic Rust, APIs, lints, tests, docs.
- `rust-performance-core`: profiling, allocations, Cargo profiles, cache, bounds checks.
- `rust-async-concurrency`: Tokio, Rayon, channels, backpressure, Send/Sync.
- `rust-low-latency-hft`: tail latency, ring buffers, multicast, CPU/cache/NUMA.
- `rust-python-pyo3-maturin`: PyO3, maturin, GIL/free-threading, wheels.
- `rust-wasm-engineering`: wasm-bindgen, JS boundary, code size, runtime performance.
- `rust-ffi-bindings`: bindgen, cbindgen, napi-rs, ABI and ownership boundaries.
- `rust-unsafe-soundness`: unsafe invariants, Miri/sanitizers, safe wrappers.
- `rust-architecture-patterns`: DDD, onion, hexagonal, ECS, actor, pipeline, disruptor.
- `rust-review-auditor`: Rust PR/repository review workflow.
- `rust-ci-quality-gates`: CI gates for Rust, PyO3, Wasm, unsafe, fuzzing, coverage, semver, and benchmarks.
- `rust-testing-verification`: verification strategy for tests, Miri, fuzzing, concurrency, bindings, and hot paths.
- `rust-crate-release-engineering`: crate release readiness, semver, packaging, wheels, Wasm artifacts, and FFI releases.

## Audit Helper

Run:

```bash
python3 scripts/rust_project_audit.py /path/to/rust/project
```

Use `--json` when another tool or agent should consume the output.

Generate suggested quality gates from an audit:

```bash
python3 scripts/rust_project_audit.py /path/to/rust/project --json > audit.json
python3 scripts/generate_quality_gates.py audit.json
```

## Install

One-liner for Codex, Claude Code, and project-local fallback:

```bash
curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh
```

Targets can be scoped:

```bash
RUST_PERF_SKILLS_TARGET=codex sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
RUST_PERF_SKILLS_TARGET=claude sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
RUST_PERF_SKILLS_TARGET=local sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

See:

- [Codex](docs/install/codex.md)
- [Claude Code and Anthropic-style agents](docs/install/claude.md)
- [Generic coding agents](docs/install/generic-agents.md)

## Design Principles

- Measure before optimizing.
- Treat latency budgets as contracts.
- Prefer mechanical sympathy over decorative abstractions.
- Keep zero-copy explicit and lifetime-safe.
- Isolate `unsafe` behind documented invariants and tests.
- Use async for concurrency, not as a blanket performance claim.
- Prefer bounded queues, backpressure, preallocation, and stable data layout in hot paths.

## MCP Status

The distribution remains skill-first. `.mcp.json` is present so the repository can grow an optional MCP server later without changing the plugin shape. A future MCP can expose deterministic checks such as Cargo profile inspection, dependency audits, perf checklist generation, and benchmark report parsing.

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Keep advice measurable, Rust-specific, and actionable for coding agents.

When changing technical guidance, prefer the primary sources listed in [docs/sources.md](docs/sources.md).

## License

MIT. See [LICENSE](LICENSE).
