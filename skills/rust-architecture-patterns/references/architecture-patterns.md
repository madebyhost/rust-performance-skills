# Architecture Patterns Reference

## Pattern Fit

- Onion/DDD: complex business rules and stable domain vocabulary.
- Hexagonal: external adapters and testable ports.
- Actor: isolated mutable state and message flow.
- Pipeline: streaming workloads with stage metrics and backpressure.
- ECS/data-oriented: repeated scans over homogeneous components.
- Disruptor: ordered, preallocated, low-latency event fanout.

## Rust-Specific Boundary Rules

- Do not hide every concept behind a trait.
- Prefer concrete types until multiple implementations exist.
- Keep serialization out of internal hot boundaries.
- Use ownership transfer to simplify lifetimes.
- Split hot and cold modules when performance matters.

## Hot-Path Exception

It is acceptable for a hot module to be less abstract if it exposes a clear safe API, is tested by replay/benchmarks, and documents layout/performance assumptions.
