# macro-fragment-specifiers

## id
macro-fragment-specifiers

## severity
medium

## trigger
Capture with precise fragment specifiers, not raw `:tt`, where you can. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// Slurping everything as :tt, then trying to use $e as if it were an expression.
macro_rules! debug_val {
    ($($t:tt)*) => {
        println!("{} = {:?}", stringify!($($t)*), $($t)*);
        //                                          ^^^^^^^^ re-expanding :tt soup
    };
}

fn main() {
    debug_val!(1 + 2);      // works by accident
    debug_val!(let x = 1);  // accepted by the macro; blows up at expansion
}
```

## good
```rust
macro_rules! debug_val {
    // :expr captures a single expression; the follow-set allows `=>` and `,` after it.
    ($e:expr) => {
        println!("{} = {:?}", stringify!($e), $e);
    };
}

fn main() {
    debug_val!(1 + 2);
    // debug_val!(let x = 1); // now correctly rejected at the macro call site
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not write a macro when a function, trait, or const generic expresses the same idea clearly.

## verification
Add compile-pass and compile-fail tests covering exported macro paths and helper visibility.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- macro-prefer-functions
- macro-rules-hygiene
