# err-context-chain

## id
err-context-chain

## severity
critical

## trigger
Add context with `.context()` or `.with_context()`. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
// Raw error - no context
fn load_user(id: u64) -> Result<User, Error> {
    let path = format!("users/{}.json", id);
    let content = std::fs::read_to_string(&path)?;
    Ok(serde_json::from_str(&content)?)
}

// Error message: "No such file or directory (os error 2)"
// Which file? What were we doing?
```

## good
```rust
use anyhow::{Context, Result};

fn load_user(id: u64) -> Result<User> {
    let path = format!("users/{}.json", id);

    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read user file: {}", path))?;

    let user: User = serde_json::from_str(&content)
        .with_context(|| format!("failed to parse user {} JSON", id))?;

    Ok(user)
}

// Error: "failed to parse user 42 JSON"
// Caused by: "expected ':' at line 5 column 12"
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
- err-anyhow-app
- err-question-mark
- err-source-chain
