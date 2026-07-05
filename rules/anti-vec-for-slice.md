# anti-vec-for-slice

## id
anti-vec-for-slice

## severity
reference

## trigger
Don't accept &Vec<T> when &[T] works. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Forces callers to have a Vec
fn sum(numbers: &Vec<i32>) -> i32 {
    numbers.iter().sum()
}

// Caller must allocate
let arr = [1, 2, 3, 4, 5];
sum(&arr.to_vec());  // Unnecessary allocation

// Slice won't work
let slice: &[i32] = &[1, 2, 3];
// sum(slice);  // Error: expected &Vec<i32>
```

## good
```rust
// Accept slice - works with Vec, arrays, slices
fn sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}

// All these work
sum(&[1, 2, 3, 4, 5]);        // Array
sum(&vec![1, 2, 3]);          // Vec
sum(&numbers[1..3]);          // Slice of slice
sum(numbers.as_slice());      // Explicit slice
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
- anti-string-for-str
- api-impl-asref
- own-slice-over-vec
