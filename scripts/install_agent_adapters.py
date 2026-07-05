#!/usr/bin/env python3
"""Install static rust-performance-skills adapters for multiple coding agents."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


PLUGIN_NAME = "rust-performance-skills"
CLAUDE_MARKETPLACE_NAME = "madebyhost-rust-performance"
ROUTER_SKILL = "rust-performance-engineering"
MARKER_START = "<!-- rust-performance-skills:start -->"
MARKER_END = "<!-- rust-performance-skills:end -->"

AGENT_ALIASES = {
    "anthropic": "claude",
    "claude-code": "claude",
    "codex-cli": "codex",
    "gemini-cli": "gemini",
    "roo-code": "roo",
    "roo_code": "roo",
    "kilo": "kilocode",
    "kilo-code": "kilocode",
    "google-antigravity": "antigravity",
    "open-code": "opencode",
    "open-code-cli": "opencode",
    "claw": "openclaw",
    "open-claw": "openclaw",
    "ollamma": "ollama",
    "github-copilot": "copilot",
}

KNOWN_AGENTS = [
    "codex",
    "claude",
    "gemini",
    "cursor",
    "windsurf",
    "cline",
    "roo",
    "kilocode",
    "antigravity",
    "pi",
    "hermes",
    "opencode",
    "openclaw",
    "ollama",
    "copilot",
]

COMMAND_DETECTION = {
    "codex": ["codex"],
    "claude": ["claude"],
    "gemini": ["gemini"],
    "cursor": ["cursor"],
    "windsurf": ["windsurf"],
    "cline": ["cline"],
    "roo": ["roo"],
    "kilocode": ["kilocode", "kilo-code"],
    "antigravity": ["antigravity"],
    "pi": ["pi"],
    "hermes": ["hermes"],
    "opencode": ["opencode"],
    "openclaw": ["openclaw"],
    "ollama": ["ollama"],
    "copilot": ["copilot", "github-copilot-cli"],
}

DIRECTORY_DETECTION = {
    "codex": [".codex"],
    "claude": [".claude"],
    "gemini": [".gemini"],
    "cursor": [".cursor"],
    "hermes": [".hermes"],
    "openclaw": [".openclaw"],
    "ollama": [".ollama"],
    "pi": [".pi"],
}


def parse_agents(value: str, prefix: Path) -> list[str]:
    requested = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not requested or requested == ["auto"]:
        return detect_agents(prefix)
    if requested == ["all"]:
        return KNOWN_AGENTS.copy()

    agents: list[str] = []
    for item in requested:
        agent = AGENT_ALIASES.get(item, item)
        if agent not in KNOWN_AGENTS and agent != "local":
            raise ValueError(f"unknown agent: {item}")
        if agent not in agents:
            agents.append(agent)
    return agents


def detect_agents(prefix: Path) -> list[str]:
    found: list[str] = []
    for agent in KNOWN_AGENTS:
        commands = COMMAND_DETECTION.get(agent, [])
        dirs = DIRECTORY_DETECTION.get(agent, [])
        command_found = any(shutil.which(command) for command in commands)
        directory_found = any((prefix / directory).exists() for directory in dirs)
        if command_found or directory_found:
            found.append(agent)
    return found or ["local"]


def copy_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def copy_all_skills(source: Path, destination_root: Path) -> None:
    destination_root.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted((source / "skills").glob("rust-*")):
        copy_tree(skill_dir, destination_root / skill_dir.name)


def copy_bundle(source: Path, bundle_dir: Path) -> None:
    if source == bundle_dir:
        raise ValueError("bundle directory must not be the source checkout")
    bundle_dir.mkdir(parents=True, exist_ok=True)
    for directory in ["skills", "rules", "mcp", "scripts", "templates", "docs", "evals"]:
        copy_tree(source / directory, bundle_dir / directory)
    for filename in ["README.md", "CONTRIBUTING.md", "LICENSE", "install.sh", ".mcp.json"]:
        src = source / filename
        if src.exists():
            shutil.copy2(src, bundle_dir / filename)
    codex_plugin = source / ".codex-plugin"
    if codex_plugin.exists():
        copy_tree(codex_plugin, bundle_dir / ".codex-plugin")
    claude_manifest = source / "claude-plugin" / PLUGIN_NAME / ".claude-plugin" / "plugin.json"
    if not claude_manifest.exists():
        claude_manifest = source / ".claude-plugin" / "plugin.json"
    if claude_manifest.exists():
        (bundle_dir / ".claude-plugin").mkdir(parents=True, exist_ok=True)
        shutil.copy2(claude_manifest, bundle_dir / ".claude-plugin" / "plugin.json")


def marketplace_json(marketplace_name: str, plugin_source: str | dict[str, str]) -> dict[str, object]:
    return {
        "name": marketplace_name,
        "owner": {"name": "madebyhost", "email": "contact@mehdiaissani.com"},
        "description": "madebyhost marketplace for Rust performance engineering plugins.",
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "displayName": "Rust Performance Skills",
                "source": plugin_source,
                "description": "Expert Rust performance engineering plugin with skills, rulebook, deterministic MCP tools, and Tauri desktop/mobile guidance.",
                "author": {"name": "madebyhost", "email": "contact@mehdiaissani.com"},
                "homepage": "https://github.com/madebyhost/rust-performance-skills",
                "repository": "https://github.com/madebyhost/rust-performance-skills",
                "license": "MIT",
                "keywords": ["rust", "performance", "low-latency", "pyo3", "wasm", "tauri", "ebpf", "sbe", "hft"],
                "category": "development",
                "defaultEnabled": True,
            }
        ],
    }


def write_claude_marketplace(source: Path, marketplace_root: Path, marketplace_name: str) -> Path:
    plugin_root = marketplace_root / "plugins" / PLUGIN_NAME
    if plugin_root.exists():
        shutil.rmtree(plugin_root)
    copy_bundle(source, plugin_root)
    write_file(
        marketplace_root / ".claude-plugin" / "marketplace.json",
        json.dumps(marketplace_json(marketplace_name, f"./plugins/{PLUGIN_NAME}"), indent=2) + "\n",
    )
    return plugin_root


def should_run_claude_cli(prefix: Path) -> bool:
    if os.environ.get("RUST_PERF_SKILLS_SKIP_CLAUDE_ADD") == "1":
        return False
    if not shutil.which("claude"):
        return False
    if os.environ.get("RUST_PERF_SKILLS_FORCE_CLAUDE_ADD") == "1":
        return True
    return prefix == Path.home()


def maybe_install_claude_plugin(prefix: Path, marketplace_root: Path, marketplace_name: str) -> list[Path]:
    if not should_run_claude_cli(prefix):
        print(f"skipped: claude plugin marketplace add {marketplace_root}")
        print(f"skipped: claude plugin install {PLUGIN_NAME}@{marketplace_name}")
        return []
    subprocess.run(["claude", "plugin", "marketplace", "add", str(marketplace_root)], check=True)
    subprocess.run(["claude", "plugin", "install", f"{PLUGIN_NAME}@{marketplace_name}", "--scope", "user"], check=True)
    return [marketplace_root]


def maybe_clean_claude_standalone_skills(prefix: Path) -> list[Path]:
    if os.environ.get("RUST_PERF_SKILLS_CLAUDE_CLEAN_STANDALONE") != "1":
        return []
    skills_root = prefix / ".claude" / "skills"
    removed: list[Path] = []
    if not skills_root.exists():
        return removed
    for path in sorted(skills_root.glob("rust-*")):
        if path.is_symlink():
            path.unlink()
            removed.append(path)
        elif path.is_dir():
            shutil.rmtree(path)
            removed.append(path)
    return removed


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def merge_block(path: Path, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    start = existing.find(MARKER_START)
    end = existing.find(MARKER_END)
    replacement = f"{MARKER_START}\n{block.strip()}\n{MARKER_END}\n"
    if start != -1 and end != -1 and end >= start:
        end += len(MARKER_END)
        updated = existing[:start] + replacement.rstrip() + existing[end:]
    else:
        prefix = existing.rstrip()
        updated = f"{prefix}\n\n{replacement}" if prefix else replacement
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def base_instruction(bundle_dir: Path) -> str:
    return f"""Use {PLUGIN_NAME} for Rust performance, quality, and systems work, including Tauri desktop/mobile apps.

