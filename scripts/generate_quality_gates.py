#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def add_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def has_signal(audit: dict, needle: str) -> bool:
    haystack = "\n".join(
        str(item)
        for key in ["project_type", "findings", "strengths", "recommendations"]
        for item in ([audit.get(key, "")] if isinstance(audit.get(key), str) else audit.get(key, []))
    ).lower()
    return needle.lower() in haystack


def generate(audit: dict) -> dict:
    commands: list[str] = []
    notes: list[str] = []

    add_unique(commands, "cargo fmt --check")
    add_unique(commands, "cargo clippy --all-targets --all-features -- -D warnings")
    add_unique(commands, "cargo nextest run --all-features")
    add_unique(commands, "cargo deny check")
    add_unique(commands, "RUSTDOCFLAGS=\"-D warnings\" cargo doc --no-deps --all-features")

    if has_signal(audit, "semver-sensitive public library API") or has_signal(audit, "public library"):
        add_unique(commands, "cargo semver-checks check-release")

    if audit.get("project_type") == "pyo3-extension" or has_signal(audit, "pyo3"):
        add_unique(commands, "maturin build --release")
        add_unique(notes, "Install and test the built wheel in a clean Python environment.")

    if audit.get("project_type") == "wasm" or has_signal(audit, "wasm"):
        add_unique(commands, "wasm-pack test --node")
        add_unique(commands, "wasm-pack build --release")

    if audit.get("project_type") == "tauri-app" or has_signal(audit, "tauri"):
        add_unique(commands, "cargo tauri build")
        if any(has_signal(audit, token) for token in ["android", "mobile"]):
            add_unique(commands, "cargo tauri android build")
        if any(has_signal(audit, token) for token in ["ios", "mobile"]):
            add_unique(commands, "cargo tauri ios build")
        add_unique(notes, "Smoke-test Tauri bundles on every desktop/mobile target in scope, including signing and system webview assumptions.")

    if has_signal(audit, "unsafe Rust present") or has_signal(audit, "parser"):
        add_unique(commands, "cargo +nightly miri test")
        add_unique(notes, "Run Miri on targeted tests if dependencies support it.")

    if has_signal(audit, "fuzz targets present"):
        add_unique(commands, "cargo fuzz run <target>")

    if has_signal(audit, "low-latency/HFT vocabulary present"):
        add_unique(commands, "cargo bench")
        add_unique(notes, "Run latency benchmarks on controlled hardware and report p99/p999.")

    if not has_signal(audit, "cargo-deny config present"):
        add_unique(notes, "Add deny.toml before enforcing cargo deny in CI.")

    return {"commands": commands, "notes": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Rust quality gate commands from rust_project_audit.py JSON.")
    parser.add_argument("audit_json", help="Path to audit JSON")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    try:
        audit = json.loads(Path(args.audit_json).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read audit JSON: {exc}", file=sys.stderr)
        return 2

    result = generate(audit)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Commands:")
        for command in result["commands"]:
            print(f"- {command}")
        if result["notes"]:
            print("\nNotes:")
            for note in result["notes"]:
                print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
