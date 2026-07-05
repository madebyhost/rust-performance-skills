# api-must-use

## id
api-must-use

## severity
high

## trigger
Mark types and functions with `#[must_use]` when ignoring results is likely a bug. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Result ignored - error silently dropped
fn send_email(to: &str, body: &str) -> Result<(), EmailError> { ... }

send_email("user@example.com", "Hello!");  // No warning if Result ignored!
// Email may have failed, but we don't know

// Computed value ignored - likely a bug
fn compute_checksum(data: &[u8]) -> u32 { ... }

let data = vec![1, 2, 3, 4];
compute_checksum(&data);  // Result discarded - pointless call
```

## good
```rust
#[must_use = "this `Result` may be an `Err` that should be handled"]
fn send_email(to: &str, body: &str) -> Result<(), EmailError> { ... }

send_email("user@example.com", "Hello!");
// Warning: unused `Result` that must be used

// Mark pure functions
#[must_use = "this returns a new value and does not modify the input"]
fn compute_checksum(data: &[u8]) -> u32 { ... }

compute_checksum(&data);
// Warning: unused return value of `compute_checksum` that must be used
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
- api-builder-must-use
- err-result-over-panic
- lint-deny-correctness
