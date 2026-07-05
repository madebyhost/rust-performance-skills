# mem-box-large-variant

## id
mem-box-large-variant

## severity
critical

## trigger
Box large enum variants to reduce overall enum size. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
enum Message {
    Quit,                              // 0 bytes of data
    Move { x: i32, y: i32 },          // 8 bytes
    Text(String),                      // 24 bytes
    Image {
        data: [u8; 1024],             // 1024 bytes - forces entire enum to ~1032 bytes!
        width: u32,
        height: u32
    },
}

// Every Message is ~1032 bytes, even Quit and Move
let messages: Vec<Message> = vec![
    Message::Quit,  // Wastes ~1032 bytes
    Message::Quit,  // Wastes ~1032 bytes
    Message::Move { x: 0, y: 0 },  // Wastes ~1024 bytes
];
```

## good
```rust
struct ImageData {
    data: [u8; 1024],
    width: u32,
    height: u32,
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Text(String),
    Image(Box<ImageData>),  // Now just 8 bytes (pointer)
}

// Message is now ~32 bytes (String variant is largest)
let messages: Vec<Message> = vec![
    Message::Quit,  // Uses ~32 bytes
    Message::Quit,  // Uses ~32 bytes
    Message::Move { x: 0, y: 0 },  // Uses ~32 bytes
];
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when ownership is required for correctness, lifetime complexity would dominate the API, or measurement shows no meaningful allocation/copy cost.

## verification
Measure allocations, copies, cache misses, and benchmark deltas on representative inputs.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- lint-deny-correctness
- mem-smallvec
- own-move-large
