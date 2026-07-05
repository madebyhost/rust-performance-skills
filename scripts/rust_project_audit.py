#!/usr/bin/env python3
import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


HFT_RE = re.compile(r"hft|multicast|ring[_ -]?buffer|disruptor|orderbook|order_book|market[_ -]?data|low[_ -]?latency", re.I)
EBPF_RE = re.compile(
    r"\bebpf\b|\bbpf_|\bBPF_(?:PROG|MAP)_TYPE|af_xdp|\bxdp\b|xskmap|cpumap|devmap|sockmap|sockhash|"
    r"kprobe|uprobe|tracepoint|\btc\b|\btcx\b|ringbuf|verifier|bounded loop|tail call|aya[_-]?bpf|libbpf",
    re.I,
)
SBE_RE = re.compile(
    r"\bsbe\b|simple binary encoding|messageHeader|templateId|schemaId|blockLength|actingVersion|"
    r"actingBlockLength|semanticType|messageSchema",
    re.I,
)
MATH_RE = re.compile(
    r"\bbfs\b|\bdfs\b|dijkstra|a\*|astar|markov|monte\s*carlo|montecarlo|poisson|"
    r"bellman|floyd|kruskal|prim|pagerank|toposort|sparse matrix|linear algebra|simulation",
    re.I,
)
MEMORY_SIMD_IO_RE = re.compile(
    r"memmap|mmap|io[_-]?uring|o_direct|direct i/o|page fault|huge\s*pages?|hugetlb|transparent huge|"
    r"\bnuma\b|cache\s*line|false sharing|prefetch|core::arch|std::simd|portable_simd|target_feature|"
    r"\bsimd\b|\bsoa\b|\baos\b|allocator|jemalloc|mimalloc|bumpalo|arena|slab|bytemuck|zerocopy|"
    r"zero-copy|zerocopy",
    re.I,
)
UNSAFE_RE = re.compile(r"\bunsafe\b|\*const\b|\*mut\b|transmute|MaybeUninit|NonNull")
PUBLIC_API_RE = re.compile(r"(?m)^\s*pub\s+(?:unsafe\s+)?(?:async\s+)?(?:fn|struct|enum|trait|mod|type|const|static)\b")
PARSER_RE = re.compile(r"\bparse(?:r|_|\b)|decode|deserialize", re.I)
PROJECT_TEXT_EXTENSIONS = {".rs", ".toml", ".xml", ".sbe", ".proto", ".fbs", ".yaml", ".yml"}
EBPF_DEPS = {"aya", "aya-bpf", "libbpf-rs", "libbpf-cargo", "redbpf", "rbpf"}
SBE_DEPS = {"sbe", "sbe-codegen", "simple-binary-encoding", "fix-sbe", "fix-simple-binary-encoding"}
MATH_DEPS = {"petgraph", "ndarray", "nalgebra", "sprs", "faer", "statrs", "rand_distr", "argmin"}
MEMORY_SIMD_IO_DEPS = {
    "memmap2",
    "io-uring",
    "mimalloc",
    "tikv-jemallocator",
    "tikv-jemalloc-ctl",
    "bumpalo",
    "bytemuck",
    "zerocopy",
    "wide",
    "safe_arch",
    "aligned-vec",
    "crossbeam-utils",
    "slab",
}


