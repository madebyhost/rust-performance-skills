# obs-error-chain

## id
obs-error-chain

## severity
medium

## trigger
Log errors with their full source chain, and log each error exactly once. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
use tracing::error;

async fn fetch_data(id: u64) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let data = read_from_db(id).await.map_err(|e| {
        error!("{}", e);  // BAD: drops source chain, logs too early
        e
    })?;
    Ok(data)
}

async fn handle(id: u64) -> Result<(), Box<dyn std::error::Error>> {
    let data = fetch_data(id).await.map_err(|e| {
        error!("{}", e);  // BAD: logged again at every layer
        e
    })?;
    process(data);
    Ok(())
}

async fn read_from_db(_id: u64) -> Result<Vec<u8>, std::io::Error> {
    Err(std::io::Error::other("connection refused"))
}
fn process(_data: Vec<u8>) {}
```

## good
```rust
use anyhow::{Context, Result};
use tracing::{error, instrument, warn};

// Propagate with context; do NOT log here
#[instrument]
async fn read_from_db(id: u64) -> Result<Vec<u8>> {
    inner_db_call(id)
        .await
        .with_context(|| format!("failed to read record {id} from database"))
    // No logging - just add context and propagate
}

// Also just propagates
#[instrument]
async fn fetch_data(id: u64) -> Result<Vec<u8>> {
    read_from_db(id).await.context("fetch_data failed")
}

// The handler boundary: this is where the error is HANDLED, so log it once
#[instrument]
async fn handle_request(id: u64) -> Result<(), String> {
    match fetch_data(id).await {
        Ok(data) => {
            process(data);
            Ok(())
        }
        Err(err) => {
            // {:#} on anyhow::Error prints the full cause chain
            error!(error = %format!("{err:#}"), "request failed");
            Err("internal error".to_string())
        }
    }
}

async fn inner_db_call(_id: u64) -> Result<Vec<u8>> {
    Err(anyhow::anyhow!("connection refused"))
}
fn process(_data: Vec<u8>) {}
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
- anti-empty-catch
- err-context-chain
- err-source-chain
