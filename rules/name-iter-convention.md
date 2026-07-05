# name-iter-convention

## id
name-iter-convention

## severity
medium

## trigger
Use iter/iter_mut/into_iter for iterator methods. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
impl MyCollection<T> {
    // Non-standard names
    fn elements(&self) -> impl Iterator<Item = &T> { }      // Should be iter()
    fn get_items(&self) -> impl Iterator<Item = &T> { }     // Should be iter()
    fn iterate(&self) -> impl Iterator<Item = &T> { }       // Should be iter()
    fn as_iter(&self) -> impl Iterator<Item = &T> { }       // Should be iter()
}
```

## good
Prefer the design encouraged by `name-iter-convention`: Use iter/iter_mut/into_iter for iterator methods. Keep it explicit and testable.

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
- name-iter-method
- name-iter-type-match
- perf-iter-over-index
