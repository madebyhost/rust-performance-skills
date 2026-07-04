import json
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
                            {
                                "name": "other",
                                "source": {"source": "local", "path": "./plugins/other"},
                                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                "category": "Productivity",
                            },
                            {
                                "name": "rust-performance-skills",
                                "source": {"source": "local", "path": "./old"},
                                "policy": {"installation": "NOT_AVAILABLE", "authentication": "ON_USE"},
                                "category": "Old",
                            },
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
