# lint-rustfmt-check

## id
lint-rustfmt-check

## severity
low

## trigger
Run cargo fmt --check in CI. Trigger when working on linting and the code shows `lint`-class risk.

## bad
Avoid applying `lint-rustfmt-check` blindly. The risky pattern is code that ignores: Run cargo fmt --check in CI.

## good
Prefer the design encouraged by `lint-rustfmt-check`: Run cargo fmt --check in CI. Keep it explicit and testable.

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
- lint-pedantic-selective
- lint-warn-style
- name-funcs-snake
