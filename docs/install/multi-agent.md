# Multi-Agent Install

The default one-liner detects installed coding agents and installs static Rust
performance adapters for the agents it finds:

```bash
curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh
```

The installer keeps a durable shared bundle at:

```text
$HOME/.agents/rust-performance-skills
```

Agent-specific files point to that bundle, especially:

```text
skills/rust-performance-engineering/SKILL.md
rules/index.json
mcp/rust_performance_mcp.py
```

## Coverage

| Agent | Detection | Install surface |
| --- | --- | --- |
| Codex | `codex` or `$HOME/.codex` | `$HOME/.codex/skills`, plus Codex plugin marketplace when `codex` is present |
| Claude Code | `claude` or `$HOME/.claude` | `$HOME/.claude/skills` |
| Gemini CLI | `gemini` or `$HOME/.gemini` | `$HOME/.gemini/GEMINI.md` marker block |
| Cursor | `cursor` or `$HOME/.cursor` | `.cursor/rules/rust-performance-skills.mdc` |
| Windsurf | `windsurf` | `.windsurfrules` marker block |
| Cline | `cline` | `.clinerules` marker block |
| Roo Code | `roo` | `.roo/rules/rust-performance-skills.md` |
| Kilo Code | `kilocode` or `kilo-code` | `.kilocode/rules/rust-performance-skills.md` |
| Google Antigravity | `antigravity` | `.agents/rules/antigravity-rust-performance-skills.md` |
| Pi | `pi` or `$HOME/.pi` | `$HOME/.pi/agent/extensions/rust-performance-skills.md` |
| Hermes | `hermes` or `$HOME/.hermes` | `$HOME/.hermes/skills/rust-performance-skills` |
| OpenCode | `opencode` | `$HOME/.config/opencode/rust-performance-skills.md` |
| OpenClaw | `openclaw` or `$HOME/.openclaw` | `$HOME/.openclaw/skills/rust-performance-skills` |
| Ollama | `ollama` or `$HOME/.ollama` | `$HOME/.ollama/openclaw/rust-performance-skills.md` for Ollama-launched OpenClaw |
| GitHub Copilot | `copilot` or `github-copilot-cli` | `.github/copilot-instructions.md` marker block |

Ollama is treated as a model/runtime provider, not as a standalone coding
instruction host. Its adapter points Ollama-launched OpenClaw sessions at the
same installed Rust bundle.

## Explicit Agent Selection

Install for every supported adapter:

```bash
RUST_PERF_SKILLS_TARGET=agents RUST_PERF_SKILLS_AGENTS=all sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

Install a selected set:

```bash
RUST_PERF_SKILLS_TARGET=agents RUST_PERF_SKILLS_AGENTS=gemini,cursor,cline,roo,kilocode,hermes,openclaw,ollama sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

Install one adapter directly:

```bash
RUST_PERF_SKILLS_TARGET=cursor sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
RUST_PERF_SKILLS_TARGET=hermes sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
RUST_PERF_SKILLS_TARGET=openclaw sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

For project-level agents, set the target project explicitly when running the
one-liner outside the repository you want to configure:

```bash
RUST_PERF_SKILLS_PROJECT_DIR=/path/to/project RUST_PERF_SKILLS_TARGET=agents RUST_PERF_SKILLS_AGENTS=cursor,windsurf,cline,roo,kilocode,copilot sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

## Safety Model

- The installer writes static instruction files and skill directories.
- It does not install or patch agent hooks.
- It does not edit API keys, secrets, model provider configs, or shell startup
  files.
- Existing single-file instruction surfaces such as `GEMINI.md`,
  `.windsurfrules`, `.clinerules`, and Copilot instructions are updated with a
  marked block, preserving unrelated content.

The underlying helper is:

```bash
python3 scripts/install_agent_adapters.py --source . --prefix "$HOME" --project-dir . --agents auto
```

For Codex marketplace-only install, use:

```bash
RUST_PERF_SKILLS_TARGET=plugin sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

The Codex marketplace entry is `rust-performance-skills@personal`.
