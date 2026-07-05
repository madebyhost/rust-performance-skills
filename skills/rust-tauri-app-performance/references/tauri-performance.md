# Tauri Performance Reference

## Fit

Tauri is a strong fit when the app needs a Rust core, a web UI, native platform integration, small distribution artifacts, and one product surface across Windows, Linux, macOS, iOS, and Android. It uses the platform system webview instead of embedding a browser engine, so bundle size and native integration can be better than heavy desktop shells.

Tauri is a weak fit when the main requirement is hard real-time rendering, game-style frame loops, platform-native UI widgets only, or ultra-low-latency UI events where the webview and IPC boundary dominate the budget.

## Platform Matrix

- Windows: test WebView2 availability, installer behavior, code signing, auto-update, filesystem paths, tray/menu behavior, and GPU/WebView differences.
- Linux: test the target distribution family, webkit dependencies, AppImage/deb/rpm packaging assumptions, sandboxing, permissions, tray/menu support, and desktop portal behavior.
- macOS: test signing, notarization, app sandboxing when relevant, bundle metadata, menu behavior, and universal or target-specific binaries.
- iOS: treat mobile as a separate product target with Apple signing, provisioning, simulator/device testing, permissions, app lifecycle, and store review constraints.
- Android: configure Android Studio, SDK, NDK, env vars, device/emulator testing, permissions, ABI targets, signing, and Play Store packaging.

Use `cargo tauri dev` and `cargo tauri build` for desktop iteration and release bundles. Use `cargo tauri android dev`, `cargo tauri android build`, `cargo tauri ios dev`, and `cargo tauri ios build` when mobile targets are in scope.

## Process Model

Tauri apps are multi-process systems with a Rust core process and one or more webview processes. The Rust process owns native capabilities and command handlers. The webview owns rendering, layout, frontend state, and user interaction.

Do not run long blocking work in a command handler on a path that can stall UI responsiveness. Move CPU-heavy work to bounded background execution, expose progress and cancellation, and keep shared state behind explicit synchronization. For async commands, design cancellation and shutdown behavior instead of leaving detached tasks.

## IPC

Treat IPC as an API boundary. Commands are good for coarse request/response operations. Avoid one `invoke` per record, row, pixel, packet, or progress tick. Batch requests and return compact payloads.

Events are useful for lifecycle notifications, small state changes, and fan-out messages. They are fire-and-forget and should not be the default for low latency or high throughput data.

Tauri channels are the preferred path for streaming data, progress, logs, incremental search results, or high-volume Rust-to-frontend communication. Channels still cross a serialization and scheduling boundary, so measure message count, bytes transferred, queue depth, UI frame time, and cancellation behavior.

Prefer typed command payloads with `serde` structs. Validate every argument from the frontend. Avoid exposing raw filesystem, shell, HTTP, or database access as generic commands.

## State And Work Partitioning

Keep frontend state in the frontend when it exists only to render UI. Keep domain state, credentials, native handles, secure storage, database pools, and long-running sessions in Rust. Prefer `State<T>` with explicit `Arc` ownership over global mutable state.

Use async locks only around short critical sections. Do not hold locks while awaiting frontend calls, file I/O, network I/O, or long CPU work. For CPU-heavy work, consider Rayon or a bounded blocking pool and return progress through channels.

## Startup And Bundle Size

Track startup time, time to first useful screen, peak memory, frontend asset size, Rust binary size, installer size, and updater payload size.

Use release profiles intentionally. Evaluate LTO, `codegen-units = 1`, `strip`, `panic = "abort"`, and `opt-level = "z"` or `"s"` when bundle size matters. Remove unused Tauri commands, plugins, crate features, frontend dependencies, static assets, and debug artifacts.

Defer database migrations, cache warmup, model loading, network login, and telemetry setup unless they are required before the first screen. Prefer lazy initialization plus visible progress and cancellation for expensive first-run work.

## Frontend Assets

The webview is still a frontend runtime. Measure JavaScript bundle size, CSS size, image/font size, hydration time, route-level code splitting, and memory. Avoid large UI dependencies when the app is a utility or data tool. Use virtualized lists and incremental rendering for large datasets.

Do not pass huge datasets to the frontend for filtering or sorting unless the UI owns that interaction. Keep heavy filtering, parsing, indexing, compression, crypto, and native I/O in Rust and expose coarse commands or channel streams.

## Security

Use least-privilege capabilities and plugins. Validate all frontend-originating command inputs. Prefer domain-specific commands over generic `run_shell`, `read_file`, `write_file`, `request_url`, or `sql` commands.

Keep secrets in Rust/native secure storage. Never inject secrets into the frontend unless the frontend truly must display or transmit them. Treat the webview as a client across IPC.

## Verification

- Desktop smoke: `cargo tauri dev` on each desktop OS in scope.
- Desktop release: `cargo tauri build` plus installer/bundle launch tests.
- Android smoke: `cargo tauri android dev` on emulator and at least one physical device when possible.
- Android release: `cargo tauri android build` plus signing and permission checks.
- iOS smoke: `cargo tauri ios dev` on simulator and device when possible.
- iOS release: `cargo tauri ios build` plus signing/provisioning checks.
- Rust quality: `cargo test`, `cargo clippy --all-targets --all-features`, and target-specific integration tests.
- Performance: startup time, memory, bundle size, IPC message rate, bytes per message, command latency, channel backlog, UI frame time, and cancellation behavior.

## Sources

- Tauri v2: https://v2.tauri.app/start/
- Tauri process model: https://v2.tauri.app/concept/process-model/
- Tauri IPC: https://v2.tauri.app/concept/inter-process-communication/
- Tauri app size: https://v2.tauri.app/concept/size/
- Tauri mobile prerequisites: https://v2.tauri.app/start/prerequisites/
- Tauri distribution: https://v2.tauri.app/distribute/
- Tauri Rust to frontend communication: https://v2.tauri.app/develop/calling-frontend/
- Tauri configuration files: https://v2.tauri.app/develop/configuration-files/
