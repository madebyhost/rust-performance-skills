# Eval: SBE Market Data Codec

Ask the agent to review a Rust market-data decoder using SBE-style headers, repeating groups, and owned conversions.

Expected behavior:

- Loads `rust-sbe-binary-codecs`, `rust-low-latency-hft`, and `rust-testing-verification`.
- Identifies schema id, template id, block length, acting version, endian, bounds, and group-count risks.
- Rejects false zero-copy claims when per-field allocation occurs.
- Recommends golden frames, fuzzing, round trips, and replay benchmarks.
