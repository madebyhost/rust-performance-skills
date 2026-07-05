# const-named-domain-values

## id
const-named-domain-values

## severity
medium

## trigger
Magic numbers, protocol constants, timeout values, retry counts, port numbers, byte offsets, or capacity limits.

## bad
```rust
if packet.len() < 42 {
    return Err(Error::ShortFrame);
}
let timeout = Duration::from_millis(250);
```

## good
```rust
const ETHERNET_IPV4_MIN_FRAME: usize = 42;
const ORDER_ACK_TIMEOUT: Duration = Duration::from_millis(250);

if packet.len() < ETHERNET_IPV4_MIN_FRAME {
    return Err(Error::ShortFrame);
}
```

## when
Use when a literal encodes a domain rule, protocol boundary, capacity, or SLA that reviewers must recognize.

## when_not
Do not name obvious tiny literals in local arithmetic when the name adds no domain information.

## verification
Check protocol fixtures, timeout tests, and docs to ensure named constants match the external contract.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Rust const items: https://doc.rust-lang.org/reference/items/constant-items.html

## related_rules
- const-vs-static
- const-block
- mem-assert-type-size
