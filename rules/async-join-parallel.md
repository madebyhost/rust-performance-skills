# async-join-parallel

## id
async-join-parallel

## severity
high

## trigger
Use `join!` or `try_join!` for concurrent independent futures. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
async fn fetch_data() -> (User, Posts, Comments) {
    // Sequential: 300ms total (100 + 100 + 100)
    let user = fetch_user().await;        // 100ms
    let posts = fetch_posts().await;      // 100ms
    let comments = fetch_comments().await; // 100ms

    (user, posts, comments)
}

async fn read_configs() -> Result<(Config, Settings)> {
    // Sequential: 20ms + 20ms = 40ms
    let config = fs::read_to_string("config.toml").await?;
    let settings = fs::read_to_string("settings.json").await?;

    Ok((parse_config(&config)?, parse_settings(&settings)?))
}
```

## good
```rust
use tokio::join;

async fn fetch_data() -> (User, Posts, Comments) {
    // Concurrent: ~100ms total (max of all three)
    let (user, posts, comments) = join!(
        fetch_user(),
        fetch_posts(),
        fetch_comments(),
    );

    (user, posts, comments)
}

use tokio::try_join;

async fn read_configs() -> Result<(Config, Settings)> {
    // Concurrent: ~20ms total
    let (config_str, settings_str) = try_join!(
        fs::read_to_string("config.toml"),
        fs::read_to_string("settings.json"),
    )?;

    Ok((parse_config(&config_str)?, parse_settings(&settings_str)?))
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not force async for CPU-bound work without I/O concurrency; prefer threads or Rayon when they fit the workload.

## verification
Add concurrency tests, cancellation tests, and runtime checks for backpressure or lock scope.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- async-joinset-structured
- async-select-racing
- async-try-join
