# hft-disruptor-ring-buffer

## id
hft-disruptor-ring-buffer

## severity
critical

## trigger
Single-writer or staged low-latency pipelines where queues, locks, or heap churn dominate handoff cost.

## bad
```rust
let (tx, rx) = tokio::sync::mpsc::unbounded_channel();
tx.send(event.clone()).unwrap();
```

## good
```rust
let slot = ring.claim()?;
slot.write(event);
ring.publish(slot.sequence());
```

## when
Use when the topology, producers, consumers, and backpressure policy are known and benchmarked.

## when_not
Do not add disruptor-style architecture when normal bounded channels satisfy the latency budget.

## verification
Measure handoff latency, false sharing, sequence contention, backpressure behavior, and shutdown recovery.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- LMAX Disruptor: https://lmax-exchange.github.io/disruptor/

## related_rules
- conc-atomic-ordering
- mem-assert-type-size
- hft-udp-multicast-hotpath
