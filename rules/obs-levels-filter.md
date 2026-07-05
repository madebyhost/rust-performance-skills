# obs-levels-filter

## id
obs-levels-filter

## severity
medium

## trigger
Use log levels meaningfully and filter with `EnvFilter` / `RUST_LOG`. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
use tracing::info;

fn handle_request(path: &str, body: &[u8]) {
    // BAD: debug-level detail emitted at info - always noisy in production
    info!(path, body_len = body.len(), raw = ?body, "handling request");
    info!("entered handle_request");         // trace-level lifecycle noise
    info!("about to parse body");            // also trace-level
    // ... actual logic ...
    info!("done handling request");
}
```

## good
```rust
use tracing::{debug, error, info, instrument, trace, warn};

#[instrument(skip(body))]
fn handle_request(path: &str, body: &[u8]) {
    trace!("entered handler");                          // very verbose - trace
    debug!(body_len = body.len(), "parsing body");      // diagnostic - debug
    info!(path, "request received");                    // lifecycle - info

    match parse_body(body) {
        Ok(parsed) => {
            info!(items = parsed.len(), "request processed");
        }
        Err(e) if is_client_error(&e) => {
            warn!(error = ?e, "malformed request from client");   // recoverable - warn
        }
        Err(e) => {
            error!(error = ?e, "unexpected parse failure");       // needs attention - error
        }
    }
}

fn parse_body(_body: &[u8]) -> Result<Vec<u8>, String> { Ok(vec![]) }
fn is_client_error(_e: &str) -> bool { false }
```

```rust
// In main: configure EnvFilter from RUST_LOG
fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,myapp=debug,hyper=warn".into()),
        )
        .init();
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
- obs-library-facade
- obs-tracing-over-log
