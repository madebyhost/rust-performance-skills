# Claude Code Plugin Install

Claude Code has two extension modes:

- standalone skills under `$HOME/.claude/skills`;
- plugins installed through a Claude marketplace.

Use the plugin path for this project. It keeps all Rust skills, the rulebook,
and the MCP server under one plugin entry that can be enabled or disabled
together from `/plugin` or the CLI.

## Plugin Mode

The default one-liner detects Claude Code when the `claude` command or
`$HOME/.claude` is present, creates a local marketplace, registers it, and
installs `rust-performance-skills@madebyhost-rust-performance`:

```bash
curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh
```

Explicit Claude plugin install:

```bash
RUST_PERF_SKILLS_TARGET=claude sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

This runs the Claude plugin flow:

```bash
claude plugin marketplace add "$HOME/.claude/rust-performance-skills-marketplace"
claude plugin install rust-performance-skills@madebyhost-rust-performance --scope user
```

Manage the whole package as one plugin:

```bash
claude plugin list
claude plugin details rust-performance-skills@madebyhost-rust-performance
claude plugin disable rust-performance-skills@madebyhost-rust-performance
claude plugin enable rust-performance-skills@madebyhost-rust-performance
```

After install, invoke namespaced skills:

```text
/rust-performance-skills:rust-performance-engineering
/rust-performance-skills:rust-python-pyo3-maturin
/rust-performance-skills:rust-wasm-engineering
```

The public marketplace entry is also available in this repository at
`.claude-plugin/marketplace.json`, and the Claude plugin root is
`claude-plugin/rust-performance-skills`.

## Skills-Only Fallback

Use this only when the local Claude Code version does not support plugins or
when you explicitly want standalone global skills:

```bash
RUST_PERF_SKILLS_TARGET=claude-skills sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

Standalone skills are invoked without the plugin namespace:

```text
Use $rust-performance-engineering to design this Rust market-data pipeline for low latency.
```

They will not disappear when the Claude plugin is disabled. To migrate away
from a previous standalone install, use the opt-in cleanup:

```bash
RUST_PERF_SKILLS_TARGET=claude RUST_PERF_SKILLS_CLAUDE_CLEAN_STANDALONE=1 sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
```

The cleanup only removes matching `$HOME/.claude/skills/rust-*` folders.

## Project-Local Fallback

If the environment does not support installed skills, keep this repository in the project and add an instruction:

```text
For Rust performance tasks, read skills/rust-performance-engineering/SKILL.md and then load only the specialist skills and referenced files needed for the task.
```

For repository orientation, run `python3 scripts/rust_project_audit.py .` before reviewing.
Use `python3 scripts/generate_quality_gates.py audit.json` after saving audit JSON to produce CI suggestions for Rust, PyO3/maturin, and Wasm projects.
The installer entrypoint is `install.sh`.
