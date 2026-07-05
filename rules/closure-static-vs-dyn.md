# closure-static-vs-dyn

## id
closure-static-vs-dyn

## severity
medium

## trigger
Accept `impl Fn` (generic) for hot callbacks; use `&dyn Fn`/`Box<dyn Fn>` to cut code size or to store them. Trigger when working on closures and callbacks and the code shows `closure`-class risk.

## bad
```rust
// Storing closures generically in a struct is impossible - the struct
// would need a type parameter per handler, making it unusable.
struct BadRegistry<F: Fn(&str)> {
    // Can only hold ONE concrete closure type - defeats the purpose.
    handler: F,
}

// Equally, using Box<dyn Fn> on a hot, single-call-site inner loop
// pays a vtable cost for no benefit.
fn transform_slow(xs: &[i32], f: &dyn Fn(i32) -> i32) -> Vec<i32> {
    xs.iter().map(|&x| f(x)).collect()
}
```

## good
```rust
// Generic / static dispatch: preferred for hot paths - inlinable, zero allocation.
fn transform<F: Fn(i32) -> i32>(xs: &[i32], f: F) -> Vec<i32> {
    xs.iter().map(|&x| f(x)).collect()
}

// Dynamic dispatch: required when storing heterogeneous closures.
struct Registry {
    handlers: Vec<Box<dyn Fn(&str)>>,
}

impl Registry {
    fn new() -> Self {
        Self { handlers: Vec::new() }
    }

    fn register(&mut self, handler: impl Fn(&str) + 'static) {
        self.handlers.push(Box::new(handler));
    }

    fn dispatch(&self, event: &str) {
        for handler in &self.handlers {
            handler(event);
        }
    }
}

fn demo() {
    // Static dispatch - the compiler may inline the closure entirely.
    let doubled = transform(&[1, 2, 3], |x| x * 2);
    assert_eq!(doubled, vec![2, 4, 6]);

    // Dynamic dispatch - one compiled copy, heterogeneous handlers.
    let mut reg = Registry::new();
    reg.register(|e| println!("logger: {e}"));
    reg.register(|e| println!("metrics: {e}"));
    reg.dispatch("user_signup");
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
- anti-type-erasure
- closure-fn-trait-bounds
- type-generic-bounds
