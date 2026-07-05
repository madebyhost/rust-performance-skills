# api-constructor-owned-boundary

## id
api-constructor-owned-boundary

## severity
medium

## trigger
Constructors, builders, or factory functions that receive user-owned strings, paths, byte buffers, or domain values.

## bad
```rust
impl User {
    pub fn new(name: &str) -> Self {
        Self { name: name.to_string() }
    }
}
```

## good
```rust
impl User {
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into() }
    }
}
```

## when
Use when the constructed type stores owned data and callers may already have either borrowed or owned inputs.

## when_not
Do not use `impl Into<String>` when the function only borrows temporarily; prefer `&str` or `AsRef<str>` for borrowed APIs.

## verification
Add constructor tests for borrowed and owned inputs, check public API docs, and ensure the owned allocation happens only at the ownership boundary.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-impl-into
- own-borrow-over-clone
- anti-string-for-str
