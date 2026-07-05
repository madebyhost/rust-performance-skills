#!/usr/bin/env python3
"""Import and normalize Rust rule cards from leonardomso/rust-skills.

The source repository is MIT licensed. This script converts the upstream rule
shape into this project's stricter expert-card schema and appends rules that
are specific to rust-performance-skills.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("/tmp/rust-skills-research/leonardomso-rust-skills/rules")
RULES_DIR = ROOT / "rules"
UPSTREAM_SOURCE = "leonardomso/rust-skills: https://github.com/leonardomso/rust-skills"
PLUGIN_SOURCE = "rust-performance-skills: https://github.com/madebyhost/rust-performance-skills"
MCPMARKET_SOURCE = "mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices"
THRASHR_SOURCE = "thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices"

ASCII_REPLACEMENTS = {
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",
    "\u2212": "-",
    "\u2192": "->",
    "\u21d2": "=>",
    "\u2260": "!=",
    "\u2248": "~=",
    "\u2264": "<=",
    "\u2265": ">=",
    "\u2287": "superset-or-equal",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u00a0": " ",
    "\u00b5": "u",
    "\u00d7": "x",
    "\u2026": "...",
    "\u2502": "|",
    "\u251c": "|",
    "\u2514": "`",
    "\u2500": "-",
}


SEVERITY_BY_PREFIX = {
    "own": "critical",
    "err": "critical",
    "mem": "critical",
    "unsafe": "critical",
    "api": "high",
    "async": "high",
    "conc": "high",
    "opt": "high",
    "num": "high",
    "type": "medium",
    "trait": "medium",
    "conv": "medium",
    "const": "medium",
    "serde": "medium",
    "pat": "medium",
    "macro": "medium",
    "closure": "medium",
    "coll": "medium",
    "name": "medium",
    "test": "medium",
    "doc": "medium",
    "obs": "medium",
    "perf": "medium",
    "proj": "low",
    "lint": "low",
    "anti": "reference",
}


DOMAIN_BY_PREFIX = {
    "own": "ownership and borrowing",
    "err": "error handling",
    "mem": "memory and allocation",
    "unsafe": "unsafe soundness",
    "api": "public API design",
    "async": "async runtime and cancellation",
    "conc": "concurrency and synchronization",
    "opt": "compiler optimization",
    "num": "numeric safety",
    "type": "type-system invariants",
    "trait": "traits and generics",
    "conv": "conversion boundaries",
    "const": "compile-time evaluation",
    "serde": "serialization compatibility",
    "pat": "pattern matching",
    "macro": "macro API design",
    "closure": "closures and callbacks",
    "coll": "collections",
    "name": "naming and readability",
    "test": "testing strategy",
    "doc": "documentation",
    "obs": "observability",
    "perf": "performance patterns",
    "proj": "project structure",
    "lint": "linting",
    "anti": "anti-patterns",
}


VERIFICATION_BY_PREFIX = {
    "mem": "Measure allocations, copies, cache misses, and benchmark deltas on representative inputs.",
    "perf": "Measure before and after with a benchmark that captures the suspected bottleneck.",
    "opt": "Inspect release profile, generated code when useful, and benchmark hot paths before keeping the change.",
    "async": "Add concurrency tests, cancellation tests, and runtime checks for backpressure or lock scope.",
    "conc": "Use stress tests, loom where practical, and contention measurements for shared state.",
    "unsafe": "Require SAFETY documentation, Miri or sanitizer coverage where possible, and safe-wrapper tests.",
    "api": "Compile examples, run semver checks for public APIs, and add tests for boundary behavior.",
    "type": "Add constructor tests, compile-fail tests where useful, and property tests for invariants.",
    "serde": "Use golden fixtures, versioned payload tests, and compatibility checks for unknown or missing fields.",
    "macro": "Add compile-pass and compile-fail tests covering exported macro paths and helper visibility.",
    "test": "Verify the test fails before the fix and covers the intended behavior rather than implementation detail.",
    "lint": "Run cargo clippy with the intended lint level and document any allow with a narrow reason.",
}


WHEN_NOT_BY_PREFIX = {
    "mem": "Do not apply when ownership is required for correctness, lifetime complexity would dominate the API, or measurement shows no meaningful allocation/copy cost.",
    "perf": "Do not apply when the path is cold, unmeasured, or the optimization makes correctness and maintenance worse than the measured gain.",
    "opt": "Do not apply compiler hints globally or speculatively; keep them for measured hot paths and deployment-specific profiles.",
    "async": "Do not force async for CPU-bound work without I/O concurrency; prefer threads or Rayon when they fit the workload.",
    "conc": "Do not add shared mutable state, atomics, or lock-free structures when ownership transfer or single-threaded design is simpler.",
    "unsafe": "Do not use unsafe to silence the borrow checker without a written invariant and a safe abstraction boundary.",
    "api": "Do not over-generalize a public API before real consumers or compatibility constraints exist.",
    "type": "Do not encode every boolean as typestate; use the type system when it removes real invalid states.",
    "serde": "Do not make serde strict when extension fields are expected or when backward compatibility requires tolerance.",
    "macro": "Do not write a macro when a function, trait, or const generic expresses the same idea clearly.",
}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    trigger: str
    bad: str
    good: str
    when: str
    when_not: str
    verification: str
    sources: list[str]
    related_rules: list[str]


def prefix_for(rule_id: str) -> str:
    return rule_id.split("-", 1)[0]


def ascii_clean(value: str) -> str:
    for old, new in ASCII_REPLACEMENTS.items():
        value = value.replace(old, new)
    value = value.encode("ascii", "ignore").decode("ascii")
    return "\n".join(line.rstrip() for line in value.splitlines()) + "\n"


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def summary_from(text: str, rule_id: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(">"):
            return line.lstrip("> ").strip()
    return rule_id.replace("-", " ")


def compact(section: str, fallback: str) -> str:
    value = section.strip()
    if not value:
        return fallback
    return value


def related_from(text: str) -> list[str]:
    section = extract_section(text, "See Also")
    related = []
    for match in re.finditer(r"\(([^)]+\.md)\)", section):
        related.append(Path(match.group(1)).stem)
    return sorted(set(related)) or ["none"]


def imported_rule(path: Path) -> Rule:
    rule_id = path.stem
    prefix = prefix_for(rule_id)
    text = path.read_text(encoding="utf-8")
    summary = summary_from(text, rule_id)
    domain = DOMAIN_BY_PREFIX.get(prefix, "Rust")
    bad = compact(
        extract_section(text, "Bad"),
        f"Avoid applying `{rule_id}` blindly. The risky pattern is code that ignores: {summary}.",
    )
    good = compact(
        extract_section(text, "Good"),
        f"Prefer the design encouraged by `{rule_id}`: {summary}. Keep it explicit and testable.",
    )
    return Rule(
        rule_id=rule_id,
        severity=SEVERITY_BY_PREFIX.get(prefix, "medium"),
        trigger=f"{summary}. Trigger when working on {domain} and the code shows `{prefix}`-class risk.",
        bad=bad,
        good=good,
        when=f"Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.",
        when_not=WHEN_NOT_BY_PREFIX.get(
            prefix,
            "Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.",
        ),
        verification=VERIFICATION_BY_PREFIX.get(
            prefix,
            "Add focused tests or static checks that prove the intended behavior and prevent regression.",
        ),
        sources=[UPSTREAM_SOURCE, "Rust API Guidelines: https://rust-lang.github.io/api-guidelines/"],
        related_rules=related_from(text),
    )


ADVANCED_RULES = [
    Rule(
        rule_id="hft-udp-multicast-hotpath",
        severity="critical",
        trigger="UDP multicast market-data ingest, packet fanout, feed handlers, or replay paths with tail-latency constraints.",
        bad="""```rust
async fn on_packet(socket: UdpSocket) {
    let mut buf = vec![0_u8; 2048];
    loop {
        let n = socket.recv(&mut buf).await.unwrap();
        println!("packet {:?}", &buf[..n]);
        process(buf[..n].to_vec()).await;
    }
}
```""",
        good="""```rust
fn on_packet(buf: &mut [u8], ring: &mut Ring<Frame>) -> Result<(), DropReason> {
    let frame = decode_borrowed(buf)?;
    ring.try_publish(frame).map_err(|_| DropReason::Backpressure)
}
```""",
        when="Use for feed handlers that must minimize copies, allocations, logging, scheduler hops, and unbounded queues.",
        when_not="Do not force this shape for admin traffic, control planes, or low-rate feeds where clarity is the primary constraint.",
        verification="Measure packet drops, p99/p999 latency, allocation count, syscall count, queue depth, and replay determinism.",
        sources=[PLUGIN_SOURCE, "Linux networking documentation: https://docs.kernel.org/networking/"],
        related_rules=["mem-zero-copy", "async-bounded-channel", "perf-batch-processing"],
    ),
    Rule(
        rule_id="hft-disruptor-ring-buffer",
        severity="critical",
        trigger="Single-writer or staged low-latency pipelines where queues, locks, or heap churn dominate handoff cost.",
        bad="""```rust
let (tx, rx) = tokio::sync::mpsc::unbounded_channel();
tx.send(event.clone()).unwrap();
```""",
        good="""```rust
let slot = ring.claim()?;
slot.write(event);
ring.publish(slot.sequence());
```""",
        when="Use when the topology, producers, consumers, and backpressure policy are known and benchmarked.",
        when_not="Do not add disruptor-style architecture when normal bounded channels satisfy the latency budget.",
        verification="Measure handoff latency, false sharing, sequence contention, backpressure behavior, and shutdown recovery.",
        sources=[PLUGIN_SOURCE, "LMAX Disruptor: https://lmax-exchange.github.io/disruptor/"],
        related_rules=["conc-atomic-ordering", "mem-assert-type-size", "hft-udp-multicast-hotpath"],
    ),
    Rule(
        rule_id="sbe-zero-copy-lifetime",
        severity="critical",
        trigger="SBE, fixed-layout binary codecs, market-data frames, or borrowed decoders over network buffers.",
        bad="""```rust
struct Message {
    symbol: String,
}
fn decode(buf: &[u8]) -> Message {
    Message { symbol: String::from_utf8(buf[8..16].to_vec()).unwrap() }
}
```""",
        good="""```rust
struct Message<'a> {
    symbol: &'a [u8],
}
fn decode<'a>(buf: &'a [u8]) -> Result<Message<'a>, DecodeError> {
    Ok(Message { symbol: checked_field(buf, 8, 8)? })
}
```""",
        when="Use when decoded fields can borrow from the frame and the frame lifetime is tied to processing.",
        when_not="Do not return borrowed views beyond the frame owner or across async/task boundaries without ownership strategy.",
        verification="Measure copies, fuzz truncated frames, and test schema ID, template ID, block length, acting version, endian, and bounds.",
        sources=[PLUGIN_SOURCE, "Real Logic SBE: https://github.com/real-logic/simple-binary-encoding"],
        related_rules=["mem-zero-copy", "unsafe-maybeuninit", "type-repr-transparent"],
    ),
    Rule(
        rule_id="ebpf-verifier-bounds",
        severity="critical",
        trigger="Rust eBPF/XDP/tc programs that parse packet bytes, use maps, or interact with verifier-sensitive pointer arithmetic.",
        bad="""```rust
let eth = unsafe { *(ctx.data() as *const EthHdr) };
let proto = unsafe { *ctx.data().add(14) };
```""",
        good="""```rust
let start = ctx.data();
let end = ctx.data_end();
let eth = ptr_at::<EthHdr>(start, end, 0)?;
let proto = checked_byte(start, end, EthHdr::LEN)?;
```""",
        when="Use for kernel-side packet parsers and probe programs where every byte access must prove bounds to the verifier.",
        when_not="Do not hide verifier-critical bounds behind abstractions the verifier cannot inline or reason about.",
        verification="Measure verifier acceptance, instruction count, map lookup cost, drop/pass counters, and userspace/kernel benchmark separation.",
        sources=[PLUGIN_SOURCE, "docs.ebpf.io: https://docs.ebpf.io/", "Linux BPF docs: https://docs.kernel.org/bpf/"],
        related_rules=["unsafe-minimize-scope", "unsafe-safety-comment", "num-cast-try-from"],
    ),
    Rule(
        rule_id="pyo3-release-gil-hotloop",
        severity="high",
        trigger="PyO3 extension functions that perform CPU-bound loops, parsing, compression, graph algorithms, or batch transforms.",
        bad="""```rust
#[pyfunction]
fn score_rows(rows: Vec<Row>) -> PyResult<Vec<f64>> {
    Ok(rows.iter().map(score).collect())
}
```""",
        good="""```rust
#[pyfunction]
fn score_rows(py: Python<'_>, rows: Vec<Row>) -> PyResult<Vec<f64>> {
    py.detach(|| Ok(rows.par_iter().map(score).collect()))
}
```""",
        when="Use when work is pure Rust, CPU-bound, and does not touch Python objects inside the hot loop.",
        when_not="Do not release the GIL around code that calls Python APIs or holds Python object references without correct ownership.",
        verification="Measure Python/Rust boundary overhead, GIL hold time, batch size sensitivity, wheel import tests, and threaded contention.",
        sources=[PLUGIN_SOURCE, "PyO3 guide: https://pyo3.rs/", "maturin: https://www.maturin.rs/"],
        related_rules=["conc-rayon-par-iter", "mem-zero-copy", "err-thiserror-lib"],
    ),
    Rule(
        rule_id="wasm-boundary-copy-budget",
        severity="high",
        trigger="Rust/Wasm modules exchanging strings, arrays, frames, images, or simulation buffers with JavaScript.",
        bad="""```rust
#[wasm_bindgen]
pub fn ticks() -> Vec<f64> {
    compute_ticks()
}
```""",
        good="""```rust
#[wasm_bindgen]
pub fn ticks_ptr() -> *const f64 { BUFFER.with(|b| b.as_ptr()) }

#[wasm_bindgen]
pub fn ticks_len() -> usize { BUFFER.with(|b| b.len()) }
```""",
        when="Use when boundary copies dominate runtime or when large typed arrays cross JS/Wasm repeatedly.",
        when_not="Do not expose raw pointers unless lifetime, mutation, and memory growth behavior are documented and tested.",
        verification="Measure JS/Wasm call count, copied bytes, memory growth, wasm size, browser and Node tests, and fallback behavior.",
        sources=[PLUGIN_SOURCE, "wasm-bindgen: https://rustwasm.github.io/docs/wasm-bindgen/"],
        related_rules=["mem-zero-copy", "type-repr-transparent", "api-must-use"],
    ),
    Rule(
        rule_id="simd-runtime-dispatch",
        severity="high",
        trigger="SIMD acceleration using core::arch, std::simd, target_feature, or CPU-specific hot paths.",
        bad="""```rust
#[target_feature(enable = "avx2")]
unsafe fn sum_avx2(xs: &[f32]) -> f32 {
    simd_sum(xs)
}
```""",
        good="""```rust
fn sum(xs: &[f32]) -> f32 {
    if is_x86_feature_detected!("avx2") {
        unsafe { sum_avx2(xs) }
    } else {
        sum_scalar(xs)
    }
}
```""",
        when="Use when profiling shows vectorizable arithmetic, parsing, scanning, or transform work in a hot path.",
        when_not="Do not require a CPU feature unless deployment is pinned to that CPU class or a scalar fallback exists.",
        verification="Measure scalar fallback, CPU feature gates, alignment assumptions, tail handling, and per-target benchmark results.",
        sources=[PLUGIN_SOURCE, "core::arch docs: https://doc.rust-lang.org/core/arch/"],
        related_rules=["opt-simd-portable", "unsafe-minimize-scope", "num-overflow-explicit"],
    ),
    Rule(
        rule_id="numa-affinity-evidence",
        severity="high",
        trigger="CPU pinning, NUMA node placement, huge pages, isolated cores, or memory locality changes.",
        bad="""```rust
pin_thread_to_core(0);
allocate_all_buffers();
```""",
        good="""```rust
pin_thread_to_core(feed_core);
allocate_after_pin(&mut local_pool);
warm_pages(&mut local_pool);
```""",
        when="Use when latency distribution or perf counters show cross-node memory, migrations, or page faults matter.",
        when_not="Do not pin blindly on shared hosts, containers without stable topology, or workloads dominated by I/O waits.",
        verification="Measure CPU migrations, remote memory accesses, page faults, huge-page hit rate, p99/p999 latency, and jitter.",
        sources=[PLUGIN_SOURCE, "Linux NUMA docs: https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html"],
        related_rules=["mem-assert-type-size", "hft-disruptor-ring-buffer", "io-uring-backpressure"],
    ),
    Rule(
        rule_id="math-graph-compact-ids",
        severity="high",
        trigger="BFS, DFS, Dijkstra, A*, Markov chains, Monte Carlo, or graph/numerical kernels with many node lookups.",
        bad="""```rust
let mut distance: HashMap<NodeId, f64> = HashMap::new();
for neighbor in graph.neighbors(node) {
    distance.insert(neighbor.clone(), next);
}
```""",
        good="""```rust
let mut distance = vec![f64::INFINITY; graph.node_count()];
for neighbor in graph.neighbors_idx(node_idx) {
    distance[neighbor] = next;
}
```""",
        when="Use when node IDs can be compacted and the algorithm is memory-bandwidth or cache-latency sensitive.",
        when_not="Do not compact IDs if stable external identifiers dominate API clarity and the graph is small or sparse enough.",
        verification="Measure asymptotic complexity, allocation count, cache misses, deterministic seeds, and adversarial graph cases.",
        sources=[PLUGIN_SOURCE, "petgraph: https://docs.rs/petgraph/", "Rayon: https://docs.rs/rayon/"],
        related_rules=["coll-hashmap-capacity", "mem-with-capacity", "num-float-compare"],
    ),
    Rule(
        rule_id="io-uring-backpressure",
        severity="high",
        trigger="io_uring, mmap, direct I/O, queue-depth tuning, or disk/network I/O pipelines in Rust.",
        bad="""```rust
for request in requests {
    ring.submit(request)?;
}
```""",
        good="""```rust
while in_flight < max_depth {
    submit_next(&mut ring)?;
    in_flight += 1;
}
reap_completions(&mut ring, &mut in_flight)?;
```""",
        when="Use when kernel queue depth, completion batching, or page-cache behavior is part of the performance contract.",
        when_not="Do not use io_uring when portability, simple blocking I/O, or async runtime file APIs already meet the target.",
        verification="Measure queue depth, completion latency, syscalls, page faults, fallback path, and cancellation/shutdown behavior.",
        sources=[PLUGIN_SOURCE, "io-uring crate: https://docs.rs/io-uring/"],
        related_rules=["async-bounded-channel", "mem-reuse-collections", "numa-affinity-evidence"],
    ),
]


MARKET_REVIEW_RULES = [
    Rule(
        rule_id="async-runtime-deliberate-choice",
        severity="high",
        trigger="Async application setup, library APIs that may be runtime-agnostic, or code that adds Tokio without a clear runtime contract.",
        bad="""```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    library_entrypoint().await
}
```""",
        good="""```rust
async fn run(client: Client) -> anyhow::Result<()> {
    client.fetch().await?;
    Ok(())
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    run(Client::new()).await
}
```""",
        when="Use when choosing an async runtime, adding `#[tokio::main]`, or designing library APIs that should not own the executor.",
        when_not="Do not prescribe Tokio inside reusable libraries unless the crate intentionally exposes Tokio-specific types, timers, or I/O traits.",
        verification="Measure runtime worker saturation, blocking sections, cancellation behavior, and test the public API without requiring hidden global runtime state.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Tokio: https://tokio.rs/"],
        related_rules=["async-tokio-runtime", "async-spawn-blocking", "async-cancel-safety"],
    ),
    Rule(
        rule_id="async-blocking-boundary-budget",
        severity="high",
        trigger="Async functions containing synchronous sleep, filesystem, compression, parsing, crypto, CPU-bound loops, or blocking client calls.",
        bad="""```rust
async fn refresh() {
    std::thread::sleep(Duration::from_secs(1));
    let bytes = std::fs::read("snapshot.bin").unwrap();
    parse_big_snapshot(bytes);
}
```""",
        good="""```rust
async fn refresh() -> anyhow::Result<()> {
    tokio::time::sleep(Duration::from_secs(1)).await;
    let bytes = tokio::fs::read("snapshot.bin").await?;
    tokio::task::spawn_blocking(move || parse_big_snapshot(bytes)).await??;
    Ok(())
}
```""",
        when="Use when blocking work can stall async workers or hide latency spikes under load.",
        when_not="Do not move tiny CPU work into `spawn_blocking`; the scheduling overhead can exceed the saved worker time.",
        verification="Measure worker utilization, latency under concurrent load, blocking pool size, cancellation behavior, and queue depth.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Tokio spawn_blocking: https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html"],
        related_rules=["async-spawn-blocking", "async-tokio-fs", "async-bounded-channel"],
    ),
    Rule(
        rule_id="api-constructor-owned-boundary",
        severity="medium",
        trigger="Constructors, builders, or factory functions that receive user-owned strings, paths, byte buffers, or domain values.",
        bad="""```rust
impl User {
    pub fn new(name: &str) -> Self {
        Self { name: name.to_string() }
    }
}
```""",
        good="""```rust
impl User {
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into() }
    }
}
```""",
        when="Use when the constructed type stores owned data and callers may already have either borrowed or owned inputs.",
        when_not="Do not use `impl Into<String>` when the function only borrows temporarily; prefer `&str` or `AsRef<str>` for borrowed APIs.",
        verification="Add constructor tests for borrowed and owned inputs, check public API docs, and ensure the owned allocation happens only at the ownership boundary.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Rust API Guidelines: https://rust-lang.github.io/api-guidelines/"],
        related_rules=["api-impl-into", "own-borrow-over-clone", "anti-string-for-str"],
    ),
    Rule(
        rule_id="iter-collect-result-boundary",
        severity="medium",
        trigger="Iterator pipelines that transform fallible operations, parse many inputs, or convert many rows/items into domain values.",
        bad="""```rust
let users: Vec<User> = rows
    .into_iter()
    .filter_map(|row| User::try_from(row).ok())
    .collect();
```""",
        good="""```rust
let users: Result<Vec<User>, UserError> = rows
    .into_iter()
    .map(User::try_from)
    .collect();
```""",
        when="Use when failures must be preserved and the caller should see the first conversion error instead of silent item loss.",
        when_not="Do not use this when lossy filtering is the documented business rule; name that behavior explicitly.",
        verification="Test success, first-error propagation, empty input, and input containing multiple invalid rows.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Rust Iterator docs: https://doc.rust-lang.org/std/iter/trait.Iterator.html"],
        related_rules=["err-question-mark", "conv-tryfrom-fallible", "type-result-fallible"],
    ),
    Rule(
        rule_id="type-enum-over-boolean-parameter",
        severity="medium",
        trigger="Public functions or constructors with boolean parameters whose meaning is not obvious at the call site.",
        bad="""```rust
client.sync(true, false);
```""",
        good="""```rust
client.sync(SyncMode::Force, ConflictPolicy::KeepRemote);
```""",
        when="Use when each boolean represents a named mode, policy, direction, or state that affects behavior.",
        when_not="Do not replace clear predicate setters or local booleans when names already communicate the behavior.",
        verification="Check call sites for readability, add exhaustive tests for enum variants, and document default policies.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Rust API Guidelines: https://rust-lang.github.io/api-guidelines/"],
        related_rules=["type-enum-states", "pat-exhaustive-enum", "api-non-exhaustive"],
    ),
    Rule(
        rule_id="readability-early-return-control-flow",
        severity="medium",
        trigger="Deeply nested validation, parsing, request handling, or error handling where the happy path is obscured.",
        bad="""```rust
fn handle(req: Request) -> Result<Response, Error> {
    if req.is_valid() {
        if let Some(user) = req.user {
            if user.active {
                return process(user);
            }
        }
    }
    Err(Error::Invalid)
}
```""",
        good="""```rust
fn handle(req: Request) -> Result<Response, Error> {
    ensure!(req.is_valid(), Error::Invalid);
    let Some(user) = req.user else { return Err(Error::Invalid); };
    ensure!(user.active, Error::Invalid);
    process(user)
}
```""",
        when="Use when early returns, `let else`, or small extraction makes failure handling explicit and the main path easier to audit.",
        when_not="Do not split compact logic into many tiny functions if it hides invariants or makes ownership harder to follow.",
        verification="Run tests for every exit path and review whether error context is preserved after flattening.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Rust let-else: https://doc.rust-lang.org/rust-by-example/flow_control/let_else.html"],
        related_rules=["pat-let-else", "err-context-chain", "anti-over-abstraction"],
    ),
    Rule(
        rule_id="const-named-domain-values",
        severity="medium",
        trigger="Magic numbers, protocol constants, timeout values, retry counts, port numbers, byte offsets, or capacity limits.",
        bad="""```rust
if packet.len() < 42 {
    return Err(Error::ShortFrame);
}
let timeout = Duration::from_millis(250);
```""",
        good="""```rust
const ETHERNET_IPV4_MIN_FRAME: usize = 42;
const ORDER_ACK_TIMEOUT: Duration = Duration::from_millis(250);

if packet.len() < ETHERNET_IPV4_MIN_FRAME {
    return Err(Error::ShortFrame);
}
```""",
        when="Use when a literal encodes a domain rule, protocol boundary, capacity, or SLA that reviewers must recognize.",
        when_not="Do not name obvious tiny literals in local arithmetic when the name adds no domain information.",
        verification="Check protocol fixtures, timeout tests, and docs to ensure named constants match the external contract.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Rust const items: https://doc.rust-lang.org/reference/items/constant-items.html"],
        related_rules=["const-vs-static", "const-block", "mem-assert-type-size"],
    ),
    Rule(
        rule_id="qa-local-quality-gate",
        severity="high",
        trigger="Before committing Rust changes, opening PRs, publishing crates, or handing work back to a user.",
        bad="""```bash
cargo build
git commit -m change
```""",
        good="""```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets --all-features
```""",
        when="Use for ordinary Rust code changes before claiming the work is ready.",
        when_not="Do not blindly use `--all-features` when features are mutually exclusive; test the documented feature matrix instead.",
        verification="Run the gate locally or in CI and record any skipped command with the exact blocker.",
        sources=[MCPMARKET_SOURCE, THRASHR_SOURCE, "Cargo Book: https://doc.rust-lang.org/cargo/"],
        related_rules=["lint-rustfmt-check", "lint-deny-correctness", "test-integration-dir"],
    ),
]


def render_rule(rule: Rule) -> str:
    def list_block(values: list[str]) -> str:
        return "\n".join(f"- {value}" for value in values)

    return ascii_clean(f"""# {rule.rule_id}

