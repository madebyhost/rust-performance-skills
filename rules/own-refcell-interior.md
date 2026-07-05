# own-refcell-interior

## id
own-refcell-interior

## severity
critical

## trigger
Use `RefCell<T>` for interior mutability in single-threaded code. Trigger when working on ownership and borrowing and the code shows `own`-class risk.

## bad
```rust
struct Cache {
    // Requires &mut self to update, breaking shared reference patterns
    data: HashMap<String, String>,
}

impl Cache {
    fn get_or_compute(&mut self, key: &str) -> &str {
        // Caller needs &mut Cache, can't share cache reference
        if !self.data.contains_key(key) {
            self.data.insert(key.to_string(), expensive_compute(key));
        }
        &self.data[key]
    }
}
```

This forces exclusive access even for logically shared operations.

## good
```rust
use std::cell::RefCell;
use std::collections::HashMap;

struct Cache {
    data: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get_or_compute(&self, key: &str) -> String {
        // Can mutate through &self
        let mut data = self.data.borrow_mut();
        if !data.contains_key(key) {
            data.insert(key.to_string(), expensive_compute(key));
        }
        data[key].clone()
    }
}

// Multiple references can coexist
let cache = Cache::new();
let ref1 = &cache;
let ref2 = &cache;
ref1.get_or_compute("key1");
ref2.get_or_compute("key2");
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
- conc-thread-local
- own-mutex-interior
- own-rc-single-thread
