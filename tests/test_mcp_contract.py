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
        self.assertIn("detect_performance_domains", names)
        self.assertIn("rust_algorithm_checklist", names)
        self.assertIn("binary_encoding_review_checklist", names)
        self.assertIn("memory_simd_io_checklist", names)
        self.assertIn("api_type_design_checklist", names)
        self.assertIn("select_rust_rules", names)
        self.assertIn("explain_rust_rule", names)

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

    def test_direct_call_v5_domain_tools(self) -> None:
        audit = {
            "project_type": "rust",
            "strengths": [],
            "findings": [
                "eBPF/kernel performance signals present",
                "SBE/binary codec signals present",
                "math/algorithm performance signals present",
                "memory/SIMD/I/O performance signals present",
                "API/type-system design signals present",
                "unsafe Rust present",
            ],
            "recommendations": [],
        }
        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "detect_performance_domains",
                "--arguments",
                json.dumps({"audit": audit}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        domains = json.loads(completed.stdout)
        self.assertEqual(
            ["ebpf", "sbe", "math", "memory", "simd", "io", "api", "type", "serde", "macro", "unsafe"],
            domains["domains"],
        )

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "rust_algorithm_checklist",
                "--arguments",
                json.dumps({"algorithm": "dijkstra", "signals": ["petgraph", "rayon", "poisson"]}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        algorithm = json.loads(completed.stdout)
        self.assertIn("use compact node IDs and cache-friendly adjacency storage", algorithm["checks"])
        self.assertIn("preallocate frontier, distance, and predecessor buffers", algorithm["checks"])
        self.assertIn("control RNG seeds and statistical tolerances", algorithm["checks"])

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "binary_encoding_review_checklist",
                "--arguments",
                json.dumps({"codec": "sbe", "signals": ["templateId", "actingVersion"]}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        codec = json.loads(completed.stdout)
        self.assertIn("golden frame fixtures for every schema version", codec["checks"])
        self.assertIn("validate block length, template ID, schema ID, and acting version", codec["checks"])
        self.assertIn("zero-copy decode lifetimes cannot outlive the frame", codec["checks"])

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "memory_simd_io_checklist",
                "--arguments",
                json.dumps({"signals": ["memmap2", "io-uring", "mimalloc", "std::simd", "NUMA"]}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        memory = json.loads(completed.stdout)
        self.assertIn("benchmark allocator choice with production allocation lifetimes", memory["checks"])
        self.assertIn("validate SIMD dispatch, scalar fallback, and target-feature gates", memory["checks"])
        self.assertIn("measure page faults, mmap readahead, and io_uring queue depth", memory["checks"])
        self.assertIn("pin CPU and memory locality only after NUMA evidence", memory["checks"])

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "api_type_design_checklist",
                "--arguments",
                json.dumps({"signals": ["typestate", "serde", "sealed trait", "macro_rules"]}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        api = json.loads(completed.stdout)
        self.assertIn("encode invariants with validated newtypes or typestate only when states are real", api["checks"])
        self.assertIn("document sealed-trait intent and external implementation policy", api["checks"])
        self.assertIn("check serde defaults, unknown fields, flattening, and compatibility tests", api["checks"])
        self.assertIn("verify macro hygiene with $crate paths and hidden helpers", api["checks"])

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "rust_review_checklist",
                "--arguments",
                json.dumps({"project_type": "rust", "findings": audit["findings"]}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        review = json.loads(completed.stdout)
        self.assertIn("eBPF verifier, map, and privilege assumptions", review["checks"])
        self.assertIn("SBE schema compatibility and golden frames", review["checks"])
        self.assertIn("algorithmic complexity and cache-aware data layout", review["checks"])
        self.assertIn("allocator, SIMD, mmap, and io_uring evidence", review["checks"])
        self.assertIn("type-driven API invariants and serde compatibility", review["checks"])

    def test_direct_call_rulebook_tools(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "select_rust_rules",
                "--arguments",
                json.dumps({"signals": ["zero-copy", "udp multicast", "sbe", "pyo3"], "limit": 8}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        selected = json.loads(completed.stdout)
        rule_ids = {rule["id"] for rule in selected["rules"]}
        self.assertIn("mem-zero-copy", rule_ids)
        self.assertIn("hft-udp-multicast-hotpath", rule_ids)
        self.assertIn("sbe-zero-copy-lifetime", rule_ids)
        self.assertIn("pyo3-release-gil-hotloop", rule_ids)

        completed = subprocess.run(
            [
                sys.executable,
                str(SERVER),
                "--call",
                "explain_rust_rule",
                "--arguments",
                json.dumps({"rule_id": "hft-udp-multicast-hotpath"}),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        rule = json.loads(completed.stdout)
        self.assertEqual("hft-udp-multicast-hotpath", rule["id"])
        self.assertIn("bad", rule)
        self.assertIn("good", rule)
        self.assertIn("verification", rule)


if __name__ == "__main__":
    unittest.main()
