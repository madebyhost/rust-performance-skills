# conv-tryfrom-fallible

## id
conv-tryfrom-fallible

## severity
medium

## trigger
Implement `TryFrom` for fallible conversions instead of ad-hoc conversion functions. Trigger when working on conversion boundaries and the code shows `conv`-class risk.

## bad
```rust
use std::io;

struct Port(u16);

// Bespoke function - callers must know its name, can't use `.try_into()`
fn port_from_u32(n: u32) -> Result<Port, String> {
    if n > u16::MAX as u32 {
        return Err(format!("port {} out of range", n));
    }
    Ok(Port(n as u16))
}

fn main() {
    let p = port_from_u32(8080).unwrap();
}
```

## good
```rust
use std::fmt;

#[derive(Debug)]
struct Port(u16);

#[derive(Debug)]
struct PortError(u32);

impl fmt::Display for PortError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "port {} is out of range (0-65535)", self.0)
    }
}

impl std::error::Error for PortError {}

impl TryFrom<u32> for Port {
    type Error = PortError;

    fn try_from(value: u32) -> Result<Self, Self::Error> {
        u16::try_from(value)
            .map(Port)
            .map_err(|_| PortError(value))
    }
}

fn accept_port(n: u32) -> Result<Port, PortError> {
    // Callers use the standard `.try_into()?` idiom
    n.try_into()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let p: Port = 8080_u32.try_into()?;
    println!("port: {}", p.0);
    Ok(())
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
- api-from-not-into
- api-parse-dont-validate
- conv-fromstr-parsing
