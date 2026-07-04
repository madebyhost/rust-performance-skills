# Rust Performance Skills V5 Kernel Codecs Math Design

## Goal

Extend `rust-performance-skills` so it can guide advanced Rust performance work in three additional domains:

- kernel-aware optimization with eBPF;
- low-latency binary encoding with SBE and related fixed-layout codecs;
- high-performance math, graph, simulation, and stochastic algorithms.

The project should continue to be a skill-first Codex plugin with an offline, deterministic MCP surface.

## Approved Scope

Add three specialist skills:

1. `rust-ebpf-kernel-performance`
2. `rust-sbe-binary-codecs`
3. `rust-math-algorithms-performance`

Update:

- `rust-performance-engineering` router;
- `rust-low-latency-hft` references where binary codecs and kernel paths matter;
- `rust-review-auditor` routing;
- `scripts/rust_project_audit.py`;
- `mcp/rust_performance_mcp.py`;
- tests, docs, evals, and source map.

## Skill: Rust eBPF Kernel Performance

This skill should trigger for Rust eBPF, kernel-path observability, XDP, tc, kprobes, uprobes, tracepoints, perf/ring buffers, BPF maps, Aya, libbpf-rs, BTF, CO-RE, packet filtering, and kernel/user boundary optimization.

It must help agents:

- decide when eBPF is justified versus normal userspace tracing or networking;
- choose XDP, tc, tracepoint, kprobe, uprobe, or userspace-only instrumentation;
- reason about verifier constraints, map design, stack limits, no-heap/no-std constraints, bounded loops, tail calls, and kernel/user copy cost;
- design low-overhead event paths with ring buffers, perf buffers, per-CPU maps, aggregation, and sampling;
- keep safety boundaries explicit when reading kernel memory or packet data;
- avoid suggesting privileged operations unless the user explicitly asks to run them.

The skill must not execute or recommend automatic root/kernel commands. It should output commands only as optional verification examples with safety context.

## Skill: Rust SBE Binary Codecs

This skill should trigger for SBE, Simple Binary Encoding, binary market-data codecs, fixed-layout schemas, flyweight codecs, zero-copy decode, endian handling, alignment, versioning, schema evolution, wire compatibility, and HFT/order-flow serialization.

It must help agents:

- design schema layouts that minimize copies, branches, padding surprises, and per-message allocation;
- choose fixed-width fields, repeating groups, optional fields, presence maps, and versioning patterns deliberately;
- separate wire layout from domain objects so hot paths can decode borrowed views;
- reason about little/big endian cost, alignment, bounds checks, cursor movement, and batch decode;
- validate compatibility using golden frames, fuzzing, round trips, and schema-diff checks;
- avoid claiming zero-copy when conversion or allocation happens at the boundary.

## Skill: Rust Math Algorithms Performance

This skill should trigger for graph algorithms, shortest paths, search, Markov chains, Monte Carlo, Poisson and other probability distributions, simulation, numerical kernels, SIMD, ndarray, Rayon, petgraph, statrs, rand, rand_distr, sparse layouts, and cache-aware math.

It must help agents:

- choose data structures by access pattern: CSR/CSC, adjacency arrays, bitsets, heaps, buckets, grid indexes, SoA, dense arrays, and compact IDs;
- implement BFS, DFS, Dijkstra, A*, dynamic programming, Markov chains, Monte Carlo, and Poisson-related workflows with measurable performance;
- reason about allocation-free inner loops, preallocated work queues, deterministic RNG streams, parallel chunking, cache locality, and numerical stability;
- identify when petgraph, ndarray, Rayon, statrs, rand, rand_distr, or a custom layout is appropriate;
- avoid parallelism when overhead, contention, false sharing, or nondeterminism outweighs gains.

## MCP Extensions

Extend the offline MCP server with deterministic tools:

- `detect_performance_domains`: inspect audit output or a project path and return detected domains such as `ebpf`, `sbe`, `math`, `graph`, `simulation`, `hft`, `pyo3`, `wasm`, `unsafe`.
- `rust_algorithm_checklist`: return a checklist for BFS, DFS, Dijkstra, A*, Markov, Monte Carlo, Poisson, ndarray, SIMD, and Rayon concerns.
- `binary_encoding_review_checklist`: return a checklist for SBE/fixed binary codecs, schema compatibility, zero-copy decode, endian/alignment, and golden-frame tests.

The existing `rust_review_checklist` should include eBPF/SBE/math checks when relevant signals are present.

## Audit Extensions

Extend `scripts/rust_project_audit.py` to detect:

- eBPF dependencies and files: `aya`, `aya-bpf`, `libbpf-rs`, `libbpf-cargo`, `redbpf`, `xdp`, `kprobe`, `uprobe`, `tracepoint`, `BPF_MAP`, `bpf`;
- binary codec/SBE signals: `sbe`, `simple-binary-encoding`, `fix-simple-binary-encoding`, `messageHeader`, `actingVersion`, `blockLength`, `schemaId`, `templateId`, binary cursor encode/decode vocabulary;
- math/algorithm signals: `petgraph`, `ndarray`, `rayon`, `statrs`, `rand`, `rand_distr`, `nalgebra`, `sprs`, `BFS`, `DFS`, `Dijkstra`, `A*`, `Markov`, `Monte Carlo`, `Poisson`.

The audit result should add findings and recommendations for each domain without running project code.

## Docs And Evals

Add:

- source map entries for Linux BPF docs, Aya, libbpf-rs, FIX SBE, Real Logic SBE, petgraph, ndarray, Rayon, rand, rand_distr, statrs, and Rust std SIMD;
- evals for eBPF/XDP, SBE market-data codec, and math/graph/simulation performance reviews;
- README skill list updates.

## Safety Rules

- Do not add hooks.
- Do not add a remote MCP runtime or `npx @latest`.
- Do not execute kernel/eBPF commands in tests or install scripts.
- Do not require root privileges.
- Do not generate or load eBPF programs automatically.
- Keep MCP offline and deterministic.
- Keep private project metadata out of commits, docs, generated files, and marketplace metadata.

## Testing

Add tests for:

- the three new skills and their `agents/openai.yaml` files;
- router links to the new skills;
- reference links exist;
- audit detection for eBPF, SBE, and math project samples;
- MCP direct calls for new tools;
- source map contains the new primary-source tokens;
- eval files exist;
- distribution validator includes the new skills, evals, MCP tools, and source tokens.

## Success Criteria

- The plugin has specialist guidance for eBPF, SBE, and high-performance math algorithms.
- The MCP can detect and checklist these domains without executing untrusted code.
- Existing plugin marketplace install remains functional.
- All local tests and validators pass.
- GitHub Actions passes after push.
- GitHub commits show `Mehdi AISSANI <contact@mehdiaissani.com>` as author and committer.
