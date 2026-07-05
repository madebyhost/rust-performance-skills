# proj-flat-small

## id
proj-flat-small

## severity
low

## trigger
Keep small projects flat. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```
src/
|-- core/
|   `-- mod.rs           # Just re-exports
|-- domain/
|   |-- mod.rs
|   `-- models/
|       |-- mod.rs
|       `-- user.rs      # 50 lines
|-- infrastructure/
|   |-- mod.rs
|   `-- database/
|       |-- mod.rs
|       `-- connection.rs # 30 lines
|-- application/
|   |-- mod.rs
|   `-- services/
|       `-- mod.rs       # Empty
`-- main.rs
```

## good
```
src/
|-- main.rs
|-- lib.rs
|-- config.rs
|-- database.rs
|-- user.rs
`-- error.rs
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
- proj-lib-main-split
- proj-mod-by-feature
- proj-mod-rs-dir
