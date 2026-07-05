# name-as-free

## id
name-as-free

## severity
medium

## trigger
`as_` prefix: free reference conversion. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
impl MyType {
    // BAD: as_ but allocates
    pub fn as_string(&self) -> String {
        format!("{}", self.value)  // Allocates! Should be to_string()
    }

    // BAD: as_ but expensive
    pub fn as_processed(&self) -> &ProcessedData {
        // Actually does expensive computation
    }
}
```

## good
```rust
impl MyType {
    // GOOD: Free reference
    pub fn as_str(&self) -> &str {
        &self.inner
    }

    // GOOD: to_ signals allocation
    pub fn to_string(&self) -> String {
        format!("{}", self.value)
    }

    // GOOD: into_ signals ownership transfer
    pub fn into_inner(self) -> Inner {
        self.inner
    }
}
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
- name-into-ownership
- name-to-expensive
