---
name: rust-architecture-patterns
description: "Use when choosing Rust architecture and design patterns: domain-driven design, onion, hexagonal, clean architecture, ECS, actor model, pipelines, disruptor pattern, plugin systems, module boundaries, hot-path exceptions, ownership boundaries, and domain modeling."
---

# Rust Architecture Patterns

Use this skill to choose architecture by constraints, not fashion. Load `references/architecture-patterns.md` for details.

## Workflow

1. Identify domain complexity, performance sensitivity, team size, and change rate.
2. Mark hot paths and cold paths.
3. Choose boundaries that preserve ownership clarity and testability.
4. Permit hot-path exceptions where abstraction cost is measurable or obvious.

## Output

State the chosen pattern, why alternatives were rejected, how modules communicate, where allocation/dispatch occurs, and how to test boundaries.
