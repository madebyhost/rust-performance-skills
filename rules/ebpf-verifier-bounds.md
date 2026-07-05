# ebpf-verifier-bounds

## id
ebpf-verifier-bounds

## severity
critical

## trigger
Rust eBPF/XDP/tc programs that parse packet bytes, use maps, or interact with verifier-sensitive pointer arithmetic.

## bad
```rust
let eth = unsafe { *(ctx.data() as *const EthHdr) };
let proto = unsafe { *ctx.data().add(14) };
```

## good
```rust
let start = ctx.data();
let end = ctx.data_end();
let eth = ptr_at::<EthHdr>(start, end, 0)?;
let proto = checked_byte(start, end, EthHdr::LEN)?;
```

## when
Use for kernel-side packet parsers and probe programs where every byte access must prove bounds to the verifier.

## when_not
Do not hide verifier-critical bounds behind abstractions the verifier cannot inline or reason about.

## verification
Measure verifier acceptance, instruction count, map lookup cost, drop/pass counters, and userspace/kernel benchmark separation.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- docs.ebpf.io: https://docs.ebpf.io/
- Linux BPF docs: https://docs.kernel.org/bpf/

## related_rules
- unsafe-minimize-scope
- unsafe-safety-comment
- num-cast-try-from
