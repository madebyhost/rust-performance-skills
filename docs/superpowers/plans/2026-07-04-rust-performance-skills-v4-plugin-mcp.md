# Rust Performance Skills V4 Plugin MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `rust-performance-skills` installable as a visible local Codex plugin and add a safe offline MCP foundation.

**Architecture:** Keep the repo skill-first. Add a shell installer path for the Codex personal plugin marketplace, with Python helpers for deterministic marketplace JSON updates and MCP tool logic. The MCP server stays local stdio, dependency-free, and wraps existing audit/gate logic.

**Tech Stack:** POSIX shell, Python standard library, Codex plugin manifest, MCP stdio JSON-RPC, unittest.

---

## File Structure

- Modify `install.sh`: add `plugin` target, marketplace helper invocation, plugin directory copy, and optional `codex plugin add`.
- Create `scripts/install_plugin_marketplace.py`: deterministic marketplace create/update helper used by tests and installer.
- Create `tests/test_plugin_marketplace.py`: tests marketplace creation, update, plugin copy contract, and installer script tokens.
- Create `mcp/rust_performance_mcp.py`: dependency-free stdio MCP server exposing offline tools.
- Create `tests/test_mcp_contract.py`: tests `.mcp.json`, tool metadata, and direct tool logic.
- Modify `.mcp.json`: declare the local Python MCP server.
- Modify `scripts/validate_distribution.py`: validate plugin install and MCP contract.
- Modify `README.md` and `docs/install/codex.md`: document plugin install mode and Codex plugin list visibility.

### Task 1: Plugin Marketplace Contract Tests

**Files:**
- Create: `tests/test_plugin_marketplace.py`
- Modify: none

- [ ] **Step 1: Write failing tests**

```python
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "install_plugin_marketplace.py"
INSTALL = ROOT / "install.sh"


class PluginMarketplaceTest(unittest.TestCase):
    def test_creates_personal_marketplace_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            marketplace = home / ".agents" / "plugins" / "marketplace.json"
            plugin_dir = home / "plugins" / "rust-performance-skills"
            subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "--source",
                    str(ROOT),
                    "--plugin-dir",
                    str(plugin_dir),
                    "--marketplace",
                    str(marketplace),
                ],
                check=True,
            )
            data = json.loads(marketplace.read_text())
            self.assertEqual(data["name"], "personal")
            self.assertEqual(data["interface"]["displayName"], "Personal")
            self.assertEqual(len(data["plugins"]), 1)
            entry = data["plugins"][0]
            self.assertEqual(entry["name"], "rust-performance-skills")
            self.assertEqual(entry["source"], {"source": "local", "path": "./plugins/rust-performance-skills"})
            self.assertEqual(entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
            self.assertEqual(entry["category"], "Development")
            self.assertTrue((plugin_dir / ".codex-plugin" / "plugin.json").exists())
            self.assertTrue((plugin_dir / "skills" / "rust-performance-engineering" / "SKILL.md").exists())

    def test_updates_existing_entry_and_preserves_other_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marketplace = root / ".agents" / "plugins" / "marketplace.json"
            marketplace.parent.mkdir(parents=True)
            marketplace.write_text(
                json.dumps(
                    {
                        "name": "personal",
                        "interface": {"displayName": "Personal"},
                        "plugins": [
                            {"name": "other", "source": {"source": "local", "path": "./plugins/other"}, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"},
                            {"name": "rust-performance-skills", "source": {"source": "local", "path": "./old"}, "policy": {"installation": "NOT_AVAILABLE", "authentication": "ON_USE"}, "category": "Old"},
                        ],
                    }
                )
            )
            subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "--source",
                    str(ROOT),
                    "--plugin-dir",
                    str(root / "plugins" / "rust-performance-skills"),
                    "--marketplace",
                    str(marketplace),
                ],
                check=True,
            )
            data = json.loads(marketplace.read_text())
            self.assertEqual([entry["name"] for entry in data["plugins"]], ["other", "rust-performance-skills"])
            self.assertEqual(data["plugins"][1]["source"]["path"], "./plugins/rust-performance-skills")
            self.assertEqual(data["plugins"][1]["category"], "Development")

    def test_install_sh_documents_plugin_target(self) -> None:
        text = INSTALL.read_text()
        for token in [
            "RUST_PERF_SKILLS_TARGET",
            "plugin",
            "RUST_PERF_SKILLS_PLUGIN_DIR",
            "RUST_PERF_SKILLS_MARKETPLACE",
            "RUST_PERF_SKILLS_SKIP_CODEX_ADD",
            "codex plugin add rust-performance-skills@personal",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_plugin_marketplace -v`

