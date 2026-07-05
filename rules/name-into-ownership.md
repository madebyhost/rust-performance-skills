# name-into-ownership

## id
name-into-ownership

## severity
medium

## trigger
Use `into_` prefix for ownership-consuming conversions. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
impl Wrapper {
    // Misleading: doesn't indicate ownership transfer
    fn get_inner(self) -> Inner {
        self.inner
    }

    // Misleading: suggests borrowing
    fn as_inner(self) -> Inner {  // Takes self by value!
        self.inner
    }
}
```

## good
```rust
impl Wrapper {
    // into_ clearly shows ownership transfer
    fn into_inner(self) -> Inner {
        self.inner
    }
}

// Usage is clear
let wrapper = Wrapper::new(inner);
let inner = wrapper.into_inner();  // wrapper is consumed
// wrapper.foo();  // Error: use of moved value
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
- api-from-not-into
- name-as-free
- name-to-expensive
