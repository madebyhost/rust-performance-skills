# name-no-get-prefix

## id
name-no-get-prefix

## severity
medium

## trigger
Omit get_ prefix for simple getters. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    fn get_name(&self) -> &str {      // Verbose
        &self.name
    }

    fn get_age(&self) -> u32 {         // Verbose
        self.age
    }

    fn get_is_adult(&self) -> bool {   // Doubly verbose
        self.age >= 18
    }
}

let name = user.get_name();
let age = user.get_age();
```

## good
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    fn name(&self) -> &str {           // Clean
        &self.name
    }

    fn age(&self) -> u32 {             // Clean
        self.age
    }

    fn is_adult(&self) -> bool {       // Boolean uses is_ prefix
        self.age >= 18
    }
}

let name = user.name();
let age = user.age();
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
- api-builder-pattern
- name-is-has-bool
