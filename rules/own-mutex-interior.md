# own-mutex-interior

## id
own-mutex-interior

## severity
critical

## trigger
Use `Mutex<T>` for interior mutability across threads. Trigger when working on ownership and borrowing and the code shows `own`-class risk.

## bad
```rust
use std::cell::RefCell;
use std::sync::Arc;

// RefCell is !Sync - this won't compile
let shared = Arc::new(RefCell::new(vec![]));

// ERROR: RefCell cannot be shared between threads safely
std::thread::spawn({
    let shared = shared.clone();
    move || shared.borrow_mut().push(1)
});
```

## good
```rust
use std::sync::{Arc, Mutex};

let shared = Arc::new(Mutex::new(vec![]));

let handles: Vec<_> = (0..10).map(|i| {
    let shared = shared.clone();
    std::thread::spawn(move || {
        let mut data = shared.lock().unwrap();
        data.push(i);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("{:?}", shared.lock().unwrap()); // All values present
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
- async-no-lock-await
- conc-atomic-ordering
- own-refcell-interior
- own-rwlock-readers
