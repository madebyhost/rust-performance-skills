# const-fn

## id
const-fn

## severity
medium

## trigger
Make functions `const fn` when they can run at compile time. Trigger when working on compile-time evaluation and the code shows `const`-class risk.

## bad
```rust
// not const - cannot use result as an array length or const initializer
fn header_len() -> usize {
    4
}

fn magic_mask() -> u32 {
    0xFF00_FF00
}

fn make_buf() -> [u8; 8] {
    // runtime call - compiler cannot inline the length into the type
    [0u8; header_len()]  // error: `header_len` is not a `const fn`
}
```

## good
```rust
const fn header_len() -> usize {
    4
}

const fn magic_mask() -> u32 {
    0xFF00_FF00
}

// usable as an array length - evaluated at compile time
let buf = [0u8; header_len()];

// usable in a const initializer
const MASK: u32 = magic_mask();

// usable in a static
static HEADER: [u8; header_len()] = [0u8; header_len()];

// const fn with logic - still fine on stable
const fn align_up(n: usize, align: usize) -> usize {
    (n + align - 1) & !(align - 1)
}

const ALIGNED: usize = align_up(13, 8); // 16, computed at compile time
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
- const-block
- const-generics
- opt-inline-small
