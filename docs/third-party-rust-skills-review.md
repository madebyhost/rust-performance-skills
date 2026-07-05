# Third-Party Rust Skills Review

This project periodically reviews external Rust skill collections for coverage gaps. The review uses static guidance only: do not execute hooks, setup scripts, MCP launchers, background agents, or repository-provided commands from the inspected projects.

## leonardomso/rust-skills

- Repository: https://github.com/leonardomso/rust-skills
- Reviewed checkout: `fd2a861`
- License file present: MIT.
- Useful coverage: fine-grained rule catalog for ownership, errors, memory, unsafe, API design, async, concurrency, optimization, numeric safety, type safety, traits/generics, conversions, const, serde, pattern matching, macros, closures, collections, naming, testing, docs, observability, project structure, linting, and anti-patterns.
- Adopted direction: add a focused API/type-system skill rather than copying the rule corpus. The integrated guidance covers validated newtypes, typestate, sealed traits, generics vs `dyn Trait`, serde compatibility, macro hygiene, additive features, `unexpected_cfgs`, exhaustive matches, compile-fail tests, and semver checks.

## actionbook/rust-skills

- Repository: https://github.com/actionbook/rust-skills
- Reviewed checkout: `fa60f79`
- License status in checkout: README and metadata claim MIT, but no `LICENSE` file was present in the inspected checkout.
- Useful coverage: cognitive layer routing from language mechanics to design choices and domain constraints; domain-specific prompts for FinTech, embedded, ML, cloud-native, IoT, web, and CLI work; explicit "do not just clone" style reasoning for ownership errors.
- Adopted direction: use the reasoning shape as static inspiration for router/review behavior, especially "compiler error -> design constraint -> domain rule". Do not import hook behavior, background agents, `.mcp.json`, achievement scripts, `agent-browser`, or automatic setup.

## Gaps Closed In This Repository

- Added `rust-api-type-system-design` for API and type-system boundaries that were too broad in `rust-code-quality`.
- Added audit detection for API/type-system design signals.
- Added MCP checklist support for API/type design.
- Added source attribution so maintainers can trace why these rules exist.

## Non-Goals

- No wholesale copy of either repository.
- No execution of third-party hooks, scripts, or MCP launchers.
- No dependency on third-party runtime services for this plugin.
