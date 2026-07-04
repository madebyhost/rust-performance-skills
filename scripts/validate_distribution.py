#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
MCP = ROOT / ".mcp.json"

REQUIRED_SKILLS = [
    "rust-performance-engineering",
    "rust-code-quality",
    "rust-performance-core",
    "rust-async-concurrency",
    "rust-low-latency-hft",
    "rust-python-pyo3-maturin",
    "rust-wasm-engineering",
    "rust-ffi-bindings",
    "rust-unsafe-soundness",
    "rust-architecture-patterns",
    "rust-review-auditor",
    "rust-ci-quality-gates",
    "rust-testing-verification",
    "rust-crate-release-engineering",
]


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


def validate_skill(skill_name: str) -> None:
    skill_dir = SKILLS / skill_name
    skill_file = skill_dir / "SKILL.md"
    text = read(skill_file)
    read(skill_dir / "agents" / "openai.yaml")
    if not text.startswith("---\n"):
        fail(f"{skill_name} SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail(f"{skill_name} SKILL.md frontmatter must close")
    frontmatter = parts[1]
    if f"name: {skill_name}" not in frontmatter:
        fail(f"{skill_name} name mismatch")
    if "description:" not in frontmatter:
        fail(f"{skill_name} missing description")
    if re.search(r"\bTODO\b|\bTBD\b", text):
        fail(f"{skill_name} contains placeholder text")

    for ref in re.findall(r"`(references/[^`]+\.md)`", text):
        target = skill_dir / ref
        if not target.exists():
            fail(f"missing referenced file {target.relative_to(ROOT)}")


def validate_skills() -> None:
    for skill_name in REQUIRED_SKILLS:
        validate_skill(skill_name)

    router = read(SKILLS / "rust-performance-engineering" / "SKILL.md")
    for skill_name in REQUIRED_SKILLS[1:]:
        if skill_name not in router:
            fail(f"router does not mention {skill_name}")


def validate_docs() -> None:
    for rel in [
        "README.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "docs/install/codex.md",
        "docs/install/claude.md",
        "docs/install/generic-agents.md",
        "skills/rust-performance-engineering/agents/openai.yaml",
        "scripts/rust_project_audit.py",
        "scripts/generate_quality_gates.py",
        "install.sh",
        "templates/ci/rust-library.yml",
        "templates/ci/pyo3-maturin.yml",
        "templates/ci/wasm.yml",
        "templates/ci/hft-perf.yml",
        "evals/rust-quality-review.md",
        "evals/pyo3-optimization.md",
        "evals/wasm-boundary.md",
        "evals/hft-hot-path.md",
        "evals/unsafe-soundness.md",
    ]:
        read(ROOT / rel)

    install_docs = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "docs" / "install").glob("*.md")
    )
    for token in ["PyO3", "maturin", "Wasm", "rust_project_audit.py", "generate_quality_gates.py", "install.sh"]:
        if token not in install_docs:
            fail(f"install docs do not mention {token}")

    readme = read(ROOT / "README.md")
    one_liner = "curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh"
    if one_liner not in readme:
        fail("README does not expose the install one-liner")

    sources = read(ROOT / "docs" / "sources.md")
    for token in ["cargo-nextest", "cargo-deny", "cargo-audit", "cargo-semver-checks", "Miri", "cargo-fuzz", "cargo-llvm-cov", "cargo-mutants"]:
        if token not in sources:
            fail(f"sources do not mention {token}")


def main() -> None:
    validate_plugin()
    validate_skills()
    validate_docs()
    print("distribution validation passed")


if __name__ == "__main__":
    main()