def load_toml(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return {"__parse_error__": str(exc)}


def read_rust_sources(root: Path) -> str:
    chunks: list[str] = []
    for path in root.rglob("*.rs"):
        if any(part in {"target", ".git"} for part in path.parts):
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def read_project_text(root: Path) -> str:
    chunks: list[str] = []
    for path in root.rglob("*"):
        if any(part in {"target", ".git"} for part in path.parts):
            continue
        if not path.is_file() or path.name == "Cargo.lock" or path.suffix not in PROJECT_TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def dependencies(cargo: dict) -> set[str]:
    deps: set[str] = set()
    for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
        value = cargo.get(section, {})
        if isinstance(value, dict):
            deps.update(value.keys())
    return deps


def has_cdylib(cargo: dict) -> bool:
    crate_type = cargo.get("lib", {}).get("crate-type", [])
    return "cdylib" in crate_type


def has_nextest_config(root: Path) -> bool:
    return any(
        path.exists()
        for path in [
            root / ".config" / "nextest" / "config.toml",
            root / ".config" / "nextest.toml",
            root / "nextest.toml",
        ]
    )


def has_cargo_deny_config(root: Path) -> bool:
    return any(
        path.exists()
        for path in [
            root / "deny.toml",
            root / ".cargo" / "deny.toml",
            root / ".config" / "cargo-deny" / "deny.toml",
        ]
    )


def has_fuzz_targets(root: Path) -> bool:
    fuzz_dir = root / "fuzz" / "fuzz_targets"
    return fuzz_dir.exists() and any(fuzz_dir.glob("*.rs"))


def has_coverage_workflow(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    if not workflows.exists():
        return False
    for path in list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml")):
        try:
            if "llvm-cov" in path.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def detect_project_type(cargo: dict, pyproject: dict | None, deps: set[str]) -> str:
    if "pyo3" in deps or "maturin" in (pyproject or {}).get("build-system", {}).get("build-backend", ""):
        return "pyo3-extension"
    if {"wasm-bindgen", "web-sys", "js-sys"} & deps:
        return "wasm"
    if cargo.get("__parse_error__"):
        return "invalid-cargo"
    return "rust"


def audit(root: Path) -> dict:
    root = root.resolve()
    cargo_path = root / "Cargo.toml"
    result = {
        "path": str(root),
        "project_type": "unknown",
        "strengths": [],
        "findings": [],
        "recommendations": [],
    }

    if not cargo_path.exists():
        result["findings"].append("missing Cargo.toml")
        result["recommendations"].append("run audit from a Rust crate or workspace root")
        return result

    cargo = load_toml(cargo_path)
    if cargo.get("__parse_error__"):
        result["project_type"] = "invalid-cargo"
        result["findings"].append(f"Cargo.toml parse error: {cargo['__parse_error__']}")
        return result

    pyproject_path = root / "pyproject.toml"
    pyproject = load_toml(pyproject_path) if pyproject_path.exists() else None
    deps = dependencies(cargo)
    sources = read_rust_sources(root)
    project_text = read_project_text(root)
    result["project_type"] = detect_project_type(cargo, pyproject, deps)

    package = cargo.get("package", {})
    if "workspace" in cargo:
        append_unique(result["strengths"], "workspace configured")
    if (root / "Cargo.lock").exists():
        append_unique(result["strengths"], "Cargo.lock present")
    if has_cargo_deny_config(root):
        append_unique(result["strengths"], "cargo-deny config present")
    if has_nextest_config(root):
        append_unique(result["strengths"], "nextest config present")
    if has_fuzz_targets(root):
        append_unique(result["strengths"], "fuzz targets present")
    if has_coverage_workflow(root):
        append_unique(result["strengths"], "coverage workflow present")

    if package.get("edition") == "2024":
        append_unique(result["strengths"], "edition 2024 configured")
    else:
        append_unique(result["recommendations"], "consider edition 2024 for new crates when MSRV allows")

    profile = cargo.get("profile", {}).get("release", {})
    if profile:
        append_unique(result["strengths"], "release profile configured")
        if "lto" not in profile:
            append_unique(result["recommendations"], "evaluate lto for release performance or size")
        if "codegen-units" not in profile:
            append_unique(result["recommendations"], "evaluate codegen-units=1 for release hot paths")
    else:
        append_unique(result["findings"], "no explicit release profile")
        append_unique(result["recommendations"], "document release profile tradeoffs before performance claims")

    lints = cargo.get("lints", {})
    if lints.get("rust", {}).get("unsafe_code") in {"warn", "deny", "forbid"}:
        append_unique(result["strengths"], "unsafe_code lint configured")
    else:
        append_unique(result["recommendations"], "configure unsafe_code lint and local unsafe allowances")

    if PUBLIC_API_RE.search(sources):
        append_unique(result["findings"], "semver-sensitive public library API")
        append_unique(result["recommendations"], "consider cargo-semver-checks before release")

    if "pyo3" in deps:
        append_unique(result["strengths"], "PyO3 dependency detected")
        if has_cdylib(cargo):
            append_unique(result["strengths"], "cdylib crate type configured")
        append_unique(result["recommendations"], "consider Python::detach for CPU-heavy Rust work")
        append_unique(result["recommendations"], "benchmark Python caller to include conversion and boundary cost")
    if pyproject and "maturin" in str(pyproject).lower():
        append_unique(result["strengths"], "maturin packaging detected")

    if {"wasm-bindgen", "web-sys", "js-sys"} & deps:
        append_unique(result["strengths"], "Wasm dependency detected")
        append_unique(result["recommendations"], "measure generated wasm and JS boundary cost")
        append_unique(result["recommendations"], "separate size tuning from runtime performance tuning")

    if UNSAFE_RE.search(sources):
        append_unique(result["findings"], "unsafe Rust present")
        append_unique(result["recommendations"], "require SAFETY comments and soundness review")
        append_unique(result["recommendations"], "run Miri or sanitizers where supported")

    if PARSER_RE.search(sources) or UNSAFE_RE.search(sources):
        append_unique(result["recommendations"], "Miri can be useful for parser or unsafe-adjacent tests")

    if HFT_RE.search(sources) or HFT_RE.search(cargo_path.read_text(encoding="utf-8")):
        append_unique(result["findings"], "low-latency/HFT vocabulary present")
        append_unique(result["recommendations"], "capture p99/p999 latency, drops, queue depth, and replay behavior")

    if EBPF_RE.search(project_text) or EBPF_DEPS & deps:
        append_unique(result["findings"], "eBPF/kernel performance signals present")
        if EBPF_DEPS & deps:
            append_unique(result["strengths"], "eBPF Rust tooling detected")
        append_unique(result["recommendations"], "verify bounded loops, map capacity, and required kernel capabilities")
        append_unique(result["recommendations"], "test eBPF loaders without requiring root in default CI")
        append_unique(result["recommendations"], "separate kernel datapath benchmarks from userspace loader overhead")

    if SBE_RE.search(project_text) or SBE_DEPS & deps:
        append_unique(result["findings"], "SBE/binary codec signals present")
        append_unique(result["recommendations"], "add golden frame fixtures and schema compatibility tests")
        append_unique(result["recommendations"], "verify zero-copy decode lifetimes and endian/block-length handling")
        append_unique(result["recommendations"], "fuzz decoders for truncated frames and unknown template versions")

    if MATH_RE.search(project_text) or MATH_DEPS & deps:
        append_unique(result["findings"], "math/algorithm performance signals present")
        if MATH_DEPS & deps:
            append_unique(result["strengths"], "math and graph tooling detected")
        append_unique(result["recommendations"], "benchmark algorithmic complexity against representative graph sizes")
        append_unique(result["recommendations"], "control RNG seeds and statistical tolerances for simulations")
        append_unique(result["recommendations"], "prefer compact IDs, preallocation, and cache-friendly layouts for graph hot paths")

    if MEMORY_SIMD_IO_RE.search(project_text) or MEMORY_SIMD_IO_DEPS & deps:
        append_unique(result["findings"], "memory/SIMD/I/O performance signals present")
        if MEMORY_SIMD_IO_DEPS & deps:
            append_unique(result["strengths"], "allocator and zero-copy tooling detected")
        append_unique(result["recommendations"], "benchmark allocator choice with representative allocation lifetimes")
        append_unique(result["recommendations"], "validate SIMD dispatch, scalar fallback, and target-feature safety")
        append_unique(result["recommendations"], "measure page faults, mmap behavior, and io_uring queue depth under load")
        append_unique(result["recommendations"], "document NUMA, huge-page, and direct-I/O deployment assumptions")

    return result


def print_text(result: dict) -> None:
    print(f"Project type: {result['project_type']}")
    for key in ["strengths", "findings", "recommendations"]:
        print(f"\n{key.title()}:")
        values = result[key]
        if values:
            for value in values:
                print(f"- {value}")
        else:
            print("- none")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Rust project performance and binding signals.")
    parser.add_argument("path", nargs="?", default=".", help="Rust project path")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    result = audit(Path(args.path))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