Expected: FAIL because `scripts/install_plugin_marketplace.py` does not exist and `install.sh` lacks plugin target tokens.

- [ ] **Step 3: Implement marketplace helper and installer target**

Create `scripts/install_plugin_marketplace.py` with:

```python
#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path


PLUGIN_NAME = "rust-performance-skills"
ENTRY = {
    "name": PLUGIN_NAME,
    "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Development",
}


def copy_plugin(source: Path, plugin_dir: Path) -> None:
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    ignore = shutil.ignore_patterns(".git", ".worktrees", "__pycache__", "*.pyc")
    shutil.copytree(source, plugin_dir, ignore=ignore)


def load_marketplace(path: Path) -> dict:
    if not path.exists():
        return {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("marketplace.json must be an object")
    data.setdefault("name", "personal")
    data.setdefault("interface", {"displayName": "Personal"})
    data.setdefault("plugins", [])
    return data


def update_marketplace(path: Path) -> None:
    data = load_marketplace(path)
    plugins = data["plugins"]
    if not isinstance(plugins, list):
        raise ValueError("marketplace plugins must be an array")
    for index, entry in enumerate(plugins):
        if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME:
            plugins[index] = ENTRY
            break
    else:
        plugins.append(ENTRY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install rust-performance-skills into the Codex personal plugin marketplace.")
    parser.add_argument("--source", default=".", help="repository source path")
    parser.add_argument("--plugin-dir", required=True, help="destination plugin directory")
    parser.add_argument("--marketplace", required=True, help="marketplace.json path")
    args = parser.parse_args()
    copy_plugin(Path(args.source).resolve(), Path(args.plugin_dir).expanduser().resolve())
    update_marketplace(Path(args.marketplace).expanduser().resolve())
    print(f"installed {PLUGIN_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Modify `install.sh` so `plugin` and `all` call the helper using the extracted source directory:

```sh
PLUGIN_DIR="${RUST_PERF_SKILLS_PLUGIN_DIR:-$HOME/plugins/rust-performance-skills}"
MARKETPLACE="${RUST_PERF_SKILLS_MARKETPLACE:-$HOME/.agents/plugins/marketplace.json}"

