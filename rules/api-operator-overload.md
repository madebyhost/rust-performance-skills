# api-operator-overload

## id
api-operator-overload

## severity
high

## trigger
Overload operators only when the semantics are natural and unsurprising. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
use std::ops::Add;

struct Logger(Vec<String>);

// Anti-pattern: + mutates internal state and has a side effect
impl Add<String> for Logger {
    type Output = Logger;

    fn add(mut self, msg: String) -> Logger {
        self.0.push(msg.clone());
        println!("logged: {msg}"); // side effect in an operator
        self
    }
}
```

## good
```rust
use std::ops::{Add, Neg};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Vector2 {
    x: f64,
    y: f64,
}

impl Vector2 {
    pub fn new(x: f64, y: f64) -> Self {
        Vector2 { x, y }
    }

    pub fn dot(self, other: Vector2) -> f64 {
        self.x * other.x + self.y * other.y
    }
}

// Add for owned values
impl Add for Vector2 {
    type Output = Vector2;

    fn add(self, rhs: Vector2) -> Vector2 {
        Vector2::new(self.x + rhs.x, self.y + rhs.y)
    }
}

// Also implement for references - avoids forcing callers to clone
impl Add for &Vector2 {
    type Output = Vector2;

    fn add(self, rhs: &Vector2) -> Vector2 {
        Vector2::new(self.x + rhs.x, self.y + rhs.y)
    }
}

impl Neg for Vector2 {
    type Output = Vector2;

    fn neg(self) -> Vector2 {
        Vector2::new(-self.x, -self.y)
    }
}

fn main() {
    let a = Vector2::new(1.0, 2.0);
    let b = Vector2::new(3.0, 4.0);

    let c = a + b;               // owned
    let d = &a + &b;             // borrowed - no clone needed
    let e = -a;

    assert_eq!(c, Vector2::new(4.0, 6.0));
    assert_eq!(d, Vector2::new(4.0, 6.0));
    assert_eq!(e, Vector2::new(-1.0, -2.0));
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-common-traits
- type-newtype-ids
