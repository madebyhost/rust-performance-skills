# proj-build-rs-minimal

## id
proj-build-rs-minimal

## severity
low

## trigger
Keep `build.rs` minimal, deterministic, and idempotent. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```rust
// build.rs - overly broad, non-deterministic, network-dependent
use std::process::Command;

fn main() {
    // re-runs on every build because no rerun directives are emitted
    // (Cargo default: re-run if ANY file changes)

    // fragile: parses version string instead of probing capability
    let output = Command::new("rustc").arg("--version").output().unwrap();
    let version = String::from_utf8(output.stdout).unwrap();
    if version.contains("1.8") {
        println!("cargo::rustc-cfg=has_feature");
    }

    // network access breaks offline/reproducible builds
    let _resp = reqwest::blocking::get("https://example.com/schema.json").unwrap();
}
```

## good
```rust
// build.rs - narrow directives, capability probe via autocfg, no network
fn main() {
    // Only re-run when these specific files change
    println!("cargo::rerun-if-changed=build.rs");
    println!("cargo::rerun-if-changed=src/generated.rs");
    println!("cargo::rerun-if-env-changed=MY_BUILD_FLAG");

    // Probe actual compiler capability instead of parsing version strings
    let ac = autocfg::new();
    // Emit cfg if the compiler supports the feature we need
    ac.emit_has_type("std::collections::BTreeMap");

    // Conditional cfg from env var
    if std::env::var("MY_BUILD_FLAG").is_ok() {
        println!("cargo::rustc-cfg=my_feature");
    }
}
```

```toml
[build-dependencies]
autocfg = "1"
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
- lint-cfg-check
- proj-feature-additive
