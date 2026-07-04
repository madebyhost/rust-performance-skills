# Low-Latency HFT Reference

## Hot Path Rules

- No allocation after warmup unless measured and accepted.
- No formatting/logging in the decision loop.
- Preallocate events, order state, and scratch buffers.
- Avoid global locks; shard by symbol, venue, partition, or strategy.
- Keep recovery and audit correctness separate from hot decision code.

## Market Data

- UDP multicast designs need sequence checks, gap detection, snapshot recovery, and replay.
- Kernel bypass is operationally expensive; measure socket tuning first.
- Timestamp source and clock sync assumptions must be explicit.

## Mechanical Sympathy

- Pad contended atomics and producer/consumer indexes.
- Split hot/cold fields.
- Prefer compact SoA/AoS according to access pattern.
- Consider NUMA locality only when deployment controls sockets and allocation.

## Verification

- Replay captured data at normal and burst rates.
- Report p50/p95/p99/p999/max, drops, queue depth, CPU, and sequence gaps.
- Test packet loss, reconnect, replay, and kill-switch behavior.
