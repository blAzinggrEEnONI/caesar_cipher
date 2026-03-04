# ADR-004: Functional Core, Imperative Shell

**Status:** Accepted  
**Date:** 2026-03-01  
**Author:** Tanatswa D. Muskwe (grimm)

## Context

We need to organize code in a way that:
- Makes business logic easy to test
- Separates pure logic from side effects
- Improves code reliability and maintainability
- Supports property-based testing

## Decision

We will separate the application into:
- **Functional Core** - Pure functions with no side effects (domain, core)
- **Imperative Shell** - Handles all I/O and side effects (adapters)

## Rationale

### Why Functional Core / Imperative Shell?

**Pros:**
- Pure functions are trivial to test (no mocks needed)
- Business logic has no I/O dependencies
- Easy to reason about (deterministic)
- Supports property-based testing
- Can parallelize pure functions safely

**Cons:**
- Must pass data explicitly (no global state)
- Requires discipline to maintain boundaries
- May feel unnatural to OOP developers

### Alternatives Considered

1. **Mixed Approach**
   - Rejected: Hard to test (need to mock I/O)
   - Business logic coupled to infrastructure

2. **Full Functional Programming**
   - Rejected: Too extreme for Python
   - Would require monads everywhere

3. **Traditional OOP**
   - Rejected: Objects often mix logic and I/O
   - Harder to test

## Consequences

### Positive
- Core logic is pure and easily testable
- No mocking needed for business logic tests
- Can use property-based testing effectively
- Clear separation of concerns

### Negative
- Must pass data explicitly through function parameters
- Can't use global state or singletons in core
- Requires understanding of pure functions

### Neutral
- Shell coordinates between core and external systems
- Need clear boundary between core and shell

## Implementation

### Functional Core (Pure)
```python
# core/cipher_engine.py
def shift_character(char: str, shift: Shift) -> str:
    """Pure function - no side effects"""
    if not char.isalpha():
        return char
    # ... pure transformation
    return result
```

### Imperative Shell (I/O)
```python
# adapters/file_io.py
class FileTextInput:
    """Handles I/O side effects"""
    def read_text(self) -> Result[str, IOError]:
        try:
            return Ok(self._path.read_text())
        except FileNotFoundError:
            return Err(IOError(...))
```

## Usage Guidelines

**Functional Core should:**
- Have no I/O operations
- Be deterministic (same input → same output)
- Have no side effects
- Not depend on external state
- Be in `domain/` and `core/` directories

**Imperative Shell should:**
- Handle all I/O (files, network, console)
- Coordinate between core and external systems
- Return Result types for operations that can fail
- Be in `adapters/` directory

**Never:**
- Put I/O in core functions
- Put business logic in adapters
- Mix pure and impure code in same function

## Validation

Success criteria:
- [ ] Core functions have no I/O
- [ ] Core functions are deterministic
- [ ] All I/O is in adapters
- [ ] Core functions easy to test without mocks

## References

- Functional Core, Imperative Shell pattern by Gary Bernhardt
- Boundaries talk by Gary Bernhardt
