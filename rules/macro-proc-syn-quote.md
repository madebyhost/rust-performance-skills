# macro-proc-syn-quote

## id
macro-proc-syn-quote

## severity
medium

## trigger
Build procedural macros with `syn`, `quote`, and `proc-macro2`. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// Manually iterating tokens to find a struct name - brittle and hard to read.
use proc_macro::TokenStream;

#[proc_macro_derive(Hello)]
pub fn derive_hello(input: TokenStream) -> TokenStream {
    let mut iter = input.into_iter();
    // skip `struct`, grab the next ident... error-prone and breaks on generics
    iter.next(); // "struct"
    let name = iter.next().unwrap().to_string();
    format!("impl Hello for {name} {{ fn hello(&self) {{ println!(\"hello\"); }} }}")
        .parse()
        .unwrap()
}
```

## good
```toml
# Cargo.toml for the derive crate
[dependencies]
syn  = { version = "2", features = ["derive"] }
quote = "1"
proc-macro2 = "1"
```

```rust
// src/lib.rs
use proc_macro::TokenStream;
use proc_macro2::Span;
use quote::{quote, quote_spanned};
use syn::{parse_macro_input, spanned::Spanned, DeriveInput};

#[proc_macro_derive(Hello)]
pub fn derive_hello(input: TokenStream) -> TokenStream {
    // parse_macro_input! gives a typed DeriveInput or emits a compile error.
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;
    let (impl_generics, ty_generics, where_clause) = input.generics.split_for_impl();

    // quote! quasi-quotes Rust tokens; `#name` splices the identifier.
    let expanded = quote! {
        impl #impl_generics Hello for #name #ty_generics #where_clause {
            fn hello(&self) {
                println!("hello from {}", stringify!(#name));
            }
        }
    };

    expanded.into()
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
- macro-proc-error-spans
- macro-proc-two-crate
