# tauri-channel-streaming

## id
tauri-channel-streaming

## severity
high

## trigger
Tauri apps stream progress, logs, search results, telemetry, imports, or long-running Rust task output to the frontend.

## bad
```rust
for item in items {
    app.emit("item", item)?;
}
```

## good
```rust
#[tauri::command]
async fn import_file(path: String, progress: tauri::ipc::Channel<Progress>) -> Result<(), AppError> {
    run_import(path, |update| progress.send(update)).await
}
```

## when
Use when Rust-to-frontend updates are frequent, ordered, cancellable, or large enough that event spam would hurt responsiveness.

## when_not
Do not use channels for tiny fan-out lifecycle notifications where events are simpler and performance is irrelevant.

## verification
Measure channel backlog, dropped or delayed updates, cancellation latency, UI frame time, memory growth, and behavior when the window closes mid-stream.

## sources
- Tauri Rust to frontend communication: https://v2.tauri.app/develop/calling-frontend/
- Tauri IPC: https://v2.tauri.app/concept/inter-process-communication/

## related_rules
- tauri-batched-ipc-boundary
- async-bounded-channel
- async-cancel-safety
