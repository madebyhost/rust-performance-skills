# test-mock-traits

## id
test-mock-traits

## severity
medium

## trigger
Use traits for dependencies to enable mocking in tests. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
struct UserService {
    db: PostgresConnection,  // Concrete type - hard to test
}

impl UserService {
    async fn get_user(&self, id: u64) -> Result<User, Error> {
        // Directly calls Postgres - needs real database to test
        self.db.query("SELECT * FROM users WHERE id = $1", &[&id]).await
    }
}

// Test requires real Postgres instance
#[tokio::test]
async fn test_get_user() {
    let db = PostgresConnection::connect("postgres://...").await?;
    let service = UserService { db };
    // Slow, flaky, can't test error paths
}
```

## good
```rust
// Define trait for dependency
#[async_trait]
trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: u64) -> Result<Option<User>, DbError>;
    async fn save(&self, user: &User) -> Result<(), DbError>;
}

// Production implementation
struct PostgresUserRepo {
    pool: PgPool,
}

#[async_trait]
impl UserRepository for PostgresUserRepo {
    async fn find_by_id(&self, id: u64) -> Result<Option<User>, DbError> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id)
            .fetch_optional(&self.pool)
            .await
    }
    // ...
}

// Service depends on trait, not concrete type
struct UserService<R: UserRepository> {
    repo: R,
}

impl<R: UserRepository> UserService<R> {
    async fn get_user(&self, id: u64) -> Result<User, Error> {
        self.repo.find_by_id(id).await?
            .ok_or(Error::NotFound)
    }
}

// Test with mock
#[cfg(test)]
mod tests {
    struct MockUserRepo {
        users: HashMap<u64, User>,
    }

    #[async_trait]
    impl UserRepository for MockUserRepo {
        async fn find_by_id(&self, id: u64) -> Result<Option<User>, DbError> {
            Ok(self.users.get(&id).cloned())
        }
        // ...
    }

    #[tokio::test]
    async fn test_get_user_found() {
        let mut mock = MockUserRepo { users: HashMap::new() };
        mock.users.insert(1, User { id: 1, name: "Alice".into() });

        let service = UserService { repo: mock };
        let user = service.get_user(1).await.unwrap();

        assert_eq!(user.name, "Alice");
    }

    #[tokio::test]
    async fn test_get_user_not_found() {
        let mock = MockUserRepo { users: HashMap::new() };
        let service = UserService { repo: mock };

        let result = service.get_user(999).await;
        assert!(matches!(result, Err(Error::NotFound)));
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Verify the test fails before the fix and covers the intended behavior rather than implementation detail.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-sealed-trait
- proj-lib-main-split
- test-proptest-properties
