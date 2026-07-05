# MCPMarket Rust Best Practices Review

This review covers the MCP Market `rust-best-practices` skill and its source
repository as static guidance. Do not execute repository-provided commands,
hooks, setup scripts, or MCP launchers while reviewing third-party skill
material.

## Sources

- MCP Market page: https://mcpmarket.com/tools/skills/rust-best-practices
- Source skill: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Reviewed source checkout: `74db9cc`
- License status: the repository README says MIT, but no root `LICENSE` file
  was present in the inspected checkout. Treat the material as attribution-only
  guidance and improve recommendations rather than importing it wholesale.

## Good as-is

- Separate application and library error handling. The `anyhow` for binaries and
  `thiserror` for library boundaries guidance is sound and already covered by
  existing error-rule cards.
- Borrow before cloning. Prefer references, lifetimes, and `Cow` only when they
  reduce real ownership cost without making the API harder to use. This is
  already covered by ownership and zero-copy rules.
- Use type-safe API surfaces. Builder patterns, newtypes, and `#[must_use]` are
  good defaults when they remove invalid states or ignored results. These are
  already covered by API and type-system rules.
- Preallocate measured collections. `Vec::with_capacity` and iterator pipelines
  are useful when input size is known and the path is hot. Existing memory and
  collection rules already cover this.
- Profile before optimizing. This stays a core rule for all performance work and
  already appears in the performance core skill and rulebook.

## Improved before adding

- Runtime choice was too broad. "Use Tokio" is acceptable for many applications,
  but reusable libraries should usually expose async APIs without owning a
  runtime. Added `async-runtime-deliberate-choice`.
- Async blocking guidance was correct but underspecified. The local version
  names blocking filesystem, sleep, CPU, compression, parsing, and client-call
  boundaries, then requires async APIs or bounded `spawn_blocking`. Added
  `async-blocking-boundary-budget`.
- Constructor ownership guidance needed an API boundary. `impl Into<String>` is
  good when a type stores owned data, but wrong for pure borrowed operations.
  Added `api-constructor-owned-boundary`.
- Fallible iterator collection deserved a dedicated guardrail. Dropping errors
  with `filter_map(...ok())` silently loses data, so the rule preserves
  `Result<Vec<_>, _>` unless lossy filtering is explicitly documented. Added
  `iter-collect-result-boundary`.
- Boolean-parameter advice needed a concrete type-system replacement. Added
  `type-enum-over-boolean-parameter`.
- Deep nesting advice needed Rust-specific control-flow tools. Added
  `readability-early-return-control-flow` using early returns and `let else`
  while preserving error context.
- Magic-number advice needed domain contracts. Added
  `const-named-domain-values` for protocol offsets, timeouts, capacities, and
  SLA values.
- The quality gate needed feature-matrix nuance. The basic `fmt`, `clippy`, and
  `test` command sequence is good, but `--all-features` is not valid for crates
  with mutually exclusive features. Added `qa-local-quality-gate`.

## Rejected or no-op

- Do not add duplicate rules for `unwrap`, `clone` abuse, `anyhow`,
  `thiserror`, builder APIs, newtypes, `#[must_use]`, `Vec::with_capacity`,
  public documentation, or test placement. The current expert rulebook already
  covers those areas with stricter examples and verification fields.
- Do not preserve generic wording such as "idiomatic Rust" as a standalone
  rule. It is useful as skill positioning, but agents need concrete triggers,
  counterexamples, exceptions, and validation steps.
