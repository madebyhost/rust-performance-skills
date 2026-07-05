# anti-clone-excessive

## id
anti-clone-excessive

## severity
reference

## trigger
Don't clone when borrowing works. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Cloning to pass to a function that only reads
fn print_name(name: String) {  // Takes ownership
    println!("{}", name);
}
let name = "Alice".to_string();
print_name(name.clone());  // Unnecessary clone
print_name(name);          // Could have just done this

// Cloning in a loop
for item in items.clone() {  // Clones entire Vec
    process(&item);
}

// Cloning for comparison
if input.clone() == expected {  // Pointless clone
    // ...
}

// Cloning struct fields
fn get_name(&self) -> String {
    self.name.clone()  // Caller might not need ownership
}
```

## good
```rust
// Accept reference if only reading
fn print_name(name: &str) {
    println!("{}", name);
}
let name = "Alice".to_string();
print_name(&name);  // Borrow, no clone

// Iterate by reference
for item in &items {
    process(item);
}

// Compare by reference
if input == expected {
    // ...
}

// Return reference when possible
fn get_name(&self) -> &str {
    &self.name
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
- own-arc-shared
- own-borrow-over-clone
- own-cow-conditional
