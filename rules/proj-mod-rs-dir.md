# proj-mod-rs-dir

## id
proj-mod-rs-dir

## severity
low

## trigger
Use mod.rs for multi-file modules. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
Avoid applying `proj-mod-rs-dir` blindly. The risky pattern is code that ignores: Use mod.rs for multi-file modules.

## good
Prefer the design encouraged by `proj-mod-rs-dir`: Use mod.rs for multi-file modules. Keep it explicit and testable.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- proj-flat-small
- proj-mod-by-feature
- proj-pub-use-reexport
