# Codex Install

## Plugin Mode

This repository contains a Codex plugin manifest:

```text
.codex-plugin/plugin.json
skills/rust-performance-engineering/SKILL.md
```

Install the repository through the Codex plugin flow available in your Codex environment. After installation, invoke:

```text
Use $rust-performance-engineering to review this Rust service for p99 latency and allocation pressure.
```

## Skills-Only Mode

Copy or sync `skills/rust-performance-engineering` into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/rust-performance-engineering "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex or reload skills if your environment requires it.
