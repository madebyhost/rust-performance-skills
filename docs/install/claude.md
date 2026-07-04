# Claude Code And Anthropic-Style Install

## Skills-Only Mode

Copy the skill into Claude's skill directory:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/rust-performance-engineering "$HOME/.claude/skills/"
```

Then invoke:

```text
Use $rust-performance-engineering to design this Rust market-data pipeline for low latency.
```

## Project-Local Fallback

If the environment does not support installed skills, keep this repository in the project and add an instruction:

```text
For Rust performance tasks, read skills/rust-performance-engineering/SKILL.md and then load only the referenced files needed for the task.
```
