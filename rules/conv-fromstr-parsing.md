# conv-fromstr-parsing

## id
conv-fromstr-parsing

## severity
medium

## trigger
Implement `FromStr` to enable `str::parse` for string-to-type conversions. Trigger when working on conversion boundaries and the code shows `conv`-class risk.

## bad
```rust
#[derive(Debug)]
enum Color { Red, Green, Blue }

// Callers must know this private name; no `.parse()` support
fn parse_color(s: &str) -> Result<Color, String> {
    match s {
        "red"   => Ok(Color::Red),
        "green" => Ok(Color::Green),
        "blue"  => Ok(Color::Blue),
        other   => Err(format!("unknown color: {other}")),
    }
}

fn main() {
    let c = parse_color("red").unwrap();
}
```

## good
```rust
use std::str::FromStr;
use std::fmt;

#[derive(Debug, PartialEq)]
enum Color { Red, Green, Blue }

#[derive(Debug)]
struct ParseColorError(String);

impl fmt::Display for ParseColorError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "unknown color: {}", self.0)
    }
}

impl std::error::Error for ParseColorError {}

impl FromStr for Color {
    type Err = ParseColorError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "red"   => Ok(Color::Red),
            "green" => Ok(Color::Green),
            "blue"  => Ok(Color::Blue),
            other   => Err(ParseColorError(other.to_owned())),
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Standard idiom - works with clap, config parsers, etc.
    let c: Color = "green".parse()?;
    assert_eq!(c, Color::Green);
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
- api-parse-dont-validate
- conv-tryfrom-fallible
- type-newtype-validated
