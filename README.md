# Rust Performance Skills

Portable agent skills for building and reviewing high-performance Rust systems.

This repository packages a Codex-compatible plugin and a portable skill that can also be copied into Claude Code, other skill-aware coding agents, or project-local agent instructions. It focuses on real Rust performance work: measurement first, explicit latency budgets, allocation control, cache-aware data layout, async/runtime choices, concurrency, zero-copy, and low-latency/HFT patterns.

## What It Provides

- A Codex plugin manifest in `.codex-plugin/plugin.json`.
- A portable skill at `skills/rust-performance-engineering`.
- Reference playbooks for zero-copy, async, HFT/low-latency, architecture, measurement, and review.
- Install notes for Codex, Claude Code, and generic agents.
- CI validation for plugin metadata, skill frontmatter, and reference links.

## When To Use It

Use `$rust-performance-engineering` when an agent is asked to:

- design or review latency-sensitive Rust code;
- optimize async or multi-threaded Rust services;
- write zero-copy parsing, serialization, or networking code;
- build market-data, order-routing, HFT, telemetry, networking, or data-plane systems;
- choose between onion, hexagonal, ECS, actor, pipeline, or disruptor-style architecture;
- justify `unsafe`, lock-free data structures, CPU pinning, cache padding, or memory pools.

## Install

See:

- [Codex](docs/install/codex.md)
- [Claude Code and Anthropic-style agents](docs/install/claude.md)
- [Generic coding agents](docs/install/generic-agents.md)

## Design Principles

- Measure before optimizing.
- Treat latency budgets as contracts.
- Prefer mechanical sympathy over decorative abstractions.
- Keep zero-copy explicit and lifetime-safe.
- Isolate `unsafe` behind documented invariants and tests.
- Use async for concurrency, not as a blanket performance claim.
- Prefer bounded queues, backpressure, preallocation, and stable data layout in hot paths.

## MCP Status

The initial release is skill-first. `.mcp.json` is present so the repository can grow an optional MCP server later without changing the plugin shape. A future MCP can expose deterministic checks such as Cargo profile inspection, dependency audits, perf checklist generation, and benchmark report parsing.

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Keep advice measurable, Rust-specific, and actionable for coding agents.

## License

MIT. See [LICENSE](LICENSE).
