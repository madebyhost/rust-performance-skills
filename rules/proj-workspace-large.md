# proj-workspace-large

## id
proj-workspace-large

## severity
low

## trigger
Use workspaces for large projects. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```
# Separate repositories for each crate
my-app-core/
my-app-cli/
my-app-server/
my-app-common/

# Each has its own Cargo.lock
# Dependencies may drift
# Cross-crate development is painful
```

## good
```
my-app/
|-- Cargo.toml          # Workspace root
|-- Cargo.lock          # Shared lock file
|-- crates/
|   |-- core/
|   |   |-- Cargo.toml
|   |   `-- src/
|   |-- cli/
|   |   |-- Cargo.toml
|   |   `-- src/
|   |-- server/
|   |   |-- Cargo.toml
|   |   `-- src/
|   `-- common/
|       |-- Cargo.toml
|       `-- src/
`-- README.md
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
- proj-bin-dir
- proj-lib-main-split
- proj-workspace-deps
