# opt-inline-small

## id
opt-inline-small

## severity
high

## trigger
Use `#[inline]` for small hot functions. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```rust
// Small hot function without inline hint
// May not be inlined across crate boundaries
fn is_ascii_digit(b: u8) -> bool {
    b >= b'0' && b <= b'9'
}

// Called millions of times
for byte in data {
    if is_ascii_digit(*byte) {  // Function call overhead
        count += 1;
    }
}
```

## good
```rust
#[inline]
fn is_ascii_digit(b: u8) -> bool {
    b >= b'0' && b <= b'9'
}

// Now the compiler will inline this
for byte in data {
    if is_ascii_digit(*byte) {  // Inlined, no call overhead
        count += 1;
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply compiler hints globally or speculatively; keep them for measured hot paths and deployment-specific profiles.

## verification
Inspect release profile, generated code when useful, and benchmark hot paths before keeping the change.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- opt-cold-unlikely
- opt-inline-always-rare
- opt-inline-never-cold
- opt-lto-release
