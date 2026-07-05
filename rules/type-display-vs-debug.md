# type-display-vs-debug

## id
type-display-vs-debug

## severity
medium

## trigger
Use `Display` for user-facing output and `Debug` for diagnostics; never swap them. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
#[derive(Debug)]
struct ParseError {
    input: String,
    line: u32,
}

// Mistake 1: using Debug output in a user-facing message
fn report_error(e: &ParseError) {
    eprintln!("failed: {:?}", e); // leaks internal field names
}

// Mistake 2: implementing Display by calling debug
use std::fmt;
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self) // wrong - duplicates Debug
    }
}
```

## good
```rust
use std::fmt;

#[derive(Debug)] // derive Debug for free diagnostic output
struct ParseError {
    input: String,
    line: u32,
}

// Hand-write Display for a clean, human-readable message
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "parse error on line {}: {:?}", self.line, self.input)
    }
}

impl std::error::Error for ParseError {}

fn main() {
    let e = ParseError { input: "foo bar".into(), line: 42 };

    // User-facing: clean sentence
    eprintln!("error: {e}");

    // Developer/log: structured dump
    eprintln!("debug: {e:?}");
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
- api-common-traits
- err-thiserror-lib
- type-numeric-fmt
