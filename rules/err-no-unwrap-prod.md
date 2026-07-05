# err-no-unwrap-prod

## id
err-no-unwrap-prod

## severity
critical

## trigger
Avoid `unwrap()` in production code; use `?`, `expect()`, or handle errors. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
fn process_request(req: Request) -> Response {
    let user_id = req.headers.get("X-User-Id").unwrap();  // Why did it fail?
    let user = database.find_user(user_id).unwrap();       // Which operation?
    let data = user.preferences.get("theme").unwrap();     // No context

    Response::new(data)
}

// Crash message: "called `Option::unwrap()` on a `None` value"
// Where? Why? No idea.
```

## good
```rust
// Option 1: Propagate with ?
fn process_request(req: Request) -> Result<Response, AppError> {
    let user_id = req.headers
        .get("X-User-Id")
        .ok_or(AppError::MissingHeader("X-User-Id"))?;

    let user = database.find_user(user_id)?;

    let data = user.preferences
        .get("theme")
        .ok_or(AppError::MissingPreference("theme"))?;

    Ok(Response::new(data))
}

// Option 2: expect() for invariants (not user input)
fn get_config_value(&self, key: &str) -> &str {
    self.config
        .get(key)
        .expect("BUG: required config key missing after validation")
}

// Option 3: Provide defaults
fn get_theme(user: &User) -> &str {
    user.preferences
        .get("theme")
        .unwrap_or(&"default")
}

// Option 4: Match for complex handling
fn process_optional(value: Option<Data>) -> ProcessedData {
    match value {
        Some(data) => process(data),
        None => {
            log::warn!("No data provided, using fallback");
            ProcessedData::default()
        }
    }
}
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
- err-result-over-panic
