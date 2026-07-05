# doc-panics-section

## id
doc-panics-section

## severity
medium

## trigger
Include `# Panics` section for functions that can panic. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Returns the element at the given index.
pub fn get(index: usize) -> &T {
    &self.data[index]  // Panics if out of bounds - not documented!
}

/// Divides two numbers.
pub fn divide(a: i32, b: i32) -> i32 {
    a / b  // Panics on division by zero - not documented!
}
```

## good
```rust
/// Returns the element at the given index.
///
/// # Panics
///
/// Panics if `index` is out of bounds (i.e., `index >= self.len()`).
///
/// # Examples
///
/// ```
/// let v = vec![1, 2, 3];
/// assert_eq!(v.get(1), &2);
/// ```
pub fn get(&self, index: usize) -> &T {
    &self.data[index]
}

/// Divides two numbers.
///
/// # Panics
///
/// Panics if `divisor` is zero.
///
/// For a non-panicking version, use [`checked_divide`].
pub fn divide(dividend: i32, divisor: i32) -> i32 {
    dividend / divisor
}

/// Divides two numbers, returning `None` if the divisor is zero.
pub fn checked_divide(dividend: i32, divisor: i32) -> Option<i32> {
    if divisor == 0 {
        None
    } else {
        Some(dividend / divisor)
    }
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
- doc-errors-section
- doc-safety-section
- err-result-over-panic
