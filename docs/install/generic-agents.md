# Generic Agent Install

Any coding agent can use this repository if it supports one of these patterns:

- installed skills;
- project-local instruction files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`;
- explicit prompt references to files.

## Portable Prompt

Use:

```text
Use the Rust performance skill at skills/rust-performance-engineering/SKILL.md. Load only the references needed for this task, then design or review the Rust code with measurement-first performance reasoning.
```

## Expected Agent Behavior

The agent should:

- inspect real Rust code and configuration before recommending changes;
- identify the performance contract or ask for it;
- route to relevant references;
- explain tradeoffs and verification;
- avoid `unsafe`, lock-free structures, CPU pinning, and kernel tuning unless the constraint justifies them.
