# Generic Agent Install

Any coding agent can use this repository if it supports one of these patterns:

- installed skills;
- project-local instruction files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`;
- explicit prompt references to files.

For agents with known instruction surfaces, prefer the multi-agent installer:

```bash
curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh
```

It detects Codex, Claude Code, Gemini CLI, Cursor, Windsurf, Cline, Roo Code,
Kilo Code, Google Antigravity, Pi, Hermes, OpenCode, OpenClaw, Ollama-launched
OpenClaw, and GitHub Copilot. Claude Code is installed as a real plugin through
a local marketplace, not as loose standalone skills. See
`docs/install/multi-agent.md`.

One-liner local/project fallback:

```bash
RUST_PERF_SKILLS_TARGET=local sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

For Codex plugin marketplace installation, use:

```bash
RUST_PERF_SKILLS_TARGET=plugin sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

The Codex marketplace entry is `rust-performance-skills@personal`.

## Portable Prompt

Use:

```text
Use the Rust performance router at skills/rust-performance-engineering/SKILL.md. Load only the specialist skills and references needed for this task, then design or review the Rust code with measurement-first performance reasoning.
```

For Python acceleration, load `skills/rust-python-pyo3-maturin/SKILL.md` for PyO3/maturin. For WebAssembly, load `skills/rust-wasm-engineering/SKILL.md` for Wasm guidance.

## Expected Agent Behavior

The agent should:

- inspect real Rust code and configuration before recommending changes;
- identify the performance contract or ask for it;
- route to relevant references;
- explain tradeoffs and verification;
- avoid `unsafe`, lock-free structures, CPU pinning, and kernel tuning unless the constraint justifies them.

## Audit Helper

Agents that can run commands should start with:

```bash
python3 scripts/rust_project_audit.py . --json
```

Use the JSON output to decide whether PyO3/maturin, Wasm, unsafe, FFI, or low-latency skills should be loaded.
Then run `python3 scripts/generate_quality_gates.py audit.json` to produce a quality-gate command set. The installer entrypoint is `install.sh`.
