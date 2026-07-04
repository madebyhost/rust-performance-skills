# FFI Bindings Reference

## Tool Choices

- `bindgen`: generate Rust bindings from C/C++ headers.
- `cbindgen`: generate C/C++ headers for Rust libraries.
- PyO3/maturin: Python extension modules.
- napi-rs: Node.js native modules.

## Boundary Rules

- Never unwind Rust panics across FFI.
- Use `#[repr(C)]` only where layout is part of the ABI.
- Make allocation/free pairs explicit.
- Do not pass borrowed Rust references to foreign code unless lifetime and aliasing are guaranteed.
- Convert errors into stable foreign-language error values.

## Safety Wrapper

Raw FFI layer:

- `extern` declarations;
- raw pointers;
- unsafe calls;
- minimal translation.

Safe wrapper:

- validates null/alignment/lifetime;
- owns resources via RAII;
- maps errors;
- documents thread-safety.

## Verification

- Compile generated bindings in CI.
- Run sanitizers where possible.
- Test null pointers, invalid inputs, double free prevention, and panic boundaries.
