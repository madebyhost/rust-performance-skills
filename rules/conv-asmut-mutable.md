# conv-asmut-mutable

## id
conv-asmut-mutable

## severity
medium

## trigger
Accept `impl AsMut<T>` for flexible mutable borrowed inputs instead of concrete mutable references. Trigger when working on conversion boundaries and the code shows `conv`-class risk.

## bad
```rust
// Only accepts &mut Vec<u8>; arrays and slices are excluded
fn fill_zeros(buf: &mut Vec<u8>) {
    for b in buf.iter_mut() {
        *b = 0;
    }
}

fn main() {
    let mut data = vec![1u8, 2, 3];
    fill_zeros(&mut data);

    // Compile error - cannot pass &mut [u8; 3] or &mut [u8]
    // let mut arr = [1u8, 2, 3];
    // fill_zeros(&mut arr);
}
```

## good
```rust
// Accepts Vec<u8>, [u8; N], &mut [u8] - any type that lends &mut [u8]
fn fill_zeros(mut buf: impl AsMut<[u8]>) {
    for b in buf.as_mut().iter_mut() {
        *b = 0;
    }
}

fn verify(mut buf: impl AsMut<[u8]>) -> bool {
    buf.as_mut().iter().all(|&b| b == 0)
}

fn main() {
    let mut vec_buf = vec![1u8, 2, 3];
    fill_zeros(&mut vec_buf);
    assert!(verify(&mut vec_buf));

    let mut arr_buf = [1u8, 2, 3, 4];
    fill_zeros(&mut arr_buf);
    assert!(verify(&mut arr_buf));

    let mut slice_buf = [5u8, 6, 7];
    fill_zeros(slice_buf.as_mut());
    assert!(verify(slice_buf.as_mut()));
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
- api-impl-asref
- own-slice-over-vec
