---
name: rust-ebpf-kernel-performance
description: "Use when designing, reviewing, or optimizing Rust eBPF/kernel-path work with Aya, libbpf-rs, XDP, tc, kprobes, uprobes, tracepoints, BPF maps, ring/perf buffers, AF_XDP, verifier limits, CO-RE/BTF, packet processing, tracing, observability, security, and kernel/user boundary performance."
---

# Rust eBPF Kernel Performance

Use this skill when performance work crosses into the kernel path. Load `references/ebpf-kernel-performance.md` for attachment, map, verifier, and event-path details.

## Workflow

1. Decide whether eBPF is justified: kernel packet path, low-overhead observability, tracing, security policy, or userspace/kernel boundary reduction.
2. Pick the attachment point deliberately: XDP, tc, tracepoint, kprobe, uprobe, LSM, cgroup, syscall, struct-ops, or userspace-only instrumentation.
3. Design maps and event paths before code: per-CPU maps, LRU maps, ringbuf, perf event array, user-ringbuf, cpumap, xskmap, sockmap, sockhash, and prog array.
4. Check verifier constraints: bounded loops, stack limits, helper availability, no heap, no blocking, pointer bounds, dynptr/kfunc support, and kernel version.
5. Keep privilege and rollout risks explicit. Do not run or suggest automatic root/kernel commands.

## Defaults

- Prefer userspace measurement first unless the bottleneck is demonstrably in kernel path or copy/event overhead.
- Prefer XDP only when early packet handling or drop/redirect latency justifies the operational cost.
- Prefer aggregation/sampling in eBPF over high-volume event export.
- Treat `bpf_trace_printk` as debug-only, not production observability.
- Separate BPF program safety from userspace controller safety.

## Output

Return the performance contract, attachment choice, map/event design, verifier risks, kernel/version assumptions, privilege requirements, rollback plan, and safe verification commands.
