# ADR-003: Immutable Value Objects

**Status:** Accepted  
**Date:** 2026-03-01  
**Author:** Tanatswa D. Muskwe (grimm)

## Context

We need to represent domain concepts in a way that:
- Prevents invalid states
- Makes invariants explicit
- Avoids bugs from unexpected mutations
- Provides type safety

## Decision

We will use immutable value objects (frozen dataclasses) to represent domain concepts, with factory methods for validation.

## Rationale

### Why Immutable Value Objects?

**Pros:**
- Invariants enforced at creation time
- No defensive copying needed
- Thread-safe by default
- Easier to reason about (no hidden mutations)
- Aligns with functional programming principles

**Cons:**
- Must create new instances for changes
- Slightly more memory usage
- Less familiar to OOP developers

### Alternatives Considered

1. **Mutable Objects**
   - Rejected: Easy to violate invariants
   - Requires defensive copying
   - Not thread-safe

2. **Primitive Types**
   - Rejected: No validation
   - Easy to mix incompatible values (PlainText vs CipherText)

3. **Named Tuples**
   - Rejected: Less clear than dataclasses
   - No custom methods

## Consequences

### Positive
- Impossible to create invalid objects
- No bugs from unexpected mutations
- Thread-safe without locks
- Clear domain modeling

### Negative
- Must create new instances for transformations
- Slightly more verbose

### Neutral
- Need factory methods for validation
- Use NewType for simple wrappers

## Implementation

```python
@dataclass(frozen=True)
class Shift:
    value: int
    
    @staticmethod
    def create(value: int) -> Result['Shift', ValidationError]:
        normalized = value % 26
        return Ok(Shift(value=normalized))
    
    def inverse(self) -> 'Shift':
        return Shift(value=(26 - self.value) % 26)
```

## Usage Guidelines

**Create value objects for:**
- Domain concepts (Money, Email, UserId)
- Values with invariants (DateRange, PositiveInt)
- Values that should not be mixed (PlainText vs CipherText)

**Use NewType for:**
- Simple type aliases without validation
- Preventing accidental mixing of primitives

**Always:**
- Use `@dataclass(frozen=True)`
- Validate in factory method
- Return new instances from methods
- Document invariants

## Validation

Success criteria:
- [ ] All domain concepts are value objects
- [ ] Invariants documented and enforced
- [ ] No mutable domain objects
- [ ] Type checker prevents mixing incompatible types

## References

- Value Object Pattern by Martin Fowler
- Domain-Driven Design by Eric Evans
