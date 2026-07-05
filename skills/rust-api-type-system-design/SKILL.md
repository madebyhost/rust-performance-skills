---
name: rust-api-type-system-design
description: "Use when designing, reviewing, or refactoring Rust public APIs and type-system boundaries: newtypes, validated constructors, typestate, PhantomData, sealed traits, generics vs dyn Trait, object safety, From/TryFrom/FromStr, serde compatibility, pattern matching, macro hygiene, feature flags, cfgs, naming, and semver-sensitive API rules."
---

# Rust API Type System Design

Use this skill when correctness should be encoded in Rust's API and type system before runtime checks or performance tuning. Load `references/api-type-system-design.md` for detailed review rules.

## Workflow

1. Identify the boundary: public crate API, internal module API, config/serde DTO, protocol type, macro API, or domain model.
2. Parse constraints into types: validated newtypes, enums, typestate, sealed traits, or explicit fallible conversions.
3. Choose dispatch deliberately: concrete type, generic `impl Trait`, associated type, enum, or `dyn Trait`.
4. Preserve compatibility: feature flags must be additive, serde defaults must be intentional, and public enum/struct evolution must be planned.
5. Verify with compile-fail tests, serde compatibility fixtures, property tests, docs, clippy, semver checks, and examples.

## Defaults

- Prefer "parse, don't validate" at system boundaries.
- Prefer newtypes for IDs, money, units, validated strings, handles, and domain-specific numbers.
- Use typestate only when the state machine is real and the added types reduce invalid transitions.
- Seal public traits when external implementations would block future evolution or weaken invariants.
- Use exhaustive matches for enums you own; document wildcard arms for foreign `#[non_exhaustive]` enums.
- Use `$crate` and hidden helpers for exported macros.
- Gate serde and heavy integrations behind additive features for libraries.

## Output

Return boundary classification, invariant encoding, dispatch choice, serde/feature compatibility risks, macro or pattern-matching risks, semver impact, and verification commands.
