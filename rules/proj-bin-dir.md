# proj-bin-dir

## id
proj-bin-dir

## severity
low

## trigger
Put multiple binaries in src/bin/. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```
my-project/
|-- Cargo.toml        # Complex [[bin]] sections for each binary
|-- src/
|   |-- main.rs       # Which binary is this?
|   |-- server.rs     # Is this a module or binary?
|   |-- cli.rs        # Unclear
|   `-- lib.rs
```

```toml
# Cargo.toml - verbose and error-prone
[[bin]]
name = "server"
path = "src/server.rs"

[[bin]]
name = "cli"
path = "src/cli.rs"
```

## good
```
my-project/
|-- Cargo.toml        # Clean, no [[bin]] needed
|-- src/
|   |-- lib.rs        # Shared library code
|   `-- bin/
|       |-- server.rs # Binary: my-project-server (or just server)
|       `-- cli.rs    # Binary: my-project-cli (or just cli)
```

Each file in `src/bin/` automatically becomes a binary named after the file.

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
- proj-lib-main-split
- proj-workspace-large
