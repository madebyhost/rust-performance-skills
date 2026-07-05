# Eval: Tauri Cross-Platform App

Prompt:

> Use $rust-performance-engineering to design a Rust-backed Tauri app for Windows, Linux, macOS, iOS, and Android. The app streams local telemetry from Rust to the UI, stores encrypted credentials, supports long-running imports, and must keep startup under 800 ms with a small bundle size. Explain the architecture, IPC boundary, channels, mobile caveats, release plan, and verification strategy.

Expected high-quality answer:

- Loads `rust-tauri-app-performance`, `rust-performance-core`, `rust-async-concurrency`, `rust-ci-quality-gates`, and `rust-expert-rulebook` when rule IDs are useful.
- States whether Tauri is appropriate and calls out the system webview, desktop/mobile target differences, and app-store/signing constraints.
- Designs coarse IPC commands and Tauri channels for streaming instead of per-item invoke calls.
- Separates frontend UI state from Rust domain/native state, validates command inputs, and uses least-privilege capabilities.
- Defines startup time, bundle size, memory, IPC throughput, channel backlog, and UI responsiveness measurements.
- Includes `cargo tauri build`, `cargo tauri android build`, `cargo tauri ios build`, and per-platform smoke tests.
