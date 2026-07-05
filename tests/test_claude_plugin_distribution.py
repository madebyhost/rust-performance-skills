import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "install_agent_adapters.py"


class ClaudePluginDistributionTest(unittest.TestCase):
    def test_claude_plugin_manifest_packages_skills_and_mcp(self) -> None:
        manifest_path = ROOT / "claude-plugin" / "rust-performance-skills" / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "rust-performance-skills")
        self.assertEqual(manifest["displayName"], "Rust Performance Skills")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn("rust-performance", manifest["mcpServers"])
        server = manifest["mcpServers"]["rust-performance"]
        self.assertEqual(server["command"], "python3")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/mcp/rust_performance_mcp.py", server["args"])

    def test_claude_marketplace_points_to_public_plugin(self) -> None:
        marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
        self.assertTrue(marketplace_path.exists())
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "madebyhost-rust-performance")
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "rust-performance-skills")
        self.assertEqual(plugin["source"], "./claude-plugin/rust-performance-skills")
        self.assertEqual(plugin["category"], "development")

    def test_claude_agent_install_creates_plugin_marketplace_not_standalone_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            project = root / "project"
            bin_dir = root / "bin"
            log = root / "claude.log"
            home.mkdir()
            project.mkdir()
            bin_dir.mkdir()
            fake_claude = bin_dir / "claude"
            fake_claude.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {log}\n", encoding="utf-8")
            fake_claude.chmod(0o755)

            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
            env["RUST_PERF_SKILLS_FORCE_CLAUDE_ADD"] = "1"
            subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "--source",
                    str(ROOT),
                    "--prefix",
                    str(home),
                    "--project-dir",
                    str(project),
                    "--agents",
                    "claude",
                ],
                check=True,
                env=env,
            )

            marketplace_root = home / ".claude" / "rust-performance-skills-marketplace"
            plugin_root = marketplace_root / "plugins" / "rust-performance-skills"
            self.assertTrue((marketplace_root / ".claude-plugin" / "marketplace.json").exists())
            self.assertTrue((plugin_root / ".claude-plugin" / "plugin.json").exists())
            self.assertFalse((plugin_root / ".claude-plugin" / "marketplace.json").exists())
            self.assertTrue((plugin_root / "skills" / "rust-performance-engineering" / "SKILL.md").exists())
            self.assertFalse((home / ".claude" / "skills" / "rust-performance-engineering").exists())

            calls = log.read_text(encoding="utf-8")
            self.assertIn(f"plugin marketplace add {marketplace_root.resolve()}", calls)
            self.assertIn("plugin install rust-performance-skills@madebyhost-rust-performance --scope user", calls)

    def test_claude_cleanup_old_standalone_skills_is_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            project = root / "project"
            old_skill = home / ".claude" / "skills" / "rust-performance-engineering"
            keep_skill = home / ".claude" / "skills" / "custom-skill"
            old_skill.mkdir(parents=True)
            keep_skill.mkdir(parents=True)
            project.mkdir()

            env = os.environ.copy()
            env["RUST_PERF_SKILLS_CLAUDE_CLEAN_STANDALONE"] = "1"
            env["RUST_PERF_SKILLS_SKIP_CLAUDE_ADD"] = "1"
            subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "--source",
                    str(ROOT),
                    "--prefix",
                    str(home),
                    "--project-dir",
                    str(project),
                    "--agents",
                    "claude",
                ],
                check=True,
                env=env,
            )

            self.assertFalse(old_skill.exists())
            self.assertTrue(keep_skill.exists())


if __name__ == "__main__":
    unittest.main()
