# async-runtime-deliberate-choice

## id
async-runtime-deliberate-choice

## severity
high

## trigger
Async application setup, library APIs that may be runtime-agnostic, or code that adds Tokio without a clear runtime contract.

## bad
```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    library_entrypoint().await
}
```

## good
```rust
async fn run(client: Client) -> anyhow::Result<()> {
    client.fetch().await?;
    Ok(())
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    run(Client::new()).await
}
```

## when
Use when choosing an async runtime, adding `#[tokio::main]`, or designing library APIs that should not own the executor.

## when_not
Do not prescribe Tokio inside reusable libraries unless the crate intentionally exposes Tokio-specific types, timers, or I/O traits.

## verification
Measure runtime worker saturation, blocking sections, cancellation behavior, and test the public API without requiring hidden global runtime state.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Tokio: https://tokio.rs/

## related_rules
- async-tokio-runtime
- async-spawn-blocking
- async-cancel-safety
