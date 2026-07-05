# tauri-batched-ipc-boundary

## id
tauri-batched-ipc-boundary

## severity
high

## trigger
Tauri commands or frontend code call `invoke` per row, packet, record, log line, progress tick, or UI item.

## bad
```rust
#[tauri::command]
fn get_quote(id: u64) -> Quote {
    load_quote(id)
}
```

## good
```rust
#[tauri::command]
fn get_quotes(ids: Vec<u64>) -> Result<Vec<Quote>, AppError> {
    load_quotes_batch(&ids)
}
```

## when
Use when IPC call count, JSON serialization, scheduler hops, or frontend re-rendering can dominate the useful Rust work.

## when_not
Do not batch unrelated user actions when separate commands provide clearer authorization, cancellation, or failure reporting.

## verification
Measure command count, bytes per command, command latency, frontend render time, memory growth, and p95/p99 UI responsiveness under realistic data size.

## sources
- Tauri IPC: https://v2.tauri.app/concept/inter-process-communication/
- Tauri Rust to frontend communication: https://v2.tauri.app/develop/calling-frontend/

## related_rules
- wasm-boundary-copy-budget
- perf-batch-processing
- async-blocking-boundary-budget
