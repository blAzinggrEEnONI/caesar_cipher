# ADR-001: Hexagonal Architecture (Ports & Adapters)

**Status:** Accepted  
**Date:** 2026-03-01  
**Author:** Tanatswa D. Muskwe (grimm)

## Context

We need an architecture that:
- Separates business logic from infrastructure concerns
- Makes the application testable without I/O
- Allows swapping implementations (CLI → Web API)
- Supports long-term maintainability

## Decision

We will use Hexagonal Architecture (Ports & Adapters pattern) with three layers:

1. **Domain Core** (inner) - Pure business logic, no I/O
2. **Ports** (middle) - Protocol interfaces defining contracts
3. **Adapters** (outer) - I/O implementations (CLI, files, console)

## Rationale

### Why Hexagonal Architecture?

**Pros:**
- Business logic is completely independent of infrastructure
- Easy to test domain logic without mocking I/O
- Can swap UI (CLI → Web) without changing core
- Clear dependency direction (outer depends on inner)
- Aligns with Domain-Driven Design principles

**Cons:**
- More files and indirection than simple layered architecture
- Requires discipline to maintain boundaries
- Initial setup is more complex

### Alternatives Considered

1. **Simple Layered Architecture**
   - Rejected: Business logic often leaks into presentation layer
   - Harder to test without I/O

2. **Clean Architecture (Uncle Bob)**
   - Similar to Hexagonal but more layers
   - Rejected: Too complex for this project size

3. **MVC Pattern**
   - Rejected: Doesn't separate I/O from business logic well
   - Controller often becomes bloated

## Consequences

### Positive
- Domain logic is pure and easily testable
- Can add new adapters (web API, GUI) without changing core
- Clear separation makes code easier to understand
- Supports TDD and property-based testing

### Negative
- More files to navigate
- Requires understanding of ports/adapters concept
- Initial development is slower

### Neutral
- Need composition root to wire dependencies
- Must define port interfaces explicitly

## Implementation

```
src/caesar_cipher/
├── domain/          # Business logic
├── core/            # Pure functions
├── ports/           # Interfaces
├── adapters/        # I/O implementations
└── composition/     # Dependency wiring
```

## Validation

Success criteria:
- [ ] Can test domain logic without I/O
- [ ] Can swap CLI for different UI
- [ ] Business logic has no infrastructure dependencies
- [ ] Clear dependency flow (outer → inner)

## References

- Hexagonal Architecture pattern by Alistair Cockburn
- Ports and Adapters Architecture pattern
