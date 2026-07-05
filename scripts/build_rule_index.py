#!/usr/bin/env python3
"""Build rules/index.json from expert rule cards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules"
FIELDS = [
    "id",
    "severity",
    "trigger",
    "bad",
    "good",
    "when",
    "when_not",
    "verification",
    "sources",
    "related_rules",
]


def parse_rule(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current: str | None = None
    lines: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current is not None:
                data[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        data[current] = "\n".join(lines).strip()

    for field in ["sources", "related_rules"]:
        raw = str(data.get(field, ""))
        data[field] = [
            item[2:].strip()
            for item in raw.splitlines()
            if item.startswith("- ") and item[2:].strip()
        ]
    return data


def domain_for(rule_id: str) -> str:
    prefix = rule_id.split("-", 1)[0]
    return {
        "own": "ownership",
        "err": "errors",
        "mem": "memory",
        "unsafe": "unsafe",
        "api": "api",
        "async": "async",
        "conc": "concurrency",
        "opt": "optimization",
        "num": "numeric",
        "type": "types",
        "trait": "traits",
        "serde": "serde",
        "macro": "macros",
        "anti": "anti-patterns",
        "hft": "hft",
        "sbe": "sbe",
        "ebpf": "ebpf",
        "pyo3": "pyo3",
        "wasm": "wasm",
        "simd": "simd",
        "numa": "numa",
        "math": "math",
        "io": "io",
    }.get(prefix, prefix)


def build_index(rules_dir: Path) -> dict[str, Any]:
    rules = []
    for path in sorted(rules_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        data = parse_rule(path)
        rule_id = str(data.get("id", path.stem))
        rules.append(
            {
                "id": rule_id,
                "severity": data.get("severity", "medium"),
                "domain": domain_for(rule_id),
                "path": str(path.relative_to(ROOT)),
                "trigger": data.get("trigger", ""),
                "sources": data.get("sources", []),
                "related_rules": data.get("related_rules", []),
            }
        )
    return {"schema_version": 1, "rules": rules}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Rust expert rule index.")
    parser.add_argument("--rules-dir", type=Path, default=RULES_DIR)
    args = parser.parse_args()
    index = build_index(args.rules_dir)
    (args.rules_dir / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"indexed {len(index['rules'])} rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
