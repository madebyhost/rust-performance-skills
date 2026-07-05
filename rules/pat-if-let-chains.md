# pat-if-let-chains

## id
pat-if-let-chains

## severity
medium

## trigger
Use `if let` chains to combine pattern bindings and conditions. Trigger when working on pattern matching and the code shows `pat`-class risk.

## bad
```rust
fn handle(input: Option<String>, limit: Option<u32>) -> Option<String> {
    if let Some(s) = input {
        if let Ok(n) = s.trim().parse::<u32>() {
            if let Some(max) = limit {
                if n <= max {
                    return Some(format!("valid: {n}"));
                }
            }
        }
    }
    None
}
```

## good
```rust
fn handle(input: Option<String>, limit: Option<u32>) -> Option<String> {
    if let Some(s) = input
        && let Ok(n) = s.trim().parse::<u32>()
        && let Some(max) = limit
        && n <= max
    {
        return Some(format!("valid: {n}"));
    }
    None
}
```

Each `&&` clause is evaluated in order; short-circuit semantics still apply, so later clauses only run if earlier ones succeed.

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
- pat-let-else
- pat-matches-macro
