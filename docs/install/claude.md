# Claude Code And Anthropic-Style Install

## Skills-Only Mode

Copy the skill into Claude's skill directory:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/rust-* "$HOME/.claude/skills/"
```

Then invoke:

```text
Use $rust-performance-engineering to design this Rust market-data pipeline for low latency.
```

You can also invoke specialists directly:

```text
Use $rust-python-pyo3-maturin to speed up this Python bottleneck with Rust.
Use $rust-wasm-engineering to review this Wasm package for size and JS boundary cost.
```

## Project-Local Fallback

If the environment does not support installed skills, keep this repository in the project and add an instruction:

```text
For Rust performance tasks, read skills/rust-performance-engineering/SKILL.md and then load only the specialist skills and referenced files needed for the task.
```

For repository orientation, run `python3 scripts/rust_project_audit.py .` before reviewing.
