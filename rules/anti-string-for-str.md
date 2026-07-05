# anti-string-for-str

## id
anti-string-for-str

## severity
reference

## trigger
Don't accept &String when &str works. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Forces callers to have a String
fn greet(name: &String) {
    println!("Hello, {}", name);
}

// Caller must allocate
greet(&"Alice".to_string());  // Unnecessary allocation
greet(&name);                 // Only works if name is String

// In struct
struct Config {
    name: String,
}

impl Config {
    fn set_name(&mut self, name: &String) {  // Too restrictive
        self.name = name.clone();
    }
}
```

## good
```rust
// Accept &str - works with String, &str, literals
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// All these work
greet("Alice");           // String literal
greet(&name);             // &String coerces to &str
greet(name.as_str());     // Explicit &str

// In struct
impl Config {
    fn set_name(&mut self, name: &str) {
        self.name = name.to_string();
    }

    // Or accept owned String if caller usually has one
    fn set_name_owned(&mut self, name: String) {
        self.name = name;
    }

    // Or be generic
    fn set_name_into(&mut self, name: impl Into<String>) {
        self.name = name.into();
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
- anti-vec-for-slice
- api-impl-asref
- own-slice-over-vec
