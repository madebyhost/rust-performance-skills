# trait-associated-type-vs-generic

## id
trait-associated-type-vs-generic

## severity
medium

## trigger
Use an associated type when each impl has exactly one output type; use a generic parameter when a type can implement the trait for many input types. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
// Using a generic parameter for a trait that has exactly one output per type.
// Callers must now write Parser<String, Output = Ast> or face ambiguity.
trait Parser<Output> {
    fn parse(&self, input: &str) -> Option<Output>;
}

struct JsonParser;

// Only one sensible Output ever exists for JsonParser, but the signature
// forces a type parameter that adds noise everywhere.
impl Parser<String> for JsonParser {
    fn parse(&self, input: &str) -> Option<String> {
        Some(input.to_owned())
    }
}

fn run<P: Parser<String>>(p: &P, s: &str) -> Option<String> {
    p.parse(s)
}
```

## good
```rust
// ----- Associated type: one output per implementor -----
// Mirrors std::iter::Iterator { type Item; }

trait Parser {
    type Output;
    fn parse(&self, input: &str) -> Option<Self::Output>;
}

struct JsonParser;
struct NumberParser;

#[derive(Debug)]
struct JsonValue(String);

impl Parser for JsonParser {
    type Output = JsonValue;
    fn parse(&self, input: &str) -> Option<JsonValue> {
        Some(JsonValue(input.to_owned()))
    }
}

impl Parser for NumberParser {
    type Output = f64;
    fn parse(&self, input: &str) -> Option<f64> {
        input.trim().parse().ok()
    }
}

// No turbofish needed - `P::Output` is unambiguous.
fn run<P: Parser>(p: &P, s: &str) -> Option<P::Output> {
    p.parse(s)
}

// ----- Generic parameter: multiple impls on the same type -----
// Mirrors std::ops::Add<Rhs> and std::convert::From<T>.

#[derive(Debug, Clone, Copy)]
struct Vec2 { x: f64, y: f64 }

// One type implementing the same "add" concept for two different Rhs types.
impl std::ops::Add<Vec2> for Vec2 {
    type Output = Vec2;
    fn add(self, rhs: Vec2) -> Vec2 { Vec2 { x: self.x + rhs.x, y: self.y + rhs.y } }
}

impl std::ops::Add<f64> for Vec2 {
    type Output = Vec2;
    fn add(self, rhs: f64) -> Vec2 { Vec2 { x: self.x + rhs, y: self.y + rhs } }
}

fn demo() {
    let a = Vec2 { x: 1.0, y: 2.0 };
    let b = Vec2 { x: 3.0, y: 4.0 };
    let _ = a + b;       // Add<Vec2>
    let _ = a + 10.0;    // Add<f64>

    let p = NumberParser;
    if let Some(n) = run(&p, " 3.14 ") {
        println!("{n}");
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
- api-impl-fromiterator
- trait-default-methods
- type-generic-bounds
