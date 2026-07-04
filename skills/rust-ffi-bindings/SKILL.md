---
name: rust-ffi-bindings
description: "Use when creating or reviewing Rust bindings across language boundaries: C, C++, Python, Node.js, Ruby, Swift, bindgen, cbindgen, napi-rs, PyO3, extern functions, repr(C), ABI stability, ownership transfer, error mapping, memory management, and safe wrapper design."
---

# Rust FFI Bindings

Use this skill for interop design. Load `references/ffi-bindings.md` for detailed guidance.

## Workflow

1. Define direction: C calls Rust, Rust calls C/C++, Node calls Rust, Python calls Rust, or Rust embeds another runtime.
2. Define ownership: who allocates, who frees, who mutates, who owns errors.
3. Keep raw FFI thin and unsafe; expose a safe Rust wrapper or safe foreign-language wrapper.
4. Use generated bindings where appropriate, then audit the generated boundary.
5. Test ABI, memory, error, thread-safety, and panic boundaries.

## Output

Include ABI shape, ownership table, error mapping, thread-safety stance, panic policy, and test plan.
