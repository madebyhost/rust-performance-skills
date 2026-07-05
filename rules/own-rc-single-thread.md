# own-rc-single-thread

## id
own-rc-single-thread

## severity
critical

## trigger
Use `Rc<T>` for shared ownership in single-threaded contexts. Trigger when working on ownership and borrowing and the code shows `own`-class risk.

## bad
```rust
use std::sync::Arc;

// Single-threaded application using Arc unnecessarily
fn build_tree() -> Arc<Node> {
    let root = Arc::new(Node::new("root"));
    let child1 = Arc::new(Node::new("child1"));
    let child2 = Arc::new(Node::new("child2"));

    // All in same thread, but paying atomic overhead
    root.add_child(child1.clone());
    root.add_child(child2.clone());
    root
}
```

Atomic operations have measurable overhead even without contention.

## good
```rust
use std::rc::Rc;

// Single-threaded: use Rc for zero atomic overhead
fn build_tree() -> Rc<Node> {
    let root = Rc::new(Node::new("root"));
    let child1 = Rc::new(Node::new("child1"));
    let child2 = Rc::new(Node::new("child2"));

    root.add_child(child1.clone());
    root.add_child(child2.clone());
    root
}

// Compiler enforces single-thread: Rc is !Send + !Sync
// Attempting to send across threads = compile error
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
- mem-drop-order
- own-arc-shared
- own-refcell-interior
