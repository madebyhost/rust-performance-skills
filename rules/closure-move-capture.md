# closure-move-capture

## id
closure-move-capture

## severity
medium

## trigger
Use `move` for closures that outlive the current scope; clone before `move` to keep the original. Trigger when working on closures and callbacks and the code shows `closure`-class risk.

## bad
```rust
fn make_greeter_bad(name: String) -> impl Fn() {
    // `name` is borrowed, but the closure outlives the function frame -
    // the compiler rejects this with a lifetime error.
    // || println!("hello, {name}")  // error: `name` does not live long enough
    move || println!("hello, {name}") // must be move - shown here to illustrate the fix
}

fn spawn_bad() {
    let data = vec![1, 2, 3];
    // Borrowing `data` across a thread boundary is rejected:
    // std::thread::spawn(|| println!("{data:?}")); // error: borrowed value does not live long enough
    let _ = data; // suppress unused warning
}
```

## good
```rust
fn process(data: &[i32]) -> i32 {
    data.iter().sum()
}

// Return a closure that owns its capture via `move`.
fn make_greeter(name: String) -> impl Fn() {
    move || println!("hello, {name}")
}

// Clone before `move` when you need the value in both places.
fn spawn_and_keep(data: Vec<i32>) -> std::thread::JoinHandle<i32> {
    let data_for_thread = data.clone(); // clone goes into the closure
    let handle = std::thread::spawn(move || process(&data_for_thread));
    // `data` is still available here
    println!("original still owned: {data:?}");
    handle
}

fn demo() {
    let greet = make_greeter(String::from("world"));
    greet(); // prints: hello, world

    let nums = vec![10, 20, 30];
    let handle = spawn_and_keep(nums);
    let sum = handle.join().unwrap();
    assert_eq!(sum, 60);
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
- async-clone-before-await
- closure-disjoint-capture
- own-move-large
