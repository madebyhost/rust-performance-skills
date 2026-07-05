# SBE Binary Codecs Reference

## Schema Design

- Keep hot fields fixed-width and close together.
- Use repeating groups deliberately; document cardinality and bounds.
- Version with explicit schema id, template id, block length, acting version, and semantic compatibility notes.
- Prefer numeric enums and compact IDs over strings on hot paths.

## Decode Path

- Parse message header once.
- Validate block length and template id before reading body.
- Use borrowed byte slices or flyweight views while lifetimes remain simple.
- Batch decode where possible to amortize checks and dispatch.
- Convert to domain objects only after filtering, routing, or aggregation.

## Encode Path

- Preallocate output buffers and reuse them.
- Write fields in wire order.
- Keep endian handling explicit.
- Avoid formatting and heap allocation in the encode loop.

## Verification

- Golden frames for representative messages and schema versions.
- Round-trip tests for supported schema versions.
- Fuzz malformed length, version, group count, enum, and optional-field cases.
- Benchmarks with realistic message mixes, not one tiny happy-path message.

## Red Flags

- "Zero-copy" claim but `String`, `Vec`, or owned domain conversion happens per field.
- Bounds checks hidden behind panic-prone indexing.
- Schema changes without golden-frame compatibility tests.
- One decoder path for every message type causing unpredictable branches in the hottest loop.
