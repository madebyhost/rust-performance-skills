# Testing Verification Matrix

## Correctness

- Unit tests: pure functions, invariants, boundary conditions, error paths.
- Integration tests: public API, crate features, CLI behavior, service adapters.
- Snapshot tests: stable text or binary formats only when churn is controlled.
- Golden fixtures: protocol frames, market-data packets, FFI payloads, Wasm boundary payloads.

## Safety

- Unsafe wrappers: test safe API boundaries, invalid input rejection, aliasing assumptions, drop behavior, and panic safety.
- Miri: run targeted tests for unsafe abstractions, parser logic, and pointer-heavy code.
- Sanitizers: use address/thread sanitizers where platform and dependencies support them.
- SAFETY comments: every unsafe block should state preconditions and caller/callee obligations.

## Parsers And Protocols

- Property tests: round trips, idempotence, monotonicity, bounds, and rejection of malformed data.
- Fuzzing: untrusted byte input, custom deserializers, network protocols, UDP multicast decoders, and FFI boundaries.
- Corpus: seed with real frames and edge cases, but keep secrets and production data out of the repository.

## Async And Concurrency

- Avoid sleep-based tests. Prefer controlled clocks, bounded channels, and explicit readiness signals.
- Use `loom` for small concurrency primitives, atomics, and lock-free designs.
- Test cancellation, backpressure, shutdown, queue saturation, and task failure propagation.

## Performance

- Benchmarks must state target hardware assumptions and noise expectations.
- Use Criterion for comparative benchmarks and iai-callgrind where instruction stability matters.
- For HFT-style paths, record p50/p95/p99/p999, drops, queue depth, warmup, and replay behavior.
