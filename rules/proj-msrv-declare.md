# proj-msrv-declare

## id
proj-msrv-declare

## severity
low

## trigger
Declare `rust-version` (MSRV) in Cargo.toml and test it in CI. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
# no rust-version - users get cryptic errors on old toolchains,
# and nothing prevents a dep bump from silently raising the floor
```

## good
```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
rust-version = "1.80"  # oldest toolchain you commit to supporting

[workspace]
resolver = "3"  # default for edition 2024; enables MSRV-aware dep resolution
```

CI job pinning the MSRV toolchain (GitHub Actions example):

```yaml
# .github/workflows/msrv.yml
- name: Install MSRV toolchain
  uses: dtolnay/rust-toolchain@master
  with:
    toolchain: "1.80"

- name: Check MSRV
  run: cargo check --all-features
```

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
- doc-cargo-metadata
- lint-cargo-metadata
- proj-workspace-deps
