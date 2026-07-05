# lint-warn-suspicious

## id
lint-warn-suspicious

## severity
low

## trigger
Enable clippy::suspicious for likely bugs. Trigger when working on linting and the code shows `lint`-class risk.

## bad
Avoid applying `lint-warn-suspicious` blindly. The risky pattern is code that ignores: Enable clippy::suspicious for likely bugs.

## good
Prefer the design encouraged by `lint-warn-suspicious`: Enable clippy::suspicious for likely bugs. Keep it explicit and testable.

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
- lint-deny-correctness
- lint-warn-complexity
- lint-warn-style
