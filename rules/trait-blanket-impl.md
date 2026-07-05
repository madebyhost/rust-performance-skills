# trait-blanket-impl

## id
trait-blanket-impl

## severity
medium

## trigger
Use a blanket impl `impl<T: Bound> Trait for T` to give behaviour to every type that satisfies a bound. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
use std::fmt;

trait Describe {
    fn describe(&self) -> String;
}

// Manual impl for each type - tedious and doesn't scale.
impl Describe for i32 {
    fn describe(&self) -> String { format!("i32: {self}") }
}
impl Describe for f64 {
    fn describe(&self) -> String { format!("f64: {self}") }
}
impl Describe for bool {
    fn describe(&self) -> String { format!("bool: {self}") }
}
// ... repeated for every type that happens to implement Display
```

## good
```rust
use std::fmt;

// Extension trait that any `Display` type receives automatically.
trait Describe {
    fn describe(&self) -> String;
}

// One blanket impl covers every T: Display - mirrors how std blanket-impls ToString.
impl<T: fmt::Display> Describe for T {
    fn describe(&self) -> String {
        format!("{} ({})", self, std::any::type_name::<T>())
    }
}

// ----- Downstream usage: zero extra code required -----

fn print_described(value: &impl Describe) {
    println!("{}", value.describe());
}

fn demo() {
    print_described(&42_i32);
    print_described(&3.14_f64);
    print_described(&true);
    print_described(&"hello");
}

// ----- You CANNOT also override it for one type -----
// Writing `impl Describe for MyType` while the blanket impl exists is a
// coherence conflict (E0119): stable Rust has no specialization, so a blanket
// impl and a specific impl can never overlap. If you need a per-type override,
// don't use a blanket impl - or wrap the type in a newtype (see See Also).
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
- api-extension-trait
- api-sealed-trait
- trait-coherence-newtype
