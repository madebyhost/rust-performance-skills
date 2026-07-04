# Architecture For High-Performance Rust

Architecture should protect the hot path, not decorate it.

## Boundary Choices

- Domain-driven or onion architecture works well when business rules are complex and I/O adapters must change independently.
- Hexagonal architecture works well for services with external dependencies and testable ports.
- Pipeline architecture works well for streaming data with measurable stage latency and backpressure.
- Actor architecture works well when isolated mutable state and message flow are clearer than shared locks.
- ECS/data-oriented design works well when systems repeatedly scan large sets of homogeneous components.
- Disruptor-style design works for ordered, preallocated, low-latency event pipelines.

## Low-Latency Boundary Rule

Do not force every hot-path operation through trait objects, heap allocation, serialization boundaries, or async channels just to satisfy a broad architecture pattern.

Keep domain boundaries at places where they clarify ownership, testing, or I/O isolation. Keep the innermost loop mechanically simple.

## Recommended Shape

- Outer layer: configuration, I/O adapters, observability, persistence.
- Application layer: orchestration, retries, timeouts, policies.
- Domain layer: validated business rules and state transitions.
- Hot path module: compact data structures and algorithms with explicit contracts.

The hot path may be a specialized module inside the domain or data-plane layer. It should expose a clear safe API and hide layout-specific details.

## Design Review Questions

- Which code is on the hot path?
- Which abstractions compile away and which allocate or dispatch dynamically?
- Where are queues and backpressure boundaries?
- Can state be sharded by key, symbol, partition, connection, or strategy?
- Can cold-path concerns be moved out of the hot loop?
- Does the architecture preserve replay/testing?

## Red Flags

- overusing traits for every domain concept;
- async channels between every layer;
- serializing/deserializing between internal layers;
- hiding latency-critical logic behind dynamic plugin systems;
- making HFT loops depend on database, logging, or network clients directly.
