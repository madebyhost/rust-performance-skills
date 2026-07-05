# closure-impl-fn-return

## id
closure-impl-fn-return

## severity
medium

## trigger
Return closures as `impl Fn`/`FnMut`/`FnOnce`, not `Box<dyn Fn>`. Trigger when working on closures and callbacks and the code shows `closure`-class risk.

## bad
```rust
// Allocates on the heap for no benefit - single concrete closure type.
fn adder_bad(n: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x + n)
}

fn multiplier_bad(n: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x * n)
}
```

## good
```rust
// Zero allocation, statically dispatched.
fn adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn multiplier(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x * n
}

fn apply(f: impl Fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

fn demo() {
    let add5 = adder(5);
    let mul3 = multiplier(3);

    assert_eq!(apply(add5, 10), 15);
    assert_eq!(apply(mul3, 10), 30);
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
- closure-static-vs-dyn
