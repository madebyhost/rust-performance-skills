# type-numeric-fmt

## id
type-numeric-fmt

## severity
medium

## trigger
Implement `LowerHex`, `UpperHex`, `Octal`, and `Binary` for numeric newtypes. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
use std::fmt;

struct Mask(u32);

impl fmt::Display for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

fn main() {
    let m = Mask(0xDEAD_BEEF);
    println!("{}", m);   // ok
    // println!("{:x}", m); // compile error: Mask doesn't implement LowerHex
}
```

## good
```rust
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Mask(u32);

impl fmt::Display for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self.0, f)
    }
}

impl fmt::LowerHex for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::LowerHex::fmt(&self.0, f)
    }
}

impl fmt::UpperHex for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::UpperHex::fmt(&self.0, f)
    }
}

impl fmt::Octal for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Octal::fmt(&self.0, f)
    }
}

impl fmt::Binary for Mask {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Binary::fmt(&self.0, f)
    }
}

fn main() {
    let m = Mask(0xDEAD_BEEF);
    println!("{m}");          // 3735928559
    println!("{m:x}");        // deadbeef
    println!("{m:X}");        // DEADBEEF
    println!("{m:#010x}");    // 0xdeadbeef
    println!("{m:o}");        // 33653337357
    println!("{m:b}");        // 11011110101011011011111011101111
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not encode every boolean as typestate; use the type system when it removes real invalid states.

## verification
Add constructor tests, compile-fail tests where useful, and property tests for invariants.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- type-display-vs-debug
- type-newtype-ids
