---
name: rust-tauri-app-performance
description: "Use when designing, implementing, optimizing, or reviewing Rust-backed Tauri desktop/mobile apps for Windows, Linux, macOS, iOS, or Android: Tauri v2 architecture, system webview tradeoffs, IPC commands/events/channels, mobile builds, app size, bundling/signing, frontend/backend boundaries, async Rust commands, state management, security capabilities, and cross-platform performance."
---

# Rust Tauri App Performance

Use this skill when Rust is the application backend and the target is a desktop or mobile UI through Tauri. Load `references/tauri-performance.md` for detailed guidance.

## Workflow

1. Confirm targets: Windows, Linux, macOS, iOS, Android, store distribution, signing, updater, and system webview dependencies.
2. Decide whether Tauri is the right shell: strong for Rust core plus web UI, weak for hard real-time rendering or native-only UI requirements.
3. Partition ownership: keep layout and reactive UI state in the frontend, and put CPU-heavy work, native APIs, secure storage, filesystem, networking, and long-running jobs in Rust.
4. Design coarse IPC: batch commands, avoid per-item `invoke`, use channels for streaming or high-volume progress, and reserve events for small state/lifecycle notifications.
5. Keep UI responsive: avoid blocking command handlers, run CPU work through bounded background execution, expose progress and cancellation, and keep async state explicit.
6. Tune release outputs: release profile, LTO/strip/panic strategy, unused command/plugin removal, frontend asset size, updater policy, and per-platform bundles.
7. Verify on every target in scope with startup time, bundle size, memory, IPC throughput, responsiveness, signing, and installer/store smoke tests.

## Routing

- Load `rust-performance-core` for profiling, Cargo profiles, allocations, startup time, and bundle size.
- Load `rust-async-concurrency` for async commands, background tasks, cancellation, and Rust channels.
- Load `rust-ffi-bindings` if the app integrates Swift, Kotlin, C, C++, or native platform SDKs.
- Load `rust-wasm-engineering` only when frontend code itself uses Rust/Wasm.
- Load `rust-ci-quality-gates` for Windows, Linux, macOS, iOS, and Android build/sign/test matrices.
- Load `rust-expert-rulebook` when reviewing IPC boundaries or cross-platform app architecture.

## Defaults

- Prefer Tauri commands for coarse request/response operations.
- Prefer Tauri channels for streaming data, progress, logs, or frequent Rust-to-frontend updates.
- Prefer events for small fan-out lifecycle messages, not low-latency or high-throughput data.
- Prefer lazy initialization for databases, model loading, caches, and network sessions unless startup requires them.
- Prefer least-privilege capabilities and validated command arguments because the frontend is an IPC client, not a trusted Rust caller.
- Treat mobile as a first-class target: `tauri android` and `tauri ios` have platform prerequisites, signing, permissions, and device testing requirements.

## Output

Include target platforms, why Tauri is or is not appropriate, frontend/Rust ownership split, IPC/channel boundary, state model, security capabilities, performance budget, bundle/signing plan, and exact verification commands.
