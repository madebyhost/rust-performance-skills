# conc-thread-local

## id
conc-thread-local

## severity
high

## trigger
Prefer `thread_local!` with `Cell`/`RefCell` over `static mut`. Trigger when working on concurrency and synchronization and the code shows `conc`-class risk.

## bad
```rust
// Rust 2024: referencing static mut is a hard error (static_mut_refs lint)
static mut BUFFER: Vec<u8> = Vec::new();

fn append_to_buffer(data: &[u8]) {
    // UB if called from multiple threads; hard error in 2024 edition
    unsafe {
        BUFFER.extend_from_slice(data);
    }
}

fn flush_buffer() -> Vec<u8> {
    unsafe {
        std::mem::take(&mut BUFFER) // still requires unsafe
    }
}
```

## good
```rust
use std::cell::RefCell;

thread_local! {
    static BUFFER: RefCell<Vec<u8>> = RefCell::new(Vec::with_capacity(4096));
}

fn append_to_buffer(data: &[u8]) {
    BUFFER.with_borrow_mut(|buf| buf.extend_from_slice(data));
}

fn flush_buffer() -> Vec<u8> {
    BUFFER.with_borrow_mut(|buf| std::mem::take(buf))
}
```

For `Copy` types, `Cell` is simpler (no borrow overhead):

```rust
use std::cell::Cell;

thread_local! {
    static CALL_COUNT: Cell<u32> = Cell::new(0);
}

fn record_call() {
    CALL_COUNT.with(|c| c.set(c.get() + 1));
}

fn get_call_count() -> u32 {
    CALL_COUNT.with(|c| c.get())
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not add shared mutable state, atomics, or lock-free structures when ownership transfer or single-threaded design is simpler.

## verification
Use stress tests, loom where practical, and contention measurements for shared state.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- own-mutex-interior
- own-refcell-interior
