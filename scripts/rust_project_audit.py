#!/usr/bin/env python3
import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


HFT_RE = re.compile(r"hft|multicast|ring[_ -]?buffer|disruptor|orderbook|order_book|market[_ -]?data|low[_ -]?latency", re.I)
UNSAFE_RE = re.compile(r"\bunsafe\b|\*const\b|\*mut\b|transmute|MaybeUninit|NonNull")


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
    result["project_type"] = detect_project_type(cargo, pyproject, deps)

    package = cargo.get("package", {})
    if package.get("edition") == "2024":
        result["strengths"].append("edition 2024 configured")
    else:
        result["recommendations"].append("consider edition 2024 for new crates when MSRV allows")

    profile = cargo.get("profile", {}).get("release", {})
    if profile:
        result["strengths"].append("release profile configured")
        if "lto" not in profile:
            result["recommendations"].append("evaluate lto for release performance or size")
        if "codegen-units" not in profile:
            result["recommendations"].append("evaluate codegen-units=1 for release hot paths")
    else:
        result["findings"].append("no explicit release profile")
        result["recommendations"].append("document release profile tradeoffs before performance claims")

    lints = cargo.get("lints", {})
    if lints.get("rust", {}).get("unsafe_code") in {"warn", "deny", "forbid"}:
        result["strengths"].append("unsafe_code lint configured")
    else:
        result["recommendations"].append("configure unsafe_code lint and local unsafe allowances")

    if "pyo3" in deps:
        result["strengths"].append("PyO3 dependency detected")
        if has_cdylib(cargo):
            result["strengths"].append("cdylib crate type configured")
        result["recommendations"].append("consider Python::detach for CPU-heavy Rust work")
        result["recommendations"].append("benchmark Python caller to include conversion and boundary cost")
    if pyproject and "maturin" in str(pyproject).lower():
        result["strengths"].append("maturin packaging detected")

    if {"wasm-bindgen", "web-sys", "js-sys"} & deps:
        result["strengths"].append("Wasm dependency detected")
        result["recommendations"].append("measure generated wasm and JS boundary cost")
        result["recommendations"].append("separate size tuning from runtime performance tuning")

    if UNSAFE_RE.search(sources):
        result["findings"].append("unsafe Rust present")
        result["recommendations"].append("require SAFETY comments and soundness review")
        result["recommendations"].append("run Miri or sanitizers where supported")

    if HFT_RE.search(sources) or HFT_RE.search(cargo_path.read_text(encoding="utf-8")):
        result["findings"].append("low-latency/HFT vocabulary present")
        result["recommendations"].append("capture p99/p999 latency, drops, queue depth, and replay behavior")

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
