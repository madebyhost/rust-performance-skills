---
name: rust-sbe-binary-codecs
description: "Use when designing, implementing, or reviewing Rust Simple Binary Encoding (SBE), fixed-layout binary codecs, market-data/order-flow wire formats, zero-copy encode/decode, flyweight views, endian/alignment handling, schema evolution, golden frames, and low-latency serialization."
---

# Rust SBE Binary Codecs

Use this skill when binary wire layout and codec cost matter. Load `references/sbe-binary-codecs.md` for schema, decode, and compatibility checks.

## Workflow

1. Define the wire contract: schema id, template id, block length, versioning, endian, optional fields, and repeating groups.
2. Keep hot decode as borrowed views over bytes when lifetime and bounds are explicit.
3. Separate wire structs from domain structs; convert only at boundaries that justify allocation.
4. Optimize cursor movement, branch count, bounds checks, batch decode, and fixed-width fields before using unsafe.
5. Verify with golden frames, round trips, fuzzing, schema compatibility, and replay-like benchmarks.

## Defaults

- Prefer fixed-width fields in hot paths.
- Prefer explicit endian reads/writes and measured conversion cost.
- Avoid per-message allocation and string parsing in hot loops.
- Treat "zero-copy" as false if fields are copied into owned domain objects before use.
- Keep schema evolution backward/forward compatibility visible in tests.

## Output

Return schema layout risks, decode/encode design, zero-copy boundary, compatibility strategy, benchmark plan, and exact verification commands.
