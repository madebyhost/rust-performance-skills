# proj-mod-by-feature

## id
proj-mod-by-feature

## severity
low

## trigger
Organize modules by feature, not type. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```
src/
|-- controllers/
|   |-- user_controller.rs
|   |-- order_controller.rs
|   `-- product_controller.rs
|-- models/
|   |-- user.rs
|   |-- order.rs
|   `-- product.rs
|-- services/
|   |-- user_service.rs
|   |-- order_service.rs
|   `-- product_service.rs
`-- repositories/
    |-- user_repository.rs
    |-- order_repository.rs
    `-- product_repository.rs
```

## good
```
src/
|-- user/
|   |-- mod.rs           # Re-exports public items
|   |-- model.rs         # User struct, types
|   |-- repository.rs    # Database operations
|   |-- service.rs       # Business logic
|   `-- handler.rs       # HTTP handlers
|-- order/
|   |-- mod.rs
|   |-- model.rs
|   |-- repository.rs
|   |-- service.rs
|   `-- handler.rs
|-- product/
|   |-- mod.rs
|   |-- model.rs
|   |-- repository.rs
|   `-- handler.rs
`-- lib.rs
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
- proj-flat-small
- proj-lib-main-split
- proj-pub-use-reexport
