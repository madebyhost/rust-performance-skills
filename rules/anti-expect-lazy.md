# anti-expect-lazy

## id
anti-expect-lazy

## severity
reference

## trigger
Don't use expect for recoverable errors. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Network failures are expected - don't panic
let response = client.get(url).await.expect("failed to fetch");

// Files might not exist
let config = fs::read_to_string("config.toml").expect("config not found");

// User input can be invalid
let age: u32 = input.parse().expect("invalid age");

// Database queries can fail
let user = db.find_user(id).await.expect("user not found");
```

## good
```rust
// Handle recoverable errors properly
let response = client.get(url).await
    .context("failed to fetch URL")?;

// Return error if file doesn't exist
let config = fs::read_to_string("config.toml")
    .context("failed to read config file")?;

// Validate and return error
let age: u32 = input.parse()
    .map_err(|_| Error::InvalidInput("age must be a number"))?;

// Handle missing data
let user = db.find_user(id).await?
    .ok_or(Error::NotFound("user"))?;
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
- anti-unwrap-abuse
- err-expect-bugs-only
- err-no-unwrap-prod
