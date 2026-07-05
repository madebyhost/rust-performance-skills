# mem-arrayvec

## id
mem-arrayvec

## severity
critical

## trigger
Use `ArrayVec<T, N>` for fixed-capacity collections that never heap-allocate. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
// Vec always heap-allocates, even for small collections
fn parse_options(input: &str) -> Vec<Option> {
    let mut options = Vec::new();  // Heap allocation
    for part in input.split(',').take(8) {  // Know we never exceed 8
        options.push(parse_option(part));
    }
    options
}

// Or SmallVec when you truly can't exceed capacity
use smallvec::SmallVec;
fn get_flags() -> SmallVec<[Flag; 4]> {
    // SmallVec CAN heap-allocate if pushed beyond 4
    // That might be unexpected in no-alloc contexts
}
```

## good
```rust
use arrayvec::ArrayVec;

// Guaranteed no heap allocation
fn parse_options(input: &str) -> ArrayVec<Option<u32>, 8> {
    let mut options = ArrayVec::new();
    for part in input.split(',') {
        if options.try_push(parse_option(part)).is_err() {
            break;  // Capacity reached, stop
        }
    }
    options
}

// For embedded/no_std contexts
#[no_std]
fn collect_readings() -> ArrayVec<SensorReading, 16> {
    let mut readings = ArrayVec::new();
    for sensor in SENSORS.iter() {
        readings.push(sensor.read());  // Panics if > 16
    }
    readings
}
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
- mem-smallvec
- mem-with-capacity
- own-move-large
