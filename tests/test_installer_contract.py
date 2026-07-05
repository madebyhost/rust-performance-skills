import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerContractTest(unittest.TestCase):
    def test_install_sh_exists_and_documents_targets(self) -> None:
        install = ROOT / "install.sh"
        self.assertTrue(install.exists(), "install.sh missing")
        text = install.read_text()
        for token in [
            "RUST_PERF_SKILLS_TARGET",
            "RUST_PERF_SKILLS_REF",
            "RUST_PERF_SKILLS_PLUGIN_DIR",
            "RUST_PERF_SKILLS_MARKETPLACE",
            "RUST_PERF_SKILLS_SKIP_CODEX_ADD",
            "RUST_PERF_SKILLS_AGENTS",
            "RUST_PERF_SKILLS_PROJECT_DIR",
            "RUST_PERF_SKILLS_AGENT_BUNDLE_DIR",
            "auto",
            "agents",
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
            "codex",
            ".codex",
            "claude",
            ".claude",
            "plugin",
            "codex plugin add rust-performance-skills@personal",
            "rust-performance-engineering",
        ]:
            self.assertIn(token, text)

    def test_readme_exposes_one_liner(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn("curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh", readme)
        self.assertIn("RUST_PERF_SKILLS_AGENTS", readme)
        self.assertIn("Gemini CLI", readme)
        self.assertIn("OpenClaw", readme)
        self.assertIn("RUST_PERF_SKILLS_TARGET=plugin", readme)
        self.assertIn("codex plugin list", readme)
        self.assertIn("rust-performance-skills@personal", readme)


if __name__ == "__main__":
    unittest.main()
