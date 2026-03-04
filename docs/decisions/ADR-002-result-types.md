# ADR-002: Result Types for Error Handling

**Status:** Accepted  
**Date:** 2026-03-01  
**Author:** Tanatswa D. Muskwe (grimm)

## Context

We need a consistent error handling strategy that:
- Makes errors explicit in function signatures
- Forces callers to handle errors
- Provides type safety
- Avoids hidden control flow

## Decision

We will use Result types (`Result[T, E] = Ok[T] | Err[E]`) for operations that can fail in expected ways, and reserve exceptions for unexpected/unrecoverable errors.

## Rationale

### Why Result Types?

**Pros:**
- Errors are explicit in function signatures
- Type checker enforces error handling
- No hidden control flow (unlike exceptions)
- Composable with map/bind operations
- Aligns with functional programming principles

**Cons:**
- More verbose than exceptions
- Requires pattern matching or unwrap calls
- Not idiomatic Python (exceptions are standard)

### Alternatives Considered

1. **Exceptions Only**
   - Rejected: Errors not visible in signatures
   - Easy to forget error handling
   - Hidden control flow

2. **Optional/Maybe Types**
   - Rejected: Loses error information
   - Can't distinguish different error types

3. **Error Codes**
   - Rejected: Not type-safe
   - Easy to ignore return values

## Consequences

### Positive
- Impossible to ignore errors (type checker catches)
- Clear which operations can fail
- Rich error context always available
- Easier to reason about error paths

### Negative
- More verbose than exceptions
- Requires learning Result type API
- Not standard Python idiom

### Neutral
- Need to implement Result type
- Must decide when to use Result vs Exception

## Implementation

```python
@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    def map(self, func: Callable[[T], U]) -> Result[U, E]: ...
    def bind(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]: ...

@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    def map(self, func: Callable[[T], U]) -> Err[E]: ...
    def bind(self, func: Callable[[T], Result[U, E]]) -> Err[E]: ...

Result = Ok[T] | Err[E]
```

## Usage Guidelines

**Use Result for:**
- File I/O operations
- Network requests
- Validation
- Parsing
- Any operation with expected failure modes

**Use Exceptions for:**
- Programming errors (assertions)
- Unrecoverable errors (out of memory)
- System failures
- Violations of invariants

## Validation

Success criteria:
- [ ] All I/O operations return Result
- [ ] Type checker catches unhandled errors
- [ ] Error context is rich and useful
- [ ] Code is more explicit about error paths

## References

- Railway Oriented Programming pattern
- Rust Result Type pattern
