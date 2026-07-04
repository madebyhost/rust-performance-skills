# Codex Install

## Plugin Mode

This repository contains a Codex plugin manifest:

```text
.codex-plugin/plugin.json
skills/rust-performance-engineering/SKILL.md
skills/rust-python-pyo3-maturin/SKILL.md
skills/rust-wasm-engineering/SKILL.md
```

Install the repository through the Codex plugin flow available in your Codex environment. After installation, invoke:

```text
Use $rust-performance-engineering to review this Rust service for p99 latency and allocation pressure.
```

The router can then load specialist skills such as `$rust-python-pyo3-maturin` for PyO3/maturin, `$rust-wasm-engineering` for Wasm, and `$rust-review-auditor` for PR review.

## Skills-Only Mode

Copy or sync `skills/rust-performance-engineering` into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/rust-* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex or reload skills if your environment requires it.

## Audit Helper

For repository orientation, run:

```bash
python3 scripts/rust_project_audit.py /path/to/rust/project
```

This reports Rust, PyO3/maturin, Wasm, unsafe, and low-latency signals for the agent to inspect.
