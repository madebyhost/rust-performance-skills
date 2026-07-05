#!/usr/bin/env python3
"""Validate the Rust expert rulebook."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules"
INDEX = RULES_DIR / "index.json"
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
SEVERITIES = {"critical", "high", "medium", "low", "reference"}
MIN_RULES = 275


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


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
    return data


def validate_rule(path: Path) -> None:
    data = parse_rule(path)
    for field in FIELDS:
        if not data.get(field):
            fail(f"{path.relative_to(ROOT)} missing {field}")
    if data["id"] != path.stem:
        fail(f"{path.relative_to(ROOT)} id must match filename")
    if data["severity"] not in SEVERITIES:
        fail(f"{path.relative_to(ROOT)} has invalid severity {data['severity']}")
    for field in ["sources", "related_rules"]:
        if "- " not in data[field]:
            fail(f"{path.relative_to(ROOT)} {field} must be a list")


def validate() -> None:
    if not RULES_DIR.exists():
        fail("rules directory is missing")
    files = sorted(path for path in RULES_DIR.glob("*.md") if path.name != "README.md")
    if len(files) < MIN_RULES:
        fail(f"expected at least {MIN_RULES} rules, found {len(files)}")
    for path in files:
        validate_rule(path)

    if not INDEX.exists():
        fail("rules/index.json is missing")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    indexed = {entry["id"] for entry in index.get("rules", [])}
    file_ids = {path.stem for path in files}
    if indexed != file_ids:
        missing = sorted(file_ids - indexed)
        extra = sorted(indexed - file_ids)
        fail(f"index mismatch missing={missing[:5]} extra={extra[:5]}")


def main() -> int:
    validate()
    print("rulebook validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
