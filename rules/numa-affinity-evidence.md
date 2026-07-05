# numa-affinity-evidence

## id
numa-affinity-evidence

## severity
high

## trigger
CPU pinning, NUMA node placement, huge pages, isolated cores, or memory locality changes.

## bad
```rust
pin_thread_to_core(0);
allocate_all_buffers();
```

## good
```rust
pin_thread_to_core(feed_core);
allocate_after_pin(&mut local_pool);
warm_pages(&mut local_pool);
```

## when
Use when latency distribution or perf counters show cross-node memory, migrations, or page faults matter.

## when_not
Do not pin blindly on shared hosts, containers without stable topology, or workloads dominated by I/O waits.

## verification
Measure CPU migrations, remote memory accesses, page faults, huge-page hit rate, p99/p999 latency, and jitter.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- Linux NUMA docs: https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html

## related_rules
- mem-assert-type-size
- hft-disruptor-ring-buffer
- io-uring-backpressure
