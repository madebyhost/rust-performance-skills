# async-blocking-boundary-budget

## id
async-blocking-boundary-budget

## severity
high

## trigger
Async functions containing synchronous sleep, filesystem, compression, parsing, crypto, CPU-bound loops, or blocking client calls.

## bad
```rust
async fn refresh() {
    std::thread::sleep(Duration::from_secs(1));
    let bytes = std::fs::read("snapshot.bin").unwrap();
    parse_big_snapshot(bytes);
}
```

## good
```rust
async fn refresh() -> anyhow::Result<()> {
    tokio::time::sleep(Duration::from_secs(1)).await;
    let bytes = tokio::fs::read("snapshot.bin").await?;
    tokio::task::spawn_blocking(move || parse_big_snapshot(bytes)).await??;
    Ok(())
}
```

## when
Use when blocking work can stall async workers or hide latency spikes under load.

## when_not
Do not move tiny CPU work into `spawn_blocking`; the scheduling overhead can exceed the saved worker time.

## verification
Measure worker utilization, latency under concurrent load, blocking pool size, cancellation behavior, and queue depth.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Tokio spawn_blocking: https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html

## related_rules
- async-spawn-blocking
- async-tokio-fs
- async-bounded-channel
