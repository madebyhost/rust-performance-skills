#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_quality_gates import generate  # noqa: E402
from rust_project_audit import audit  # noqa: E402


TOOLS = [
    {
        "name": "audit_rust_project",
        "description": "Audit Rust project structure and performance signals.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "generate_quality_gates",
        "description": "Generate quality gate commands from audit JSON.",
        "inputSchema": {
            "type": "object",
            "properties": {"audit": {"type": "object"}},
            "required": ["audit"],
        },
    },
    {
        "name": "list_rust_skills",
        "description": "List packaged Rust specialist skills.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "rust_review_checklist",
        "description": "Return a Rust review checklist selected by project signals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_type": {"type": "string"},
                "findings": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
    {
        "name": "detect_performance_domains",
        "description": "Classify performance domains from Rust audit JSON.",
        "inputSchema": {
            "type": "object",
            "properties": {"audit": {"type": "object"}},
            "required": ["audit"],
        },
    },
    {
        "name": "rust_algorithm_checklist",
        "description": "Return algorithm and math performance checks for Rust implementations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "algorithm": {"type": "string"},
                "signals": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
    {
        "name": "binary_encoding_review_checklist",
        "description": "Return binary codec and SBE review checks for Rust implementations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "codec": {"type": "string"},
                "signals": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
]


def list_skills() -> dict[str, Any]:
    skills = []
    for skill in sorted((ROOT / "skills").glob("rust-*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")), skill.parent.name)
        skills.append({"name": skill.parent.name, "title": title})
    return {"skills": skills}


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def audit_signal_text(audit_data: dict[str, Any]) -> str:
    parts = [str(audit_data.get("project_type", ""))]
    for key in ["strengths", "findings", "recommendations"]:
        values = audit_data.get(key, [])
        if isinstance(values, list):
            parts.extend(str(value) for value in values)
    return "\n".join(parts).lower()


def detect_performance_domains(arguments: dict[str, Any]) -> dict[str, Any]:
    text = audit_signal_text(arguments.get("audit", {}))
    domains: list[str] = []
    if any(token in text for token in ["ebpf", "kernel performance", "xdp", "libbpf", "aya"]):
        append_unique(domains, "ebpf")
    if any(token in text for token in ["sbe", "binary codec", "simple binary encoding", "templateid"]):
        append_unique(domains, "sbe")
    if any(token in text for token in ["math/algorithm", "algorithm", "graph", "monte carlo", "poisson", "markov"]):
        append_unique(domains, "math")
    if any(token in text for token in ["low-latency", "hft", "market data", "multicast"]):
        append_unique(domains, "hft")
    if any(token in text for token in ["pyo3", "maturin", "python"]):
        append_unique(domains, "pyo3")
    if "wasm" in text:
        append_unique(domains, "wasm")
    if "unsafe" in text:
        append_unique(domains, "unsafe")
    return {"domains": domains}


def algorithm_checklist(arguments: dict[str, Any]) -> dict[str, Any]:
    algorithm = str(arguments.get("algorithm", "")).lower()
    signals = " ".join(str(signal).lower() for signal in arguments.get("signals", []))
    text = f"{algorithm} {signals}"
    checks = [
        "define input size, density, distribution, and latency target before optimizing",
        "benchmark representative and adversarial datasets",
        "measure allocations, cache misses, and branch misses before changing data layout",
    ]
    if any(token in text for token in ["bfs", "dfs", "dijkstra", "a*", "astar", "petgraph", "graph"]):
        checks.extend(
            [
                "use compact node IDs and cache-friendly adjacency storage",
                "preallocate frontier, distance, and predecessor buffers",
                "avoid hashing and heap churn in the inner traversal loop",
            ]
        )
    if any(token in text for token in ["rayon", "parallel", "threads"]):
        checks.append("parallelize only after partitioning avoids shared hot counters and false sharing")
    if any(token in text for token in ["monte", "markov", "poisson", "rand", "statrs", "simulation"]):
        checks.extend(
            [
                "control RNG seeds and statistical tolerances",
                "separate deterministic unit tests from stochastic convergence tests",
            ]
        )
    return {"checks": checks}


def binary_encoding_checklist(arguments: dict[str, Any]) -> dict[str, Any]:
    codec = str(arguments.get("codec", "")).lower()
    signals = " ".join(str(signal).lower() for signal in arguments.get("signals", []))
    text = f"{codec} {signals}"
    checks = [
        "bounds-check every frame length before indexing",
        "fuzz truncated frames and unknown message versions",
        "keep decode APIs explicit about ownership and byte order",
    ]
    if any(token in text for token in ["sbe", "templateid", "actingversion", "blocklength", "schema"]):
        checks.extend(
            [
                "golden frame fixtures for every schema version",
                "validate block length, template ID, schema ID, and acting version",
                "zero-copy decode lifetimes cannot outlive the frame",
            ]
        )
    return {"checks": checks}


def review_checklist(arguments: dict[str, Any]) -> dict[str, Any]:
    findings = "\n".join(arguments.get("findings", []))
    findings_lower = findings.lower()
    checks = [
        "correctness and API compatibility",
        "tests and CI quality gates",
        "allocation/copy hot paths",
        "error handling and observability",
    ]
    if "unsafe" in findings_lower:
        checks.extend(["SAFETY comments", "Miri or sanitizer suitability", "safe wrapper invariants"])
    if arguments.get("project_type") == "pyo3-extension":
        checks.extend(["Python/Rust boundary cost", "maturin wheel build and import test"])
    if arguments.get("project_type") == "wasm":
        checks.extend(["JS/Wasm boundary cost", "wasm-pack build and test"])
    if "low-latency/HFT vocabulary present" in findings:
        checks.extend(["p99/p999 latency", "drops and queue depth", "CPU/cache/network assumptions"])
    if "ebpf" in findings_lower or "kernel performance" in findings_lower:
        checks.extend(["eBPF verifier, map, and privilege assumptions", "kernel/userspace benchmark separation"])
    if "sbe" in findings_lower or "binary codec" in findings_lower:
        checks.extend(["SBE schema compatibility and golden frames", "zero-copy frame lifetime and bounds handling"])
    if "math/algorithm" in findings_lower or "algorithm" in findings_lower:
        checks.extend(["algorithmic complexity and cache-aware data layout", "deterministic stochastic test tolerances"])
    return {"checks": checks}


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "audit_rust_project":
        return audit(Path(arguments["path"]))
    if name == "generate_quality_gates":
        return generate(arguments["audit"])
    if name == "list_rust_skills":
        return list_skills()
    if name == "rust_review_checklist":
        return review_checklist(arguments)
    if name == "detect_performance_domains":
        return detect_performance_domains(arguments)
    if name == "rust_algorithm_checklist":
        return algorithm_checklist(arguments)
    if name == "binary_encoding_review_checklist":
        return binary_encoding_checklist(arguments)
    raise ValueError(f"unknown tool: {name}")


def rpc_result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def rpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")
    try:
        if method == "initialize":
            return rpc_result(
                request_id,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "rust-performance-skills", "version": "0.1.0"},
                },
            )
        if method == "notifications/initialized":
            return None
        if method == "tools/list":
            return rpc_result(request_id, {"tools": TOOLS})
        if method == "tools/call":
            params = request.get("params", {})
            result = call_tool(params["name"], params.get("arguments", {}))
            return rpc_result(request_id, {"content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}]})
        return rpc_error(request_id, -32601, f"method not found: {method}")
    except Exception as exc:  # noqa: BLE001 - MCP response should surface deterministic error text.
        return rpc_error(request_id, -32000, str(exc))


def run_stdio() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        response = handle_request(json.loads(line))
        if response is not None:
            print(json.dumps(response), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Rust Performance Skills MCP server.")
    parser.add_argument("--list-tools", action="store_true", help="print tool metadata and exit")
    parser.add_argument("--call", help="call one tool directly and exit")
    parser.add_argument("--arguments", default="{}", help="JSON arguments for --call")
    args = parser.parse_args()

    if args.list_tools:
        print(json.dumps({"tools": TOOLS}, indent=2, sort_keys=True))
        return 0
    if args.call:
        print(json.dumps(call_tool(args.call, json.loads(args.arguments)), indent=2, sort_keys=True))
        return 0
    return run_stdio()


if __name__ == "__main__":
    raise SystemExit(main())
