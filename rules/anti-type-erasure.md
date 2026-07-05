# anti-type-erasure

## id
anti-type-erasure

## severity
reference

## trigger
Don't use Box<dyn Trait> when impl Trait works. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Unnecessary type erasure
fn get_iterator() -> Box<dyn Iterator<Item = i32>> {
    Box::new((0..10).map(|x| x * 2))
}

// Boxing for no reason
fn make_handler() -> Box<dyn Fn(i32) -> i32> {
    Box::new(|x| x + 1)
}

// Vec of boxed trait objects when one type would do
fn get_validators() -> Vec<Box<dyn Validator>> {
    vec![
        Box::new(LengthValidator),
        Box::new(RegexValidator),
    ]
}
```

## good
```rust
// impl Trait - zero overhead, inlined
fn get_iterator() -> impl Iterator<Item = i32> {
    (0..10).map(|x| x * 2)
}

// impl Fn - no boxing
fn make_handler() -> impl Fn(i32) -> i32 {
    |x| x + 1
}

// When mixed types are genuinely needed, Box is OK
fn get_validators() -> Vec<Box<dyn Validator>> {
    // Actually different types at runtime - Box is appropriate
    config.validators.iter()
        .map(|v| v.create_validator())
        .collect()
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
- anti-over-abstraction
- closure-static-vs-dyn
- mem-box-large-variant
- trait-dyn-vs-generic
- type-generic-bounds
