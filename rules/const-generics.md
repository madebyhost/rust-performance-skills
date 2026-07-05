# const-generics

## id
const-generics

## severity
medium

## trigger
Parameterize over values with const generics `<const N: usize>`. Trigger when working on compile-time evaluation and the code shows `const`-class risk.

## bad
```rust
// works only for one fixed size - must be copy-pasted per size
fn sum_4(arr: [i32; 4]) -> i32 {
    arr.iter().sum()
}

fn sum_8(arr: [i32; 8]) -> i32 {
    arr.iter().sum()
}

// carries runtime length - extra field, heap allocation, no compile-time bounds
struct Buffer {
    data: Vec<u8>,
    capacity: usize,
}
```

## good
```rust
// one generic function works for any array size; N is inferred from the argument
fn sum<const N: usize>(arr: [i32; N]) -> i32 {
    arr.iter().sum()
}

let total = sum([1, 2, 3, 4]);       // N = 4, inferred
let total8 = sum([0i32; 8]);         // N = 8, inferred

// stack-allocated buffer parameterized by capacity - no heap, no runtime length
struct Buffer<const N: usize> {
    data: [u8; N],
    len: usize,
}

impl<const N: usize> Buffer<N> {
    const fn new() -> Self {
        Self { data: [0u8; N], len: 0 }
    }

    fn push(&mut self, byte: u8) -> bool {
        if self.len < N {
            self.data[self.len] = byte;
            self.len += 1;
            true
        } else {
            false
        }
    }

    fn as_slice(&self) -> &[u8] {
        &self.data[..self.len]
    }
}

// capacity is part of the type - mismatches caught at compile time
let mut small: Buffer<8> = Buffer::new();
let mut large: Buffer<1024> = Buffer::new();
small.push(42);
large.push(99);

// const generic used as an array length computed from another const
const BLOCK: usize = 16;
fn xor_block<const N: usize>(a: [u8; N], b: [u8; N]) -> [u8; N] {
    let mut out = [0u8; N];
    for i in 0..N {
        out[i] = a[i] ^ b[i];
    }
    out
}
let result = xor_block([0u8; BLOCK], [0xFF; BLOCK]);
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
