# iter-collect-result-boundary

## id
iter-collect-result-boundary

## severity
medium

## trigger
Iterator pipelines that transform fallible operations, parse many inputs, or convert many rows/items into domain values.

## bad
```rust
let users: Vec<User> = rows
    .into_iter()
    .filter_map(|row| User::try_from(row).ok())
    .collect();
```

## good
```rust
let users: Result<Vec<User>, UserError> = rows
    .into_iter()
    .map(User::try_from)
    .collect();
```

## when
Use when failures must be preserved and the caller should see the first conversion error instead of silent item loss.

## when_not
Do not use this when lossy filtering is the documented business rule; name that behavior explicitly.

## verification
Test success, first-error propagation, empty input, and input containing multiple invalid rows.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Rust Iterator docs: https://doc.rust-lang.org/std/iter/trait.Iterator.html

## related_rules
- err-question-mark
- conv-tryfrom-fallible
- type-result-fallible
