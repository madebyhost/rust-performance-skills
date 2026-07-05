# eBPF Kernel Performance Reference

## When eBPF Fits

- Packet path: XDP for earliest packet handling, tc for traffic control after skb creation, socket/cgroup hooks for policy.
- Observability: tracepoints first for stability, kprobes/uprobes when no stable tracepoint exists.
- Security: LSM/cgroup/syscall hooks when policy requires kernel context.
- Performance: in-kernel aggregation, sampling, filtering, redirect, or avoiding high-volume userspace export.

## docs.ebpf.io Vocabulary To Consider

- Concepts: maps, verifier, functions, concurrency, pinning, tail calls, loops, timers, resource limits, AF_XDP, kfuncs, dynptrs, token, trampolines, USDT.
- Program families: network, tracing, cgroup, LSM, syscall, struct-ops, lightweight tunnel.
- Streaming maps: `BPF_MAP_TYPE_PERF_EVENT_ARRAY`, `BPF_MAP_TYPE_RINGBUF`, `BPF_MAP_TYPE_USER_RINGBUF`.
- Packet redirection maps: devmap, cpumap, xskmap, sockmap, sockhash.
- Flow control: prog array for tail calls, per-CPU maps for low-contention counters, LRU maps for bounded state.

## Rust Stack Choices

- Aya: Rust-first eBPF userspace and BPF-side workflows.
- libbpf-rs/libbpf-cargo: libbpf/CO-RE centered workflows.
- Keep generated bindings and kernel layout assumptions reviewed alongside code.

## Hot Path Rules

- Bound loops and stack use.
- Avoid per-event map churn where per-CPU aggregation or batching works.
- Use ringbuf/perf buffers for event export; choose based on ordering and kernel support.
- Minimize probe reads and copy volume; read only fields needed for decisions.
- Validate packet bounds before every header access.

## Review Checklist

- Attachment point matches latency and stability requirements.
- Map types match contention, cardinality, and lifetime.
- Verifier risks are documented before implementation.
- Kernel version, BTF/CO-RE availability, and helper support are stated.
- Rollback, feature flag, and safe deploy path exist.
- Tests do not require root or loading programs unless explicitly isolated.