## id
{rule.rule_id}

## severity
{rule.severity}

## trigger
{rule.trigger}

## bad
{rule.bad}

## good
{rule.good}

## when
{rule.when}

## when_not
{rule.when_not}

## verification
{rule.verification}

## sources
{list_block(rule.sources)}

## related_rules
{list_block(rule.related_rules)}
""")


def import_rules(source: Path, destination: Path) -> int:
    if not source.exists():
        raise FileNotFoundError(f"missing leonardomso rules directory: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    for old in destination.glob("*.md"):
        old.unlink()

    count = 0
    for path in sorted(source.glob("*.md")):
        rule = imported_rule(path)
        (destination / f"{rule.rule_id}.md").write_text(render_rule(rule), encoding="utf-8")
        count += 1

    for rule in ADVANCED_RULES + MARKET_REVIEW_RULES:
        (destination / f"{rule.rule_id}.md").write_text(render_rule(rule), encoding="utf-8")
        count += 1

    readme = """# Rust Expert Rulebook

This directory contains expert Rust rule cards consumed by skills and MCP tools.
The imported cards are normalized from `leonardomso/rust-skills` under its MIT license.
The plugin-specific cards cover HFT, SBE, eBPF, PyO3, Wasm, SIMD, NUMA, algorithms, and I/O.
"""
    (destination / "README.md").write_text(readme, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Rust expert rules.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--destination", type=Path, default=RULES_DIR)
    args = parser.parse_args()
    count = import_rules(args.source, args.destination)
    print(f"imported {count} rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
