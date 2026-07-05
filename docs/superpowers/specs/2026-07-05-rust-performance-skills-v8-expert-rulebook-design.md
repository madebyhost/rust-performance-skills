# Rust Performance Skills v8 Expert Rulebook Design

## Goal

Move from specialist guidelines to a hybrid system: specialist skills route the task, while an expert rulebook constrains Rust code generation and review with concrete rule IDs.

## Design

- Import the MIT-licensed `leonardomso/rust-skills` rule corpus into `rules/`.
- Normalize every rule into the schema: `id`, `severity`, `trigger`, `bad`, `good`, `when`, `when_not`, `verification`, `sources`, `related_rules`.
- Add local rules for HFT, SBE, eBPF, PyO3, Wasm, SIMD, NUMA, graph/math kernels, and io_uring.
- Generate `rules/index.json` for MCP and agent selection.
- Add `rust-expert-rulebook` so agents cite rule IDs in reviews and non-trivial Rust decisions.
- Add MCP tools `select_rust_rules` and `explain_rust_rule`.

## Validation

- `tests/test_rulebook.py` checks scale, schema, imported examples, advanced rules, index parity, skill, and eval.
- `scripts/validate_rules.py` validates rule cards and index consistency.
- Distribution validation calls the rule validator.
