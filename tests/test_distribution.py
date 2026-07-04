import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

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


class DistributionTest(unittest.TestCase):
    def test_plugin_manifest_points_to_skills(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "rust-performance-skills")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn("skills", manifest["interface"]["capabilities"])

    def test_mcp_config_points_to_existing_local_server(self) -> None:
        config = json.loads((ROOT / ".mcp.json").read_text())
        server = config["mcpServers"]["rust-performance"]
        self.assertEqual(server["command"], "python3")
        for arg in server["args"]:
            if arg.endswith(".py"):
                self.assertTrue((ROOT / arg).exists(), f"missing MCP server {arg}")

    def test_required_skills_exist_with_metadata(self) -> None:
        for skill_name in REQUIRED_SKILLS:
            with self.subTest(skill=skill_name):
                skill_dir = SKILLS / skill_name
                skill_file = skill_dir / "SKILL.md"
                ui_file = skill_dir / "agents" / "openai.yaml"
                self.assertTrue(skill_file.exists(), f"missing {skill_file}")
                self.assertTrue(ui_file.exists(), f"missing {ui_file}")
                text = skill_file.read_text()
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---\n", 2)[1]
                self.assertIn(f"name: {skill_name}", frontmatter)
                self.assertIn("description:", frontmatter)
                self.assertNotRegex(text, r"\bTODO\b|\bTBD\b")
                ui_text = ui_file.read_text()
                self.assertIn("display_name:", ui_text)
                self.assertIn("short_description:", ui_text)
                self.assertIn(f"$${skill_name}".replace("$$", "$"), ui_text)

    def test_router_links_to_all_specialist_skills(self) -> None:
        router = (SKILLS / "rust-performance-engineering" / "SKILL.md").read_text()
        for skill_name in REQUIRED_SKILLS[1:]:
            self.assertIn(skill_name, router)

    def test_reference_links_exist(self) -> None:
        for skill_file in SKILLS.glob("*/SKILL.md"):
            text = skill_file.read_text()
            for rel in re.findall(r"`(references/[^`]+\.md)`", text):
                target = skill_file.parent / rel
                self.assertTrue(target.exists(), f"{skill_file} references missing {target}")

    def test_install_docs_cover_python_wasm_and_audit(self) -> None:
        combined = "\n".join(
            path.read_text() for path in (ROOT / "docs" / "install").glob("*.md")
        )
        for token in [
            "PyO3",
            "maturin",
            "Wasm",
            "rust_project_audit.py",
            "generate_quality_gates.py",
            "install.sh",
            "RUST_PERF_SKILLS_TARGET=plugin",
            "rust-performance-skills@personal",
        ]:
            self.assertIn(token, combined)

    def test_v4_plugin_and_mcp_files_exist(self) -> None:
        for rel in [
            "scripts/install_plugin_marketplace.py",
            "mcp/rust_performance_mcp.py",
            "tests/test_plugin_marketplace.py",
            "tests/test_mcp_contract.py",
        ]:
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")

    def test_v3_templates_and_evals_exist(self) -> None:
        for rel in [
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
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")

    def test_source_map_mentions_v3_tools(self) -> None:
        sources = (ROOT / "docs" / "sources.md").read_text()
        for token in ["cargo-nextest", "cargo-deny", "cargo-audit", "cargo-semver-checks", "Miri", "cargo-fuzz", "cargo-llvm-cov", "cargo-mutants"]:
            self.assertIn(token, sources)


if __name__ == "__main__":
    unittest.main()
