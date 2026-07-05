# opt-cache-friendly

## id
opt-cache-friendly

## severity
high

## trigger
Organize data for cache-efficient access patterns. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```rust
// Array of Structs (AoS) - poor cache use when accessing one field
struct Particle {
    position: [f32; 3],  // 12 bytes
    velocity: [f32; 3],  // 12 bytes
    mass: f32,           // 4 bytes
    id: u64,             // 8 bytes
    flags: u8,           // 1 byte + padding
    // Total: 40 bytes per particle
}

fn update_positions(particles: &mut [Particle], dt: f32) {
    for p in particles {
        // Access position and velocity - 24 bytes
        // But loads 40-byte struct per particle
        // 16 bytes wasted per cache line load
        p.position[0] += p.velocity[0] * dt;
        p.position[1] += p.velocity[1] * dt;
        p.position[2] += p.velocity[2] * dt;
    }
}
```

## good
```rust
// Struct of Arrays (SoA) - cache-efficient for field access
struct Particles {
    positions_x: Vec<f32>,
    positions_y: Vec<f32>,
    positions_z: Vec<f32>,
    velocities_x: Vec<f32>,
    velocities_y: Vec<f32>,
    velocities_z: Vec<f32>,
    masses: Vec<f32>,
    ids: Vec<u64>,
    flags: Vec<u8>,
}

fn update_positions(p: &mut Particles, dt: f32) {
    // Access contiguous memory - perfect cache utilization
    for (px, vx) in p.positions_x.iter_mut().zip(&p.velocities_x) {
        *px += vx * dt;
    }
    for (py, vy) in p.positions_y.iter_mut().zip(&p.velocities_y) {
        *py += vy * dt;
    }
    for (pz, vz) in p.positions_z.iter_mut().zip(&p.velocities_z) {
        *pz += vz * dt;
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply compiler hints globally or speculatively; keep them for measured hot paths and deployment-specific profiles.

## verification
Inspect release profile, generated code when useful, and benchmark hot paths before keeping the change.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- mem-box-large-variant
- mem-smaller-integers
- opt-bounds-check
