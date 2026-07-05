# type-enum-over-boolean-parameter

## id
type-enum-over-boolean-parameter

## severity
medium

## trigger
Public functions or constructors with boolean parameters whose meaning is not obvious at the call site.

## bad
```rust
client.sync(true, false);
```

## good
```rust
client.sync(SyncMode::Force, ConflictPolicy::KeepRemote);
```

## when
Use when each boolean represents a named mode, policy, direction, or state that affects behavior.

## when_not
Do not replace clear predicate setters or local booleans when names already communicate the behavior.

## verification
Check call sites for readability, add exhaustive tests for enum variants, and document default policies.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- type-enum-states
- pat-exhaustive-enum
- api-non-exhaustive
