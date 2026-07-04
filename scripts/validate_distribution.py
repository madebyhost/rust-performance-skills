#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rust-performance-engineering" / "SKILL.md"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
MCP = ROOT / ".mcp.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate_plugin() -> None:
    data = json.loads(read(PLUGIN))
    required = ["name", "version", "description", "skills", "interface"]
    for key in required:
        if key not in data:
            fail(f"plugin missing {key}")
    if data["name"] != "rust-performance-skills":
        fail("plugin name must be rust-performance-skills")
    if data["skills"] != "./skills/":
        fail("plugin skills path must be ./skills/")
    interface = data["interface"]
    for key in ["displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"]:
        if not interface.get(key):
            fail(f"plugin interface missing {key}")
    json.loads(read(MCP))


def validate_skill() -> None:
    text = read(SKILL)
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter must close")
    frontmatter = parts[1]
    if "name: rust-performance-engineering" not in frontmatter:
        fail("SKILL.md name mismatch")
    if "description:" not in frontmatter:
        fail("SKILL.md missing description")
    if "TODO" in text or "TBD" in text:
        fail("SKILL.md contains placeholder text")

    refs = re.findall(r"`(references/[^`]+\.md)`", text)
    if not refs:
        fail("SKILL.md must route to reference files")
    for ref in refs:
        target = SKILL.parent / ref
        if not target.exists():
            fail(f"missing referenced file {target.relative_to(ROOT)}")


def validate_docs() -> None:
    for rel in [
        "README.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "docs/install/codex.md",
        "docs/install/claude.md",
        "docs/install/generic-agents.md",
        "skills/rust-performance-engineering/agents/openai.yaml",
    ]:
        read(ROOT / rel)


def main() -> None:
    validate_plugin()
    validate_skill()
    validate_docs()
    print("distribution validation passed")


if __name__ == "__main__":
    main()
