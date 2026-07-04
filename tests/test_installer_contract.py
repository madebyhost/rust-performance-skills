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
            "codex",
            ".codex",
            "claude",
            ".claude",
            "rust-performance-engineering",
        ]:
            self.assertIn(token, text)

    def test_readme_exposes_one_liner(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn("curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh", readme)


if __name__ == "__main__":
    unittest.main()
