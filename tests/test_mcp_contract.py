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
                [
                    sys.executable,
                    str(SERVER),
                    "--call",
                    "audit_rust_project",
                    "--arguments",
                    json.dumps({"path": str(root)}),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            audit = json.loads(completed.stdout)
            self.assertEqual(audit["project_type"], "rust")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SERVER),
                    "--call",
                    "generate_quality_gates",
                    "--arguments",
                    json.dumps({"audit": audit}),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            gates = json.loads(completed.stdout)
            self.assertIn("cargo fmt --check", "\n".join(gates["commands"]))


if __name__ == "__main__":
    unittest.main()