install_plugin() {
  python3 "$src_dir/scripts/install_plugin_marketplace.py" \
    --source "$src_dir" \
    --plugin-dir "$PLUGIN_DIR" \
    --marketplace "$MARKETPLACE"
  if [ "${RUST_PERF_SKILLS_SKIP_CODEX_ADD:-0}" != "1" ] && command -v codex >/dev/null 2>&1; then
    codex plugin add rust-performance-skills@personal
  else
    echo "skipped: codex plugin add rust-performance-skills@personal"
  fi
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_plugin_marketplace -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add install.sh scripts/install_plugin_marketplace.py tests/test_plugin_marketplace.py
git commit -m "feat: add codex plugin marketplace installer"
```

### Task 2: MCP Contract Tests

**Files:**
- Create: `tests/test_mcp_contract.py`
- Create: `mcp/rust_performance_mcp.py`
- Modify: `.mcp.json`

- [ ] **Step 1: Write failing tests**

```python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "rust_performance_mcp.py"


class McpContractTest(unittest.TestCase):
    def test_mcp_config_declares_existing_local_server(self) -> None:
        data = json.loads((ROOT / ".mcp.json").read_text())
        server = data["mcpServers"]["rust-performance"]
        self.assertEqual(server["command"], "python3")
        self.assertIn("mcp/rust_performance_mcp.py", server["args"][0])
        self.assertTrue((ROOT / server["args"][0]).exists())

    def test_direct_list_tools(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SERVER), "--list-tools"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        tools = json.loads(completed.stdout)
        names = {tool["name"] for tool in tools["tools"]}
        self.assertIn("audit_rust_project", names)
        self.assertIn("generate_quality_gates", names)
        self.assertIn("list_rust_skills", names)
        self.assertIn("rust_review_checklist", names)

    def test_direct_call_audit_and_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "Cargo.toml").write_text("[package]\nname='demo'\nversion='0.1.0'\nedition='2024'\n")
            (root / "src" / "lib.rs").write_text("pub fn parse(_: &[u8]) {}\n")
            completed = subprocess.run(
                [sys.executable, str(SERVER), "--call", "audit_rust_project", "--arguments", json.dumps({"path": str(root)})],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            audit = json.loads(completed.stdout)
            self.assertEqual(audit["project_type"], "rust")
            completed = subprocess.run(
                [sys.executable, str(SERVER), "--call", "generate_quality_gates", "--arguments", json.dumps({"audit": audit})],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            gates = json.loads(completed.stdout)
            self.assertIn("cargo fmt --check", "\n".join(gates["commands"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_mcp_contract -v`

Expected: FAIL because `.mcp.json` does not declare the server and `mcp/rust_performance_mcp.py` does not exist.

- [ ] **Step 3: Implement MCP server and config**

Create `mcp/rust_performance_mcp.py` as a dependency-free server that supports both direct test CLI and stdio JSON-RPC:

```python
#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_quality_gates import generate  # noqa: E402
from rust_project_audit import audit  # noqa: E402


TOOLS = [
    {"name": "audit_rust_project", "description": "Audit Rust project structure and performance signals.", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "generate_quality_gates", "description": "Generate quality gate commands from audit JSON.", "inputSchema": {"type": "object", "properties": {"audit": {"type": "object"}}, "required": ["audit"]}},
    {"name": "list_rust_skills", "description": "List packaged Rust specialist skills.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "rust_review_checklist", "description": "Return a Rust review checklist selected by signals.", "inputSchema": {"type": "object", "properties": {"project_type": {"type": "string"}, "findings": {"type": "array", "items": {"type": "string"}}}}},
]


def list_skills() -> dict:
    skills = []
    for skill in sorted((ROOT / "skills").glob("rust-*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        first_heading = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")), skill.parent.name)
        skills.append({"name": skill.parent.name, "title": first_heading})
    return {"skills": skills}


def review_checklist(arguments: dict) -> dict:
    findings = "\n".join(arguments.get("findings", []))
    checks = ["correctness and API compatibility", "tests and CI quality gates", "allocation/copy hot paths", "error handling and observability"]
    if "unsafe" in findings:
        checks.extend(["SAFETY comments", "Miri or sanitizer suitability", "safe wrapper invariants"])
    if arguments.get("project_type") == "pyo3-extension":
        checks.extend(["Python/Rust boundary cost", "maturin wheel build and import test"])
    if arguments.get("project_type") == "wasm":
        checks.extend(["JS/Wasm boundary cost", "wasm-pack build and test"])
    if "low-latency/HFT vocabulary present" in findings:
        checks.extend(["p99/p999 latency", "drops and queue depth", "CPU/cache/network assumptions"])
    return {"checks": checks}


def call_tool(name: str, arguments: dict) -> dict:
    if name == "audit_rust_project":
        return audit(Path(arguments["path"]))
    if name == "generate_quality_gates":
        return generate(arguments["audit"])
    if name == "list_rust_skills":
        return list_skills()
    if name == "rust_review_checklist":
        return review_checklist(arguments)
    raise ValueError(f"unknown tool: {name}")
```

Add request handling for `initialize`, `tools/list`, and `tools/call`, returning MCP-compatible JSON-RPC responses.

Update `.mcp.json`:

```json
{
  "mcpServers": {
    "rust-performance": {
      "command": "python3",
      "args": [
        "mcp/rust_performance_mcp.py"
      ]
    }
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_mcp_contract -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add .mcp.json mcp/rust_performance_mcp.py tests/test_mcp_contract.py
git commit -m "feat: add offline rust performance mcp server"
```

### Task 3: Distribution Docs And Validator

**Files:**
- Modify: `README.md`
- Modify: `docs/install/codex.md`
- Modify: `docs/install/generic-agents.md`
- Modify: `scripts/validate_distribution.py`
- Modify: `tests/test_distribution.py`
- Modify: `tests/test_installer_contract.py`

- [ ] **Step 1: Write failing tests**

Add assertions requiring:

- README contains `RUST_PERF_SKILLS_TARGET=plugin`.
- README contains `codex plugin list`.
- Codex install doc contains `rust-performance-skills@personal`.
- distribution validator checks `scripts/install_plugin_marketplace.py`, `mcp/rust_performance_mcp.py`, and `.mcp.json` server file existence.

- [ ] **Step 2: Run tests to verify failure**

Run: `python3 -m unittest tests.test_distribution tests.test_installer_contract -v`

Expected: FAIL on missing docs or validator contract.

- [ ] **Step 3: Update docs and validator**

Document:

```bash
RUST_PERF_SKILLS_TARGET=plugin sh -c "$(curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh)"
codex plugin list
codex plugin add rust-performance-skills@personal
```

Update `scripts/validate_distribution.py` to ensure `.mcp.json` names an existing local server file and that plugin installer helper exists.

- [ ] **Step 4: Run tests to verify pass**

Run: `python3 -m unittest tests.test_distribution tests.test_installer_contract -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add README.md docs/install/codex.md docs/install/generic-agents.md scripts/validate_distribution.py tests/test_distribution.py tests/test_installer_contract.py
git commit -m "docs: document plugin marketplace install"
```

### Task 4: Full Verification, Local Plugin Install, Push

**Files:**
- Modify: none unless verification exposes issues.

- [ ] **Step 1: Run full test suite**

Run: `python3 -m unittest discover -s tests`

Expected: all tests pass.

- [ ] **Step 2: Run distribution and plugin validators**

Run:

```bash
python3 scripts/validate_distribution.py
/tmp/rust-performance-skills-venv/bin/python /Users/admin/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/admin/Documents/Codex/2026-07-04/a/work/rust-performance-skills
zsh -lc 'for d in skills/*; do /tmp/rust-performance-skills-venv/bin/python /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d" || exit 1; done'
sh -n install.sh
```

Expected: all pass.

- [ ] **Step 3: Install locally for Codex plugin visibility**

Run from the repo:

```bash
RUST_PERF_SKILLS_REF=main RUST_PERF_SKILLS_TARGET=plugin RUST_PERF_SKILLS_SKIP_DOWNLOAD=1 sh install.sh
codex plugin list
```

Expected: `rust-performance-skills@personal` appears installed or available in `codex plugin list`.

- [ ] **Step 4: Merge and push**

Run:

```bash
git checkout main
git pull --ff-only origin main
git merge --ff-only codex/rust-performance-v4-plugin-mcp
git push origin main
```

Expected: push succeeds.

- [ ] **Step 5: Watch GitHub Actions**

Run:

```bash
gh run list --repo madebyhost/rust-performance-skills --limit 5
gh run watch <run-id> --repo madebyhost/rust-performance-skills --exit-status
```

Expected: CI success.
