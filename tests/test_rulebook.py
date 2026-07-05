import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
RULE_INDEX = RULES / "index.json"
REQUIRED_FIELDS = [
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
IMPORTED_RULES = [
    "api-parse-dont-validate",
    "async-no-lock-await",
    "mem-zero-copy",
    "unsafe-safety-comment",
    "anti-unwrap-abuse",
]
ADVANCED_RULES = [
    "hft-udp-multicast-hotpath",
    "hft-disruptor-ring-buffer",
    "sbe-zero-copy-lifetime",
    "ebpf-verifier-bounds",
    "pyo3-release-gil-hotloop",
    "wasm-boundary-copy-budget",
    "simd-runtime-dispatch",
    "numa-affinity-evidence",
    "math-graph-compact-ids",
    "io-uring-backpressure",
]
MARKET_RULES = [
    "async-runtime-deliberate-choice",
    "async-blocking-boundary-budget",
    "api-constructor-owned-boundary",
    "iter-collect-result-boundary",
    "type-enum-over-boolean-parameter",
    "readability-early-return-control-flow",
    "const-named-domain-values",
    "qa-local-quality-gate",
]


def load_rule(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
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

    for list_field in ["sources", "related_rules"]:
        raw = str(data.get(list_field, ""))
        data[list_field] = [
            item[2:].strip()
            for item in raw.splitlines()
            if item.startswith("- ") and item[2:].strip()
        ]
    return data


class RulebookTest(unittest.TestCase):
    def test_rulebook_has_expert_scale(self) -> None:
        files = sorted(path for path in RULES.glob("*.md") if path.name != "README.md")
        self.assertGreaterEqual(len(files), 283)

    def test_every_rule_uses_expert_card_schema(self) -> None:
        for path in sorted(RULES.glob("*.md")):
            if path.name == "README.md":
                continue
            with self.subTest(rule=path.name):
                rule = load_rule(path)
                for field in REQUIRED_FIELDS:
                    self.assertIn(field, rule, f"{path} missing {field}")
                    self.assertTrue(rule[field], f"{path} has empty {field}")
                self.assertEqual(path.stem, rule["id"])
                self.assertIn(rule["severity"], {"critical", "high", "medium", "low", "reference"})

    def test_imported_leonardomso_rules_are_present_with_examples(self) -> None:
        for rule_id in IMPORTED_RULES:
            with self.subTest(rule=rule_id):
                rule = load_rule(RULES / f"{rule_id}.md")
                self.assertIn("leonardomso/rust-skills", "\n".join(rule["sources"]))
                self.assertIn("```rust", str(rule["bad"]))
                self.assertIn("```rust", str(rule["good"]))

    def test_advanced_plugin_rules_are_present(self) -> None:
        for rule_id in ADVANCED_RULES:
            with self.subTest(rule=rule_id):
                rule = load_rule(RULES / f"{rule_id}.md")
                self.assertIn("rust-performance-skills", "\n".join(rule["sources"]))
                self.assertIn("measure", str(rule["verification"]).lower())

    def test_mcpmarket_review_rules_are_present_and_improved(self) -> None:
        for rule_id in MARKET_RULES:
            with self.subTest(rule=rule_id):
                rule = load_rule(RULES / f"{rule_id}.md")
                sources = "\n".join(rule["sources"])
                self.assertIn("mcpmarket", sources.lower())
                self.assertIn("thrashr888-agent-kit", sources)
                self.assertIn("when_not", rule)
                self.assertNotIn("Use tokio for Async Runtime", str(rule["good"]))

    def test_rule_index_matches_rule_files(self) -> None:
        index = json.loads(RULE_INDEX.read_text(encoding="utf-8"))
        indexed = {entry["id"]: entry for entry in index["rules"]}
        files = {path.stem for path in RULES.glob("*.md") if path.name != "README.md"}
        self.assertEqual(files, set(indexed))
        for rule_id in IMPORTED_RULES + ADVANCED_RULES:
            self.assertIn(rule_id, indexed)
            self.assertTrue(indexed[rule_id]["path"].startswith("rules/"))

        for rule_id in MARKET_RULES:
            self.assertIn(rule_id, indexed)

    def test_rulebook_skill_and_eval_exist(self) -> None:
        skill = ROOT / "skills" / "rust-expert-rulebook" / "SKILL.md"
        self.assertTrue(skill.exists())
        text = skill.read_text(encoding="utf-8")
        self.assertIn("rules/index.json", text)
        self.assertIn("rule IDs", text)
        self.assertTrue((ROOT / "evals" / "rust-expert-rulebook.md").exists())

    def test_mcpmarket_review_document_exists(self) -> None:
        review = ROOT / "docs" / "mcpmarket-rust-best-practices-review.md"
        self.assertTrue(review.exists())
        text = review.read_text(encoding="utf-8")
        self.assertIn("Good as-is", text)
        self.assertIn("Improved before adding", text)
        self.assertIn("mcpmarket.com/tools/skills/rust-best-practices", text)


if __name__ == "__main__":
    unittest.main()
