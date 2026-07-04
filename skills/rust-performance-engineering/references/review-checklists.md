# Review Checklists

Use these checklists when reviewing Rust performance work.

## Performance PR Review

- Is the performance contract stated?
- Is the hot path identified?
- Are before/after measurements included or explicitly missing?
- Did allocations, copies, locks, syscalls, or task counts change?
- Are tail latency and throughput both considered where relevant?
- Are feature flags and release profile effects understood?

## Zero-Copy Review

- Does the source buffer outlive all borrowed views?
- Are malformed inputs rejected before borrowed access?
- Are clones/copies removed from a measured hot path?
- Are offsets used instead of self-referential structs where practical?
- Is ownership clear across async tasks and queues?

## Async Review

- Are channels bounded?
- Are blocking operations kept off async worker threads?
- Are locks held across `.await`?
- Is shutdown deterministic?
- Are queue depths and task counts observable?
- Is CPU work handled by the right execution model?

## Unsafe Review

- Is `unsafe` required by a measured bottleneck or FFI boundary?
- Is there a safe wrapper?
- Are invariants documented next to the `unsafe` block or API?
- Are aliasing, alignment, initialization, lifetimes, panic safety, and thread safety addressed?
- Is Miri, sanitizer, fuzzing, or focused testing possible?

## HFT / Ultra-Low-Latency Review

- Are warmup, p99/p99.9, jitter, and max latency reported?
- Are allocations absent or bounded after warmup?
- Are ring-buffer overflow and slow-consumer policies explicit?
- Are packet loss, sequence gaps, replay, and reconnect paths tested?
- Are CPU affinity, NUMA, and kernel/network assumptions deployment-realistic?
- Is persistence outside the decision hot path unless required?
