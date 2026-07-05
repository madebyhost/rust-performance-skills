---
name: rust-expert-rulebook
description: "Use when writing, reviewing, refactoring, or optimizing Rust code and the agent needs concrete rule IDs, bad/good examples, exceptions, verification checks, or expert constraints rather than broad guidelines."
---

# Rust Expert Rulebook

Use this skill when the answer should be constrained by concrete Rust rules. The rulebook is intentionally heavy: it complements the specialist skills with explicit `bad`, `good`, `when`, `when_not`, and `verification` cards.

## Rulebook Workflow

1. Classify the work: correctness, API, async, concurrency, unsafe, memory, performance, HFT, SBE, eBPF, PyO3, Wasm, SIMD, NUMA, algorithms, I/O, release, or tests.
2. Select rules from `rules/index.json` using the code signals, file names, dependencies, user goal, and performance contract.
3. Read the relevant `rules/<rule-id>.md` cards before making non-trivial Rust recommendations.
4. Cite rule IDs in reviews and design decisions.
5. Apply `when_not` before recommending a rule. Do not force a rule when the exception applies.
6. Use `verification` to choose tests, benchmarks, clippy lints, Miri, fuzzing, semver checks, or runtime measurements.

## Required Output Behavior

- For reviews: group findings by rule ID and severity.
- For implementation: mention which rules shaped API, ownership, async, unsafe, and performance choices.
- For optimization: distinguish measured, likely, and speculative improvements.
- For unsafe/eBPF/SIMD/FFI: state the invariant and the rule that protects it.
- For PyO3/Wasm/FFI: call out boundary-copy and lifetime rules.
- For HFT/SBE: include tail latency, allocation/copy count, bounds checks, schema/version compatibility, and backpressure rules.

## Local Rule Files

- `rules/index.json`: searchable rule index.
- `rules/*.md`: expert rule cards with `id`, `severity`, `trigger`, `bad`, `good`, `when`, `when_not`, `verification`, `sources`, and `related_rules`.

Prefer the MCP tools `select_rust_rules` and `explain_rust_rule` when available; otherwise inspect `rules/index.json` and open the matching rule cards directly.
