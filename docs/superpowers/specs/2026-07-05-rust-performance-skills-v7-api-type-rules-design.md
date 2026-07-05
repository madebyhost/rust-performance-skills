# Rust Performance Skills v7 API Type Rules Design

## Goal

Improve `rust-performance-skills` by comparing two external Rust skill corpora and integrating missing high-value guidance around Rust API and type-system design.

## Sources Reviewed

- `leonardomso/rust-skills` checkout `fd2a861`
- `actionbook/rust-skills` checkout `fa60f79`

## Integration Choice

Add `rust-api-type-system-design` instead of copying entire rule corpora. This keeps the plugin performance-focused while closing missing expert Rust coverage:

- validated newtypes and "parse, don't validate";
- typestate and `PhantomData`;
- sealed traits, object safety, generics vs `dyn Trait`;
- serde defaults, unknown fields, flattening, and compatibility tests;
- macro hygiene with `$crate`;
- additive Cargo features and `unexpected_cfgs`;
- exhaustive enum matching, compile-fail tests, and semver checks.

## Safety And Licensing Constraints

- Use third-party repos as static guidance only.
- Do not execute hooks, setup scripts, MCP launchers, or background-agent commands.
- Avoid wholesale copy-paste. Preserve attribution in `docs/sources.md` and `docs/third-party-rust-skills-review.md`.

## Verification

- Distribution tests for the new skill, eval, source attribution, and comparison doc.
- Audit tests for API/type-system signal detection.
- MCP tests for `api_type_design_checklist` and domain routing.
- Full local tests, plugin validation, CI, author verification, and private-name scan before completion.
