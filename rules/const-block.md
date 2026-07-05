# const-block

## id
const-block

## severity
medium

## trigger
Use inline `const { }` blocks for compile-time evaluation and assertions. Trigger when working on compile-time evaluation and the code shows `const`-class risk.

## bad
```rust
const SIZE: usize = 64;

fn process(buf: &[u8]) {
    // runtime panic - error surface is deferred until execution
    assert!(SIZE.is_power_of_two(), "SIZE must be a power of two");
    assert!(buf.len() <= SIZE);
}

// repeated magic number - easy to get out of sync
fn header() -> [u8; 4] {
    [0u8; 4]
}

// initializing array of non-Copy type requires unsafe or a workaround without const blocks
// std::array::from_fn is fine, but const blocks make the intent clearer for const values
```

## good
```rust
const SIZE: usize = 64;

fn process(buf: &[u8]) {
    // compile-time assertion - build fails immediately if SIZE changes to a bad value
    const { assert!(SIZE.is_power_of_two(), "SIZE must be a power of two") };

    // runtime assertion for dynamic data still makes sense here
    assert!(buf.len() <= SIZE);
}

// inline const block used as a value - evaluated once, inlined at each use
fn magic_header() -> u32 {
    const { 0xDEAD_BEEFu32.swap_bytes() }
}

// compile-time bounds check on a type-level relationship
struct Packet<const HDR: usize, const BODY: usize>;

impl<const HDR: usize, const BODY: usize> Packet<HDR, BODY> {
    fn new() -> Self {
        // fails at compile time if the relationship is violated, not at runtime
        const { assert!(HDR + BODY <= 1500, "packet exceeds ethernet MTU") };
        Packet
    }
}

// array of non-Copy type using a const block per element
// (each element is its own const expression - legal since 1.79)
fn make_table() -> [u64; 4] {
    [
        const { u64::MAX / 1 },
        const { u64::MAX / 2 },
        const { u64::MAX / 3 },
        const { u64::MAX / 4 },
    ]
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- const-fn
- mem-assert-type-size
