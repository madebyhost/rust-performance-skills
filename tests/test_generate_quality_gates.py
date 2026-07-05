import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_quality_gates.py"


def run_generator(audit: dict) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "audit.json"
        path.write_text(json.dumps(audit))
        completed = subprocess.run(
            [sys.executable, str(GENERATOR), str(path), "--json"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return json.loads(completed.stdout)


class QualityGateGeneratorTest(unittest.TestCase):
    def test_generates_base_rust_gates(self) -> None:
        result = run_generator({"project_type": "rust", "findings": [], "strengths": [], "recommendations": []})
        commands = "\n".join(result["commands"])
        self.assertIn("cargo fmt --check", commands)
        self.assertIn("cargo clippy --all-targets --all-features", commands)
        self.assertIn("cargo nextest run", commands)
        self.assertIn("cargo deny check", commands)

    def test_generates_pyo3_wasm_unsafe_hft_gates(self) -> None:
        result = run_generator(
            {
                "project_type": "pyo3-extension",
                "findings": ["unsafe Rust present", "low-latency/HFT vocabulary present"],
                "strengths": ["Wasm dependency detected"],
                "recommendations": [],
            }
        )
        commands = "\n".join(result["commands"])
        self.assertIn("maturin build --release", commands)
        self.assertIn("wasm-pack test", commands)
        self.assertIn("cargo +nightly miri test", commands)
        self.assertIn("cargo bench", commands)

    def test_generates_tauri_gates(self) -> None:
        result = run_generator(
            {
                "project_type": "tauri-app",
                "findings": ["Tauri app structure detected"],
                "strengths": [],
                "recommendations": ["test Windows, Linux, macOS, iOS, and Android targets that are in scope"],
            }
        )
        commands = "\n".join(result["commands"])
        notes = "\n".join(result["notes"])
        self.assertIn("cargo tauri build", commands)
        self.assertIn("cargo tauri android build", commands)
        self.assertIn("cargo tauri ios build", commands)
        self.assertIn("Smoke-test Tauri bundles", notes)


if __name__ == "__main__":
    unittest.main()
