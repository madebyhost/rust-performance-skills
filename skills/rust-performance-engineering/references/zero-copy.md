# Zero-Copy Rust

Zero-copy is a data ownership design, not a keyword.

## Use Zero-Copy When

- payloads are large or frequent enough that copying shows up in profiles;
- ownership boundaries are clear;
- the source buffer outlives all borrowed views;
- mutation is not required or can be isolated;
- parsing can validate before exposing borrowed structures.

## Preferred Patterns

- Borrowed input APIs: `fn parse(input: &[u8]) -> Result<View<'_>, Error>`.
- Shared immutable buffers: `bytes::Bytes` for network payloads that cross async tasks.
- Offset-based views: store ranges into an owned buffer instead of self-referential structs.
- Streaming decode: parse fields as needed instead of materializing all intermediate structures.
- `Cow<'a, str>` only when both borrowed and owned cases are real.
- mmap for large read-only files when OS page-cache behavior fits the workload.

## Serialization And Parsing

- Prefer serde borrowing only when input lifetimes are easy to carry.
- For JSON hot paths, benchmark `serde_json`, `simd-json`, and schema changes.
- For binary protocols, prefer explicit endian-aware parsing and range checks.
- Avoid `String` for protocol fields unless ownership and UTF-8 validation are required.

## Red Flags

- `.to_vec()`, `.to_string()`, `.clone()` in the hot path.
- Parsing into owned DTOs and immediately converting again.
- Returning borrowed data tied to a temporary buffer.
- `Arc<Vec<u8>>` used where `Bytes` or `Arc<[u8]>` gives clearer ownership.
- Self-referential structs introduced to avoid a simple offset table.

## Verification

- Count allocations and copied bytes.
- Benchmark representative message sizes and batch sizes.
- Test lifetime boundaries with async handoff and queueing.
- Include malformed-input tests to preserve validation before borrowed access.
