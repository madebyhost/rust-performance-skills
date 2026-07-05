# obs-structured-fields

## id
obs-structured-fields

## severity
medium

## trigger
Record structured key-value fields, not values interpolated into the message string. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
use tracing::info;

fn process_batch(user_id: u64, items: usize, elapsed_ms: u64) {
    // Values buried in the message string - unqueryable in aggregators
    info!("processed {} items for user {} in {}ms", items, user_id, elapsed_ms);
}
```

## good
```rust
use tracing::info;

fn process_batch(user_id: u64, items: usize, elapsed_ms: u64) {
    // Structured: each value is a discrete, queryable field
    info!(
        user.id = user_id,
        items,
        elapsed_ms,
        "batch processed"
    );
}

#[derive(Debug)]
struct Request {
    path: String,
    method: String,
}

fn handle_request(req: &Request, status: u16) {
    // %req uses Display; ?req uses Debug; status is a primitive
    info!(
        request = ?req,   // Debug format for the whole struct
        status,
        "request complete"
    );
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
- obs-error-chain
- obs-no-sensitive-data
- obs-tracing-over-log
