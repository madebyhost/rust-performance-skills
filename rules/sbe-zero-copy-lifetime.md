# sbe-zero-copy-lifetime

## id
sbe-zero-copy-lifetime

## severity
critical

## trigger
SBE, fixed-layout binary codecs, market-data frames, or borrowed decoders over network buffers.

## bad
```rust
struct Message {
    symbol: String,
}
fn decode(buf: &[u8]) -> Message {
    Message { symbol: String::from_utf8(buf[8..16].to_vec()).unwrap() }
}
```

## good
```rust
struct Message<'a> {
    symbol: &'a [u8],
}
fn decode<'a>(buf: &'a [u8]) -> Result<Message<'a>, DecodeError> {
    Ok(Message { symbol: checked_field(buf, 8, 8)? })
}
```

## when
Use when decoded fields can borrow from the frame and the frame lifetime is tied to processing.

## when_not
Do not return borrowed views beyond the frame owner or across async/task boundaries without ownership strategy.

## verification
Measure copies, fuzz truncated frames, and test schema ID, template ID, block length, acting version, endian, and bounds.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- Real Logic SBE: https://github.com/real-logic/simple-binary-encoding

## related_rules
- mem-zero-copy
- unsafe-maybeuninit
- type-repr-transparent
