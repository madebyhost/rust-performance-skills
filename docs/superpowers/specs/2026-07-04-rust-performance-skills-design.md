# Rust Performance Skills Design

## Goal

Create an open-source, portable Rust performance engineering skill distribution for Codex, Claude Code, and other coding agents.

## Architecture

The repository is skill-first and plugin-compatible. Codex reads `.codex-plugin/plugin.json` and loads the `skills/` directory. Other agents can copy the same skill folder or use project-local instructions. MCP support is intentionally a documented extension point in v1 instead of a heavy runtime dependency.

## Components

- `.codex-plugin/plugin.json`: Codex plugin metadata.
- `skills/rust-performance-engineering/SKILL.md`: entrypoint and routing workflow.
- `skills/rust-performance-engineering/references/`: detailed performance playbooks loaded only when relevant.
- `docs/install/`: installation notes for Codex, Claude, and generic agents.
- `scripts/validate_distribution.py`: deterministic repository validation.
- `.github/workflows/ci.yml`: CI validation for open-source contributions.

## Design Rules

The skill must force measurement-first performance work, avoid cargo-cult optimization, and make tradeoffs explicit. It should support HFT and ultra-low-latency work without making those patterns the default for every Rust project.

## Initial Scope

The initial release includes the skill, Codex plugin metadata, multi-agent install docs, contribution docs, and CI. The MCP remains a roadmap because most useful behavior is procedural and architectural rather than a deterministic tool call.
