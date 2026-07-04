---
name: rust-testing-verification
description: "Use when adding, reviewing, or improving Rust tests and verification for crates, async code, unsafe code, parsers, protocols, PyO3 extensions, Wasm modules, low-latency systems, property tests, fuzzing, Miri, sanitizers, coverage, benchmarks, and regression suites."
---

# Rust Testing Verification

Use this skill when correctness evidence matters as much as implementation. Load `references/testing-verification.md` for the verification matrix.

## Workflow

1. Identify the risk class: public API, parser, unsafe, async scheduling, concurrency, FFI boundary, PyO3 boundary, Wasm boundary, or latency hot path.
2. Choose the cheapest test that can fail for the real risk.
3. Prefer deterministic unit and integration tests before fuzzing or benchmarks.
4. Add property, fuzz, Miri, sanitizer, or benchmark gates only when they exercise a risk not covered by normal tests.
5. Keep performance tests separate from correctness tests unless the latency budget is part of correctness.

## Defaults

- Unit tests for invariants and edge cases.
- Integration tests for public crate behavior and feature combinations.
- `proptest` or `quickcheck` for algebraic invariants, parsers, codecs, and state machines.
- `cargo fuzz` for untrusted byte input, binary protocols, market-data parsing, and FFI decoders.
- Miri for unsafe abstractions, pointer validity, aliasing assumptions, and parser logic that uses unsafe-adjacent APIs.
- `loom` for small concurrency algorithms where interleavings matter.
- Criterion or iai-callgrind for benchmarks with stable inputs and explicit budgets.

## Output

Return a verification plan with commands, fixtures, expected failure modes, and what evidence remains missing. Separate PR-fast checks from nightly or release checks.
