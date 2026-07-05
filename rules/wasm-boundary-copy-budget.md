# wasm-boundary-copy-budget

## id
wasm-boundary-copy-budget

## severity
high

## trigger
Rust/Wasm modules exchanging strings, arrays, frames, images, or simulation buffers with JavaScript.

## bad
```rust
#[wasm_bindgen]
pub fn ticks() -> Vec<f64> {
    compute_ticks()
}
```

## good
```rust
#[wasm_bindgen]
pub fn ticks_ptr() -> *const f64 { BUFFER.with(|b| b.as_ptr()) }

#[wasm_bindgen]
pub fn ticks_len() -> usize { BUFFER.with(|b| b.len()) }
```

## when
Use when boundary copies dominate runtime or when large typed arrays cross JS/Wasm repeatedly.

## when_not
Do not expose raw pointers unless lifetime, mutation, and memory growth behavior are documented and tested.

## verification
Measure JS/Wasm call count, copied bytes, memory growth, wasm size, browser and Node tests, and fallback behavior.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- wasm-bindgen: https://rustwasm.github.io/docs/wasm-bindgen/

## related_rules
- mem-zero-copy
- type-repr-transparent
- api-must-use
