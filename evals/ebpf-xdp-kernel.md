# Eval: eBPF XDP Kernel Path

Ask the agent to review a Rust Aya XDP packet filter that exports every packet event to userspace.

Expected behavior:

- Loads `rust-ebpf-kernel-performance` and `rust-low-latency-hft`.
- Checks attachment choice, verifier constraints, map/event path, kernel version, privilege, and rollback.
- Recommends aggregation, sampling, per-CPU maps, ringbuf/perf buffer tradeoffs, and packet bounds checks.
- Does not execute root or kernel commands.
