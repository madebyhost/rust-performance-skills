# trait-dyn-vs-generic

## id
trait-dyn-vs-generic

## severity
medium

## trigger
Choose static dispatch (generics / `impl Trait`) vs dynamic dispatch (`dyn Trait`) deliberately. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
// Using `dyn` everywhere "to be flexible" - blocks inlining and
// forces heap allocation even for single, known types.
trait Shape {
    fn area(&self) -> f64;
}

struct Circle { radius: f64 }
impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
}

// Unnecessary boxing when only one concrete type is used.
fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}
```

## good
```rust
use std::fmt;

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
}

#[derive(Clone)]
struct Circle { radius: f64 }
#[derive(Clone)]
struct Rect { w: f64, h: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn name(&self) -> &str { "circle" }
}
impl Shape for Rect {
    fn area(&self) -> f64 { self.w * self.h }
    fn name(&self) -> &str { "rect" }
}

// --- Static dispatch: use when the type is known and performance matters ---
// Monomorphized; the compiler can inline `area()`.
fn total_area_generic<S: Shape>(shapes: &[S]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

// Also fine with `impl Trait` in argument position (same monomorphization).
fn print_area(shape: &impl Shape) {
    println!("{}: {:.2}", shape.name(), shape.area());
}

// --- Dynamic dispatch: use for heterogeneous collections or plugin-like APIs ---
fn total_area_dyn(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

fn demo() {
    // Homogeneous slice - zero boxing, static dispatch.
    let circles = [Circle { radius: 1.0 }, Circle { radius: 2.0 }];
    println!("{:.2}", total_area_generic(&circles));

    // Heterogeneous collection - `dyn` is the right tool.
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { radius: 1.0 }),
        Box::new(Rect { w: 3.0, h: 4.0 }),
    ];
    println!("{:.2}", total_area_dyn(&shapes));
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
- anti-type-erasure
- trait-object-safety
- type-generic-bounds
