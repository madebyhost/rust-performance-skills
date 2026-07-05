# macro-prefer-functions

## id
macro-prefer-functions

## severity
medium

## trigger
Reach for a macro only when a function or generic cannot express it. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// Nothing here requires a macro - no variadic args, no DSL, no trait impl.
macro_rules! double {
    ($x:expr) => {
        $x * 2
    };
}

fn main() {
    let n = double!(21);
    println!("{n}");
}
```

## good
```rust
// A generic function is clearer, debuggable, and just as efficient.
#[inline]
fn double<T>(x: T) -> T
where
    T: std::ops::Mul<Output = T> + Copy,
{
    x * x  // or x + x for integer-like types
}

fn main() {
    let n = double(21_i32);
    println!("{n}");
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not write a macro when a function, trait, or const generic expresses the same idea clearly.

## verification
Add compile-pass and compile-fail tests covering exported macro paths and helper visibility.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- anti-over-abstraction
- macro-rules-hygiene
- type-generic-bounds