Primary router:
{bundle_dir}/skills/{ROUTER_SKILL}/SKILL.md

Expert rule index:
{bundle_dir}/rules/index.json

Deterministic MCP server, when the agent supports MCP:
python3 {bundle_dir}/mcp/rust_performance_mcp.py

Behavior contract:
- inspect the real Rust project before recommending changes;
- identify latency, throughput, allocation, safety, and API constraints;
- load only the specialist skills needed for the task;
- cite rule IDs for non-trivial Rust review or design decisions;
- verify performance claims with benchmarks, profiles, tests, or explicit blockers.
"""


def cursor_rule(bundle_dir: Path) -> str:
    return f"""---
description: Rust performance engineering specialist for rust-performance-skills
globs: **/*.rs,**/Cargo.toml,**/pyproject.toml,**/tauri.conf.*,**/src-tauri/**,**/*.md
alwaysApply: false
---

{base_instruction(bundle_dir)}
"""


def agent_rule(bundle_dir: Path, agent_name: str) -> str:
    return f"""# rust-performance-skills for {agent_name}

{base_instruction(bundle_dir)}
"""


def install_codex(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    dest = prefix / ".codex" / "skills"
    copy_all_skills(source, dest)
    return [dest]


def install_claude(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    marketplace_name = os.environ.get("RUST_PERF_SKILLS_CLAUDE_MARKETPLACE", CLAUDE_MARKETPLACE_NAME)
    marketplace_root = prefix / ".claude" / "rust-performance-skills-marketplace"
    plugin_root = write_claude_marketplace(source, marketplace_root, marketplace_name)
    installed_paths = maybe_install_claude_plugin(prefix, marketplace_root, marketplace_name)
    removed_paths = maybe_clean_claude_standalone_skills(prefix)
    for path in removed_paths:
        print(f"removed standalone Claude skill: {path}")
    return [marketplace_root, plugin_root, *installed_paths]


def install_local(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    skills_dest = project_dir / ".agents" / "skills"
    copy_all_skills(source, skills_dest)
    rule_path = project_dir / ".agents" / "rules" / "rust-performance-skills.md"
    write_file(rule_path, agent_rule(bundle_dir, "generic local agents"))
    return [skills_dest, rule_path]


def install_gemini(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = prefix / ".gemini" / "GEMINI.md"
    merge_block(path, base_instruction(bundle_dir))
    return [path]


def install_cursor(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".cursor" / "rules" / "rust-performance-skills.mdc"
    write_file(path, cursor_rule(bundle_dir))
    return [path]


def install_windsurf(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".windsurfrules"
    merge_block(path, base_instruction(bundle_dir))
    return [path]


def install_cline(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".clinerules"
    merge_block(path, base_instruction(bundle_dir))
    return [path]


def install_roo(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".roo" / "rules" / "rust-performance-skills.md"
    write_file(path, agent_rule(bundle_dir, "Roo Code"))
    return [path]


def install_kilocode(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".kilocode" / "rules" / "rust-performance-skills.md"
    write_file(path, agent_rule(bundle_dir, "Kilo Code"))
    return [path]


def install_antigravity(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".agents" / "rules" / "antigravity-rust-performance-skills.md"
    write_file(path, agent_rule(bundle_dir, "Google Antigravity"))
    return [path]


def install_pi(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = prefix / ".pi" / "agent" / "extensions" / "rust-performance-skills.md"
    write_file(path, agent_rule(bundle_dir, "Pi"))
    return [path]


def install_hermes(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    dest = prefix / ".hermes" / "skills" / PLUGIN_NAME
    copy_tree(source / "skills" / ROUTER_SKILL, dest)
    write_file(dest / "README.md", agent_rule(bundle_dir, "Hermes"))
    return [dest]


def install_opencode(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = prefix / ".config" / "opencode" / "rust-performance-skills.md"
    write_file(path, agent_rule(bundle_dir, "OpenCode"))
    return [path]


def install_openclaw(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    dest = prefix / ".openclaw" / "skills" / PLUGIN_NAME
    copy_tree(source / "skills" / ROUTER_SKILL, dest)
    write_file(dest / "README.md", agent_rule(bundle_dir, "OpenClaw"))
    return [dest]


def install_ollama(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = prefix / ".ollama" / "openclaw" / "rust-performance-skills.md"
    write_file(
        path,
        agent_rule(bundle_dir, "Ollama launched OpenClaw")
        + "\nOllama is treated as a model/runtime provider; this file points OpenClaw-launched agents at the installed Rust skill bundle.\n",
    )
    return [path]


def install_copilot(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path) -> list[Path]:
    path = project_dir / ".github" / "copilot-instructions.md"
    merge_block(path, base_instruction(bundle_dir))
    return [path]


INSTALLERS = {
    "codex": install_codex,
    "claude": install_claude,
    "local": install_local,
    "gemini": install_gemini,
    "cursor": install_cursor,
    "windsurf": install_windsurf,
    "cline": install_cline,
    "roo": install_roo,
    "kilocode": install_kilocode,
    "antigravity": install_antigravity,
    "pi": install_pi,
    "hermes": install_hermes,
    "opencode": install_opencode,
    "openclaw": install_openclaw,
    "ollama": install_ollama,
    "copilot": install_copilot,
}


def install(source: Path, prefix: Path, project_dir: Path, bundle_dir: Path, agents: list[str]) -> dict[str, list[Path]]:
    copy_bundle(source, bundle_dir)
    results: dict[str, list[Path]] = {}
    for agent in agents:
        results[agent] = INSTALLERS[agent](source, prefix, project_dir, bundle_dir)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Install rust-performance-skills adapters for coding agents.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--prefix", type=Path, default=Path.home())
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--bundle-dir", type=Path)
    parser.add_argument("--claude-marketplace", default=os.environ.get("RUST_PERF_SKILLS_CLAUDE_MARKETPLACE", CLAUDE_MARKETPLACE_NAME))
    parser.add_argument("--agents", default="auto")
    args = parser.parse_args()

    source = args.source.resolve()
    prefix = args.prefix.expanduser().resolve()
    project_dir = args.project_dir.expanduser().resolve()
    bundle_dir = (args.bundle_dir or (prefix / ".agents" / PLUGIN_NAME)).expanduser().resolve()
    os.environ["RUST_PERF_SKILLS_CLAUDE_MARKETPLACE"] = args.claude_marketplace

    try:
        agents = parse_agents(args.agents, prefix)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        results = install(source, prefix, project_dir, bundle_dir, agents)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"installed agent adapters: {', '.join(results)}")
    for agent, paths in results.items():
        for path in paths:
            print(f"- {agent}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
