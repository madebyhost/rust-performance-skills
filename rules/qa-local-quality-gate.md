# qa-local-quality-gate

## id
qa-local-quality-gate

## severity
high

## trigger
Before committing Rust changes, opening PRs, publishing crates, or handing work back to a user.

## bad
```bash
cargo build
git commit -m change
```

## good
```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets --all-features
```

## when
Use for ordinary Rust code changes before claiming the work is ready.

## when_not
Do not blindly use `--all-features` when features are mutually exclusive; test the documented feature matrix instead.

## verification
Run the gate locally or in CI and record any skipped command with the exact blocker.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Cargo Book: https://doc.rust-lang.org/cargo/

## related_rules
- lint-rustfmt-check
- lint-deny-correctness
- test-integration-dir
