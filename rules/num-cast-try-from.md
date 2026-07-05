# num-cast-try-from

## id
num-cast-try-from

## severity
high

## trigger
Avoid `as` for narrowing casts; use `From` for widening and `TryFrom` for narrowing. Trigger when working on numeric safety and the code shows `num`-class risk.

## bad
```rust
fn narrow(x: u32) -> u8 {
    x as u8  // silently truncates: 300 becomes 44
}

fn to_index(f: f64) -> usize {
    f as usize  // NaN becomes 0, negatives become 0, may truncate
}

fn widen(x: u8) -> u32 {
    x as u32  // works, but hides that this is always safe
}
```

## good
```rust
use std::convert::TryFrom;

// widening: From<u8> for u32 is always lossless - won't compile if lossy
fn widen(x: u8) -> u32 {
    u32::from(x)
    // or: x.into()
}

// narrowing: TryFrom makes the failure case explicit
fn narrow(x: u32) -> Result<u8, <u8 as TryFrom<u32>>::Error> {
    u8::try_from(x)
    // or: x.try_into()
}

// float -> integer: validate the range manually before casting
fn float_to_index(f: f64, len: usize) -> Option<usize> {
    if f.is_nan() || f < 0.0 || f >= len as f64 {
        return None;
    }
    Some(f as usize)  // `as` is acceptable here: range is verified above
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::convert::TryFrom;

    #[test]
    fn widen_is_lossless() {
        assert_eq!(widen(255), 255u32);
    }

    #[test]
    fn narrow_errors_on_overflow() {
        assert!(narrow(300).is_err());
        assert_eq!(narrow(200), Ok(200u8));
    }

    #[test]
    fn float_to_index_rejects_nan_and_negative() {
        assert_eq!(float_to_index(f64::NAN, 10), None);
        assert_eq!(float_to_index(-1.0, 10), None);
        assert_eq!(float_to_index(3.9, 10), Some(3));
    }

    #[test]
    fn as_cast_truncation_footgun() {
        // demonstrating why `as` is dangerous for narrowing:
        let x: u32 = 300;
        assert_eq!(x as u8, 44);  // 300 % 256 == 44 - silently wrong
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
- conv-tryfrom-fallible
- num-overflow-explicit
