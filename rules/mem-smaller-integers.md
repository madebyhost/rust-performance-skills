# mem-smaller-integers

## id
mem-smaller-integers

## severity
critical

## trigger
Use appropriately-sized integers to reduce memory footprint. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
struct Pixel {
    r: u64,  // Color channels 0-255 = 8 bits needed
    g: u64,  // Using 64 bits = 8x waste
    b: u64,
    a: u64,
}
// Size: 32 bytes per pixel

struct HttpStatus {
    code: i32,      // HTTP codes 100-599 = 10 bits needed
    version: i32,   // HTTP 1.0, 1.1, 2, 3 = 2 bits needed
}
// Size: 8 bytes per status

struct GeoPoint {
    lat: f64,   // -90 to 90
    lon: f64,   // -180 to 180
}
// Often f32 precision is sufficient for display
```

## good
```rust
struct Pixel {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}
// Size: 4 bytes per pixel (8x smaller!)

struct HttpStatus {
    code: u16,      // 100-599 fits in u16
    version: u8,    // 1, 2, 3 fits in u8
}
// Size: 3 bytes (+ 1 padding = 4 bytes)

struct GeoPoint {
    lat: f32,   // ~7 decimal digits precision
    lon: f32,   // Sufficient for most geo applications
}
// Size: 8 bytes vs 16 bytes
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when ownership is required for correctness, lifetime complexity would dominate the API, or measurement shows no meaningful allocation/copy cost.

## verification
Measure allocations, copies, cache misses, and benchmark deltas on representative inputs.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- mem-assert-type-size
- mem-box-large-variant
- num-cast-try-from
- num-nonzero
- type-newtype-ids
