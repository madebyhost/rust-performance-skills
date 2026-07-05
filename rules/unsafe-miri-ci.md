# unsafe-miri-ci

## id
unsafe-miri-ci

## severity
critical

## trigger
Run `cargo miri test` in CI for every crate that contains `unsafe` code.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```yaml
# CI that tests but never runs Miri - unsafe code ships unverified.
- name: Test
  run: cargo test --all-features
```

## good
```yaml
# .github/workflows/miri.yml
name: Miri

on: [push, pull_request]

jobs:
  miri:
    name: Miri (nightly)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install nightly toolchain with Miri
        run: |
          rustup toolchain install nightly --component miri
          rustup override set nightly
          cargo miri setup

      - name: Run Miri
        env:
          MIRIFLAGS: "-Zmiri-strict-provenance"
        run: cargo miri test --all-features
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not use unsafe to silence the borrow checker without a written invariant and a safe abstraction boundary.

## verification
Require SAFETY documentation, Miri or sanitizer coverage where possible, and safe-wrapper tests.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- test-criterion-bench
- unsafe-maybeuninit
- unsafe-safety-comment
