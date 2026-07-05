# io-uring-backpressure

## id
io-uring-backpressure

## severity
high

## trigger
io_uring, mmap, direct I/O, queue-depth tuning, or disk/network I/O pipelines in Rust.

## bad
```rust
for request in requests {
    ring.submit(request)?;
}
```

## good
```rust
while in_flight < max_depth {
    submit_next(&mut ring)?;
    in_flight += 1;
}
reap_completions(&mut ring, &mut in_flight)?;
```

## when
Use when kernel queue depth, completion batching, or page-cache behavior is part of the performance contract.

## when_not
Do not use io_uring when portability, simple blocking I/O, or async runtime file APIs already meet the target.

## verification
Measure queue depth, completion latency, syscalls, page faults, fallback path, and cancellation/shutdown behavior.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- io-uring crate: https://docs.rs/io-uring/

## related_rules
- async-bounded-channel
- mem-reuse-collections
- numa-affinity-evidence
