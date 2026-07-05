# Rust Performance Skills v6 Memory SIMD I/O Design

## Goal

Extend `rust-performance-skills` with specialist guidance and deterministic tooling for Rust hot paths dominated by memory movement, allocation lifetime, SIMD, and kernel/storage I/O.

## Scope

- Add `rust-memory-simd-io-performance`.
- Cover allocator selection, arenas, SoA/AoS, cache lines, false sharing, prefetching, SIMD, `core::arch`, `std::simd`, `memmap2`, `io-uring`, direct I/O, page faults, HugeTLB, NUMA, `bytemuck`, and `zerocopy`.
- Extend audit detection and MCP checklist generation for these signals.
- Add a maintainer eval and source-map entries using primary or official references.

## Constraints

- Keep advice measurement-first and avoid unconditional allocator, SIMD, huge-page, or NUMA recommendations.
- Keep MCP offline and deterministic.
- Do not add scripts that require root, kernel tuning, device access, or live benchmark execution.
- Preserve existing plugin install behavior and author identity.

## Verification

- Unit tests for distribution, audit, and MCP contracts.
- Plugin and skill validation.
- CI validation after push.
- Scan for private project identifiers before final report.
