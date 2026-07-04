# Eval: Unsafe Soundness

Ask the agent to review a crate that wraps an unsafe pointer-based parser in a safe API.

Expected behavior:

- Loads `rust-unsafe-soundness`, `rust-testing-verification`, and `rust-ci-quality-gates`.
- Demands explicit invariants, SAFETY comments, panic/drop behavior, aliasing rules, and safe wrapper boundaries.
- Recommends targeted Miri tests, fuzzing for untrusted input, and normal tests before performance claims.
