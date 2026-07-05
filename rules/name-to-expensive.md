# name-to-expensive

## id
name-to-expensive

## severity
medium

## trigger
Use `to_` prefix for expensive conversions that allocate or compute. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
impl Name {
    // Misleading: suggests expensive operation
    fn as_uppercase(&self) -> String {
        self.0.to_uppercase()  // Allocates!
    }

    // Misleading: suggests cheap reference
    fn get_string(&self) -> String {
        self.0.clone()  // Allocates!
    }
}
```

## good
```rust
impl Name {
    // to_ = allocates/computes
    fn to_uppercase(&self) -> String {
        self.0.to_uppercase()
    }

    // to_ = creates new value
    fn to_string(&self) -> String {
        self.0.clone()
    }

    // as_ = free reference (cheap)
    fn as_str(&self) -> &str {
        &self.0
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
- name-as-free
- name-into-ownership
- own-cow-conditional
