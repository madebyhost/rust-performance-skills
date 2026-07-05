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

    def test_detects_ebpf_kernel_performance_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "Cargo.toml").write_text(
                """
[package]
name = "xdp-fast"
version = "0.1.0"
edition = "2024"

[dependencies]
aya = "0.13"
libbpf-rs = "0.24"
""".strip()
            )
            (root / "src" / "lib.rs").write_text(
                """
pub fn xdp_market_data_filter() {
    let _program = "BPF_PROG_TYPE_XDP";
    let _map = "BPF_MAP_TYPE_XSKMAP";
    let _trace = "kprobe ringbuf bounded loop verifier";
}
""".strip()
            )
            result = run_audit(root)
        self.assertIn("eBPF/kernel performance signals present", result["findings"])
        self.assertIn("eBPF Rust tooling detected", result["strengths"])
        self.assertIn("verify bounded loops, map capacity, and required kernel capabilities", result["recommendations"])
        self.assertIn("test eBPF loaders without requiring root in default CI", result["recommendations"])

    def test_detects_sbe_binary_codec_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "schemas").mkdir()
            (root / "Cargo.toml").write_text(
                """
[package]
name = "codec"
version = "0.1.0"
edition = "2024"

[dependencies]
sbe-codegen = "0.1"
""".strip()
            )
            (root / "src" / "lib.rs").write_text(
                """
pub fn decode_header(buf: &[u8]) {
    let _ = (buf, "messageHeader templateId schemaId blockLength actingVersion");
}
""".strip()
            )
            (root / "schemas" / "market-data.xml").write_text(
                """
<messageSchema package="md" id="1" version="3">
  <message name="Quote" id="10" blockLength="24"/>
</messageSchema>
""".strip()
            )
            result = run_audit(root)
        self.assertIn("SBE/binary codec signals present", result["findings"])
        self.assertIn("add golden frame fixtures and schema compatibility tests", result["recommendations"])
        self.assertIn("verify zero-copy decode lifetimes and endian/block-length handling", result["recommendations"])

    def test_detects_math_algorithm_performance_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "Cargo.toml").write_text(
                """
[package]
name = "solver"
version = "0.1.0"
edition = "2024"

[dependencies]
petgraph = "0.7"
ndarray = "0.16"
rayon = "1"
rand_distr = "0.5"
statrs = "0.18"
""".strip()
            )
            (root / "src" / "lib.rs").write_text(
                """
pub fn run() {
    let _ = "BFS DFS Dijkstra A* MonteCarlo Markov Poisson sparse matrix";
}
""".strip()
            )
            result = run_audit(root)
        self.assertIn("math/algorithm performance signals present", result["findings"])
        self.assertIn("math and graph tooling detected", result["strengths"])
        self.assertIn("benchmark algorithmic complexity against representative graph sizes", result["recommendations"])
        self.assertIn("control RNG seeds and statistical tolerances for simulations", result["recommendations"])

    def test_detects_quality_gate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".config" / "nextest").mkdir(parents=True)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "fuzz" / "fuzz_targets").mkdir(parents=True)
            (root / "src").mkdir()
            (root / "Cargo.toml").write_text(
                """
[workspace]
members = ["crates/core"]

[package]
name = "quality"
version = "0.2.0"
edition = "2024"

[dependencies]
serde = "1"
""".strip()
            )
            (root / "Cargo.lock").write_text("# lock")
            (root / "deny.toml").write_text("[advisories]\n")
            (root / ".config" / "nextest" / "config.toml").write_text("[profile.default]\n")
            (root / "fuzz" / "fuzz_targets" / "parser.rs").write_text("fuzz_target!(|data: &[u8]| {});")
            (root / ".github" / "workflows" / "coverage.yml").write_text("cargo llvm-cov nextest\n")
            (root / "src" / "lib.rs").write_text("pub fn parse(_: &[u8]) {}\n")
            result = run_audit(root)
        self.assertIn("workspace configured", result["strengths"])
        self.assertIn("Cargo.lock present", result["strengths"])
        self.assertIn("cargo-deny config present", result["strengths"])
        self.assertIn("nextest config present", result["strengths"])
        self.assertIn("fuzz targets present", result["strengths"])
        self.assertIn("coverage workflow present", result["strengths"])
        self.assertIn("semver-sensitive public library API", result["findings"])
        self.assertIn("consider cargo-semver-checks before release", result["recommendations"])
        self.assertIn("Miri can be useful for parser or unsafe-adjacent tests", result["recommendations"])


if __name__ == "__main__":
    unittest.main()
