# trait-object-safety

## id
trait-object-safety

## severity
medium

## trigger
Keep a trait dyn-compatible (object-safe) when you need `dyn Trait`. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
trait Transformer {
    // Generic method - not dispatchable, makes the whole trait non-object-safe.
    fn transform<T: std::fmt::Debug>(&self, value: T) -> String;

    fn name(&self) -> &str;
}

struct Shout;
impl Transformer for Shout {
    fn transform<T: std::fmt::Debug>(&self, value: T) -> String {
        format!("{value:?}").to_uppercase()
    }
    fn name(&self) -> &str { "shout" }
}

// This fails to compile:
// error[E0038]: the trait `Transformer` cannot be made into an object
// fn apply(t: &dyn Transformer, x: i32) { ... }
```

## good
```rust
trait Transformer {
    // Core dispatchable method - always in the vtable.
    fn transform_str(&self, value: &str) -> String;

    fn name(&self) -> &str;

    // Generic convenience method gated with `where Self: Sized`.
    // Callers can use it via a concrete type; it is excluded from `dyn Transformer`.
    fn transform_debug<T: std::fmt::Debug>(&self, value: T) -> String
    where
        Self: Sized,
    {
        self.transform_str(&format!("{value:?}"))
    }
}

// ----- Implementations -----

struct Shout;
impl Transformer for Shout {
    fn transform_str(&self, value: &str) -> String { value.to_uppercase() }
    fn name(&self) -> &str { "shout" }
}

struct Whisper;
impl Transformer for Whisper {
    fn transform_str(&self, value: &str) -> String { value.to_lowercase() }
    fn name(&self) -> &str { "whisper" }
}

// ----- Object-safe usage -----

fn apply_all(transformers: &[Box<dyn Transformer>], input: &str) {
    for t in transformers {
        println!("[{}] {}", t.name(), t.transform_str(input));
    }
}

// ----- Generic (static) usage - can call the `where Self: Sized` method -----

fn apply_generic<T: Transformer>(t: &T, value: i32) -> String {
    t.transform_debug(value)  // available because T: Sized
}

fn demo() {
    let ts: Vec<Box<dyn Transformer>> = vec![
        Box::new(Shout),
        Box::new(Whisper),
    ];
    apply_all(&ts, "Hello World");

    // Static dispatch path can use the generic helper.
    let result = apply_generic(&Shout, 42);
    println!("{result}");
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
- api-sealed-trait
- trait-dyn-vs-generic
