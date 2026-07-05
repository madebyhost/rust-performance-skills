# lint-cargo-metadata

## id
lint-cargo-metadata

## severity
low

## trigger
Enable clippy::cargo for published crates. Trigger when working on linting and the code shows `lint`-class risk.

## bad
Avoid applying `lint-cargo-metadata` blindly. The risky pattern is code that ignores: Enable clippy::cargo for published crates.

## good
Prefer the design encouraged by `lint-cargo-metadata`: Enable clippy::cargo for published crates. Keep it explicit and testable.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- doc-cargo-metadata
- lint-deny-correctness
- proj-workspace-deps
