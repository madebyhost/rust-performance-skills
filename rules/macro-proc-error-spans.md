# macro-proc-error-spans

## id
macro-proc-error-spans

## severity
medium

## trigger
Report proc-macro errors as spanned compile errors, never by panicking. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
use proc_macro::TokenStream;
use syn::{parse_macro_input, Data, DeriveInput};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match input.data {
        Data::Struct(ref s) => &s.fields,
        _ => panic!("MyTrait can only be derived on structs"), // WRONG
    };

    // `.unwrap()` here gives "called `Option::unwrap()` on a `None` value"
    // with no location info in user code.
    let first = fields.iter().next().unwrap();
    let name = first.ident.as_ref().unwrap();

    quote::quote! {
        impl MyTrait for #name {}
    }
    .into()
}
```

```text
error: proc macro panicked
  --> src/main.rs:3:10
   |
 3 | #[derive(MyTrait)]
   |          ^^^^^^^
   |
   = help: message: MyTrait can only be derived on structs
```

## good
```rust
use proc_macro::TokenStream;
use proc_macro2::TokenStream as TokenStream2;
use quote::quote;
use syn::{parse_macro_input, spanned::Spanned, Data, DeriveInput, Error};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    derive_my_trait_inner(input).unwrap_or_else(|e| e.to_compile_error().into())
}

fn derive_my_trait_inner(input: TokenStream) -> Result<TokenStream, Error> {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match &input.data {
        Data::Struct(s) => &s.fields,
        Data::Enum(e) => {
            return Err(Error::new_spanned(
                &input.ident,
                "MyTrait can only be derived on structs, not enums",
            ));
        }
        Data::Union(u) => {
            return Err(Error::new_spanned(
                &input.ident,
                "MyTrait can only be derived on structs, not unions",
            ));
        }
    };

    let first = fields.iter().next().ok_or_else(|| {
        Error::new_spanned(&input.ident, "MyTrait requires at least one field")
    })?;

    let field_name = first.ident.as_ref().ok_or_else(|| {
        // Attach the error to the field's span, not the struct name.
        Error::new_spanned(first, "MyTrait requires named fields")
    })?;

    let struct_name = &input.ident;
    Ok(quote! {
        impl MyTrait for #struct_name {
            fn first_field_name() -> &'static str {
                stringify!(#field_name)
            }
        }
    }
    .into())
}
```

```text
error: MyTrait requires named fields
  --> src/main.rs:7:5
   |
 7 |     u8,   // tuple struct field
   |     ^^
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
- err-thiserror-lib
- macro-proc-syn-quote
