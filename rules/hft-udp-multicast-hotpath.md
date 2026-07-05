# hft-udp-multicast-hotpath

## id
hft-udp-multicast-hotpath

## severity
critical

## trigger
UDP multicast market-data ingest, packet fanout, feed handlers, or replay paths with tail-latency constraints.

## bad
```rust
async fn on_packet(socket: UdpSocket) {
    let mut buf = vec![0_u8; 2048];
    loop {
        let n = socket.recv(&mut buf).await.unwrap();
        println!("packet {:?}", &buf[..n]);
        process(buf[..n].to_vec()).await;
    }
}
```

## good
```rust
fn on_packet(buf: &mut [u8], ring: &mut Ring<Frame>) -> Result<(), DropReason> {
    let frame = decode_borrowed(buf)?;
    ring.try_publish(frame).map_err(|_| DropReason::Backpressure)
}
```

## when
Use for feed handlers that must minimize copies, allocations, logging, scheduler hops, and unbounded queues.

## when_not
Do not force this shape for admin traffic, control planes, or low-rate feeds where clarity is the primary constraint.

## verification
Measure packet drops, p99/p999 latency, allocation count, syscall count, queue depth, and replay determinism.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- Linux networking documentation: https://docs.kernel.org/networking/

## related_rules
- mem-zero-copy
- async-bounded-channel
- perf-batch-processing
