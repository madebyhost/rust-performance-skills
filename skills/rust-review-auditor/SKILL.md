---
name: rust-review-auditor
description: "Use for Rust code reviews, repository audits, PR reviews, and quality/performance assessments covering correctness, tests, API design, performance regressions, unsafe soundness, async/concurrency, FFI, PyO3/maturin, Wasm, and maintainability."
---

# Rust Review Auditor

Use this skill for review stance. Load `references/review-auditor.md` for checklists.

## Review Workflow

1. Inspect diff, `Cargo.toml`, tests, CI, and public API changes.
2. Classify risks: correctness, performance, safety, concurrency, API, packaging, docs.
3. Prioritize findings by severity and evidence.
4. Recommend exact verification commands.
5. Avoid style-only findings unless they affect maintainability or API quality.

Load `rust-ci-quality-gates` when CI is missing or weak, `rust-testing-verification` when evidence is thin, and `rust-crate-release-engineering` when public API, packaging, or release artifacts are affected.
Load `rust-ebpf-kernel-performance` for eBPF/kernel hooks, `rust-sbe-binary-codecs` for fixed binary wire formats, `rust-math-algorithms-performance` for graph, simulation, stochastic, SIMD, or numerical kernels, `rust-memory-simd-io-performance` for allocator, layout, SIMD, mmap, io_uring, NUMA, or huge-page hot paths, and `rust-api-type-system-design` for public API, typestate, serde, macro, trait, and feature-compatibility risks.

## Output

Lead with findings. Include file/line references when available. Then list test gaps and residual risks.
