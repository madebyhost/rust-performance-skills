# Contributing

This project is meant to improve how coding agents work on performance-sensitive Rust code.

## Contribution Rules

- Prefer actionable guidance over broad Rust tutorials.
- Include tradeoffs. Performance rules without constraints are usually wrong.
- Explain when a pattern should not be used.
- Keep `SKILL.md` concise. Put detailed domain material in `references/`.
- Do not recommend `unsafe` as a default optimization path.
- Cite primary or stable references when adding facts that depend on external tools or platform behavior.

## Local Validation

Run:

```bash
python3 scripts/validate_distribution.py
```

The validator checks the Codex plugin manifest, skill frontmatter, reference links, and install docs.

## Adding A Reference

1. Add a focused file under `skills/rust-performance-engineering/references/`.
2. Link it from `skills/rust-performance-engineering/SKILL.md`.
3. Add practical review questions and red flags.
4. Run validation.

## Review Standard

A good contribution helps an agent produce better Rust code under real constraints: lower tail latency, lower allocation pressure, clearer concurrency boundaries, safer memory handling, or better architectural fit.
