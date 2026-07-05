# own-clone-explicit

## id
own-clone-explicit

## severity
critical

## trigger
Use explicit `Clone` for types where copying has meaningful cost. Trigger when working on ownership and borrowing and the code shows `own`-class risk.

## bad
```rust
// Hiding expensive operations
fn process_data(data: Vec<u32>) -> Vec<u32> {
    let backup = data; // Moved, not copied - but unclear at call site
    transform(backup)
}

let my_data = vec![1, 2, 3, 4, 5];
let result = process_data(my_data);
// my_data is moved - surprise if you expected it to still exist
```

## good
```rust
fn process_data(data: Vec<u32>) -> Vec<u32> {
    let backup = data;
    transform(backup)
}

let my_data = vec![1, 2, 3, 4, 5];
let result = process_data(my_data.clone()); // Explicit: "I know this allocates"
// my_data still available

// Or better - take reference if you don't need ownership
fn process_data_ref(data: &[u32]) -> Vec<u32> {
    transform(data)
}
let result = process_data_ref(&my_data); // No clone needed
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
- mem-clone-from
- own-copy-small
- own-cow-conditional
