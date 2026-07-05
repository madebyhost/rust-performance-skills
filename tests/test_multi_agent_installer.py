import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "install_agent_adapters.py"


class MultiAgentInstallerTest(unittest.TestCase):
    def run_helper(self, home: Path, project: Path, agents: str, env: dict[str, str] | None = None) -> str:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        result = subprocess.run(
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
                agents,
            ],
            check=True,
            text=True,
            capture_output=True,
            env=merged_env,
        )
        return result.stdout

    def test_explicit_multi_agent_install_writes_static_adapters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            project = root / "project"
            home.mkdir()
            project.mkdir()
            (project / ".windsurfrules").write_text("keep me\n", encoding="utf-8")

            output = self.run_helper(
                home,
                project,
                "codex,claude,gemini,cursor,windsurf,cline,roo,kilocode,antigravity,pi,hermes,opencode,openclaw,ollama,copilot",
            )

            self.assertIn("installed agent adapters", output)
            self.assertTrue((home / ".agents" / "rust-performance-skills" / "skills" / "rust-performance-engineering" / "SKILL.md").exists())
            self.assertTrue((home / ".codex" / "skills" / "rust-performance-engineering" / "SKILL.md").exists())
            self.assertTrue((home / ".claude" / "rust-performance-skills-marketplace" / ".claude-plugin" / "marketplace.json").exists())
            self.assertFalse((home / ".claude" / "skills" / "rust-performance-engineering").exists())
            self.assertIn("rust-performance-skills", (home / ".gemini" / "GEMINI.md").read_text(encoding="utf-8"))
            self.assertIn("alwaysApply", (project / ".cursor" / "rules" / "rust-performance-skills.mdc").read_text(encoding="utf-8"))
            self.assertIn("keep me", (project / ".windsurfrules").read_text(encoding="utf-8"))
            self.assertIn("rust-performance-skills", (project / ".clinerules").read_text(encoding="utf-8"))
            self.assertTrue((project / ".roo" / "rules" / "rust-performance-skills.md").exists())
            self.assertTrue((project / ".kilocode" / "rules" / "rust-performance-skills.md").exists())
            self.assertTrue((project / ".agents" / "rules" / "antigravity-rust-performance-skills.md").exists())
            self.assertTrue((home / ".pi" / "agent" / "extensions" / "rust-performance-skills.md").exists())
            self.assertTrue((home / ".hermes" / "skills" / "rust-performance-skills" / "SKILL.md").exists())
            self.assertTrue((home / ".config" / "opencode" / "rust-performance-skills.md").exists())
            self.assertTrue((home / ".openclaw" / "skills" / "rust-performance-skills" / "SKILL.md").exists())
            self.assertTrue((home / ".ollama" / "openclaw" / "rust-performance-skills.md").exists())
            self.assertIn("rust-performance-skills", (project / ".github" / "copilot-instructions.md").read_text(encoding="utf-8"))

    def test_auto_mode_detects_known_agent_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            project = root / "project"
            bin_dir = root / "bin"
            home.mkdir()
            project.mkdir()
            bin_dir.mkdir()
            for name in ["gemini", "cursor", "hermes", "openclaw", "ollama"]:
                tool = bin_dir / name
                tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                tool.chmod(0o755)

            output = self.run_helper(
                home,
                project,
                "auto",
                env={"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"},
            )

            self.assertIn("gemini", output)
            self.assertIn("cursor", output)
            self.assertIn("hermes", output)
            self.assertIn("openclaw", output)
            self.assertIn("ollama", output)
            self.assertTrue((home / ".gemini" / "GEMINI.md").exists())
            self.assertTrue((project / ".cursor" / "rules" / "rust-performance-skills.mdc").exists())
            self.assertTrue((home / ".hermes" / "skills" / "rust-performance-skills" / "SKILL.md").exists())
            self.assertTrue((home / ".openclaw" / "skills" / "rust-performance-skills" / "SKILL.md").exists())
            self.assertTrue((home / ".ollama" / "openclaw" / "rust-performance-skills.md").exists())


if __name__ == "__main__":
    unittest.main()
