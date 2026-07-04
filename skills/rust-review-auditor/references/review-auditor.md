# Rust Review Auditor Reference

## Findings To Prioritize

- unsound `unsafe`;
- new allocation/copy in hot path;
- unbounded channel or queue;
- blocking call in async worker;
- missing error handling around FFI or bindings;
- public API break without migration path;
- benchmark claim without benchmark evidence;
- missing tests for parser/protocol/boundary logic.

## Review Commands

```bash
cargo fmt --check
cargo clippy --all-targets --all-features
cargo test --all-targets --all-features
cargo bench
python3 scripts/rust_project_audit.py .
```

Use only commands that fit the project.

## Output Shape

- Findings first, ordered by severity.
- Then open questions.
- Then validation performed or missing.
- Then concise summary.
