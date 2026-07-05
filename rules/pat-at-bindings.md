# pat-at-bindings

## id
pat-at-bindings

## severity
medium

## trigger
Use `@` bindings to capture a value while matching it against a pattern. Trigger when working on pattern matching and the code shows `pat`-class risk.

## bad
```rust
fn classify(n: u32) -> String {
    match n {
        1..=9 => format!("single digit: {n}"), // fine here - n is Copy and in scope
        10..=99 => {
            let tens = n; // no real benefit; contrived but shows the pattern
            format!("two digits: {tens}")
        }
        _ => String::from("large"),
    }
}

// More revealing: nested struct field - must re-access after matching range
#[derive(Debug)]
enum Command {
    Move { x: i32, y: i32 },
}

fn validate_move(cmd: &Command) {
    match cmd {
        Command::Move { x, y } if *x >= 0 && *x <= 100 => {
            // x is already bound, so this is fine, but the guard duplicates the range
            println!("valid move to x={x}, y={y}");
        }
        _ => println!("invalid command"),
    }
}
```

## good
```rust
fn classify(n: u32) -> String {
    match n {
        id @ 1..=9 => format!("single digit: {id}"),
        id @ 10..=99 => format!("two digits: {id}"),
        _ => String::from("large"),
    }
}

// Nested struct field with @ binding
#[derive(Debug)]
enum Command {
    Move { x: i32, y: i32 },
}

fn validate_move(cmd: &Command) {
    match cmd {
        Command::Move { x: x_pos @ 0..=100, y } => {
            println!("valid move to x={x_pos}, y={y}");
        }
        _ => println!("invalid command"),
    }
}
```

`x: x_pos @ 0..=100` destructures the `x` field, checks that it falls in `0..=100`, and binds the value to `x_pos` - all in one expression.

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
- pat-exhaustive-enum
- type-enum-states
