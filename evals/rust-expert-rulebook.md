# Rust Expert Rulebook Eval

Use this eval to verify that an agent uses concrete rule IDs instead of generic Rust advice.

## Prompt

Review a Rust feed-handler module that allocates a `Vec<u8>` per UDP multicast packet, decodes SBE frames into owned `String` fields, holds a Tokio mutex across `.await`, uses `unwrap()` in production parsing, and exports a broad public trait without sealing.

## Expected Behavior

- Cite specific rule IDs such as `hft-udp-multicast-hotpath`, `sbe-zero-copy-lifetime`, `mem-zero-copy`, `async-no-lock-await`, `anti-unwrap-abuse`, and `api-sealed-trait`.
- Include at least one `bad` versus `good` rewrite pattern.
- Apply `when_not` caveats for zero-copy and disruptor-style architecture.
- Require verification through allocation counts, packet-drop counters, golden SBE frames, async lock-scope tests, and latency measurements.
