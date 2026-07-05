# obs-instrument-spans

## id
obs-instrument-spans

## severity
medium

## trigger
Use `#[tracing::instrument]` and spans to attach context to async tasks and requests. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
use tracing::{info, span, Level};

// BAD: holding an entry guard across .await corrupts span context
async fn fetch_user(user_id: u64) -> Result<String, String> {
    let span = span!(Level::INFO, "fetch_user", user_id);
    let _guard = span.enter(); // guard held here...

    let result = some_async_db_call(user_id).await; // ...across this await - wrong!
    info!("fetched user");
    result
}

async fn some_async_db_call(_id: u64) -> Result<String, String> {
    Ok("alice".to_string())
}
```

## good
```rust
use tracing::{info, instrument, Instrument, info_span};

// GOOD: #[instrument] handles async correctly; skip large/sensitive args
#[instrument(skip(db), fields(user.id = user_id))]
async fn fetch_user(user_id: u64, db: &DbPool) -> Result<String, DbError> {
    info!("fetching user from database");
    let user = db.query_user(user_id).await?;
    info!(username = %user.name, "user fetched");
    Ok(user.name)
}

// GOOD: manual span + .instrument() for dynamic span names
async fn process_job(job_id: &str) {
    let span = info_span!("process_job", job.id = job_id);
    async move {
        info!("job started");
        do_work().await;
        info!("job complete");
    }
    .instrument(span)
    .await;
}

async fn do_work() {}

// Placeholder types for the example
struct DbPool;
#[derive(Debug)] struct DbUser { name: String }
#[derive(Debug)] struct DbError;

impl DbPool {
    async fn query_user(&self, _id: u64) -> Result<DbUser, DbError> {
        Ok(DbUser { name: "alice".to_string() })
    }
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
- async-no-lock-await
- obs-no-sensitive-data
- obs-structured-fields
