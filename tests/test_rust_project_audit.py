import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "rust_project_audit.py"


def run_audit(project: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(AUDIT), str(project), "--json"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(completed.stdout)


class RustProjectAuditTest(unittest.TestCase):
    def test_reports_missing_cargo_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_audit(Path(tmp))
        self.assertEqual(result["project_type"], "unknown")
        self.assertIn("missing Cargo.toml", result["findings"])

    def test_detects_release_profile_and_lints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text(
                """
[package]
name = "demo"
version = "0.1.0"
edition = "2024"

[lints.rust]
unsafe_code = "warn"

[profile.release]
lto = "thin"
codegen-units = 1
strip = "symbols"
""".strip()
            )
            result = run_audit(root)
        self.assertIn("release profile configured", result["strengths"])
        self.assertIn("unsafe_code lint configured", result["strengths"])

    def test_detects_pyo3_maturin_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text(
                """
[package]
name = "pyfast"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.29", features = ["extension-module"] }
rayon = "1"
""".strip()
            )
            (root / "pyproject.toml").write_text(
                """
[build-system]
requires = ["maturin>=1.14"]
build-backend = "maturin"
""".strip()
            )
            result = run_audit(root)
        self.assertEqual(result["project_type"], "pyo3-extension")
        self.assertIn("maturin packaging detected", result["strengths"])
        self.assertIn("consider Python::detach for CPU-heavy Rust work", result["recommendations"])

    def test_detects_wasm_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text(
                """
[package]
name = "webfast"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
web-sys = "0.3"
""".strip()
            )
            result = run_audit(root)
        self.assertEqual(result["project_type"], "wasm")
        self.assertIn("measure generated wasm and JS boundary cost", result["recommendations"])

    def test_detects_unsafe_and_hft_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "Cargo.toml").write_text(
                """
[package]
name = "feed"
version = "0.1.0"
edition = "2024"
""".strip()
            )
            (root / "src" / "lib.rs").write_text(
                """
pub unsafe fn read(ptr: *const u8) -> u8 { *ptr }
pub fn udp_multicast_ring_buffer() {}
""".strip()
            )
            result = run_audit(root)
        self.assertIn("unsafe Rust present", result["findings"])
        self.assertIn("low-latency/HFT vocabulary present", result["findings"])
        self.assertIn("require SAFETY comments and soundness review", result["recommendations"])


if __name__ == "__main__":
    unittest.main()
