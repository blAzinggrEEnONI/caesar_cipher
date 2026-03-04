# Architecture Documentation

**Author:** Tanatswa D. Muskwe  
**Project:** Caesar Cipher CLI  
**Architecture Style:** Hexagonal (Ports & Adapters) with Functional Core

## Overview

This project showcases a personalized coding architecture that emphasizes:
- Clean separation of concerns
- Explicit error handling
- Testable, maintainable code
- Domain-driven design principles

The architecture is designed to be **reusable across projects** and represents a distinctive coding signature.

## Architectural Layers

### 1. Domain Core (Inner Layer)

**Purpose:** Pure business logic with no external dependencies.

**Location:** `src/caesar_cipher/domain/` and `src/caesar_cipher/core/`

**Characteristics:**
- No I/O operations
- No framework dependencies
- Pure functions (deterministic, no side effects)
- Immutable data structures
- Rich domain models

**Components:**

#### Value Objects (`domain/values.py`)
Immutable objects representing domain concepts:
- `Shift` - validated shift value with inverse calculation
- `PlainText` / `CipherText` - type-safe text wrappers
- `FrequencyScore` - chi-squared analysis score
- `CrackResult` - aggregates shift, text, and score

**Design Decision:** Using `NewType` for PlainText/CipherText prevents accidentally mixing them.

#### Domain Services (`domain/services.py`)
Coordinate business logic that doesn't belong to a single entity:
- `CipherService` - orchestrates encryption, decryption, and cracking
- Depends only on port interfaces (not concrete implementations)

#### Pure Functions (`core/cipher_engine.py`, `core/frequency_analyzer.py`)
Stateless, deterministic operations:
- `shift_character()` - transforms single character
- `transform_text()` - applies shift to text
- `calculate_chi_squared()` - statistical analysis

**Mathematical Properties:**
- Round-trip: `decrypt(encrypt(text, s), s) = text`
- Inverse: `shift + shift.inverse() ≡ 0 (mod 26)`

### 2. Ports (Middle Layer)

**Purpose:** Define contracts between domain and infrastructure.

**Location:** `src/caesar_cipher/ports/interfaces.py`

**Characteristics:**
- Protocol classes (structural typing)
- No implementation details
- Enable dependency inversion

**Interfaces:**
- `TextInputPort` - reading text from various sources
- `TextOutputPort` - writing text to various destinations
- `CipherEnginePort` - encryption/decryption operations
- `FrequencyAnalyzerPort` - text analysis

**Design Decision:** Using Protocols instead of abstract base classes allows duck typing and easier testing.

### 3. Adapters (Outer Layer)

**Purpose:** Handle all I/O and external system interactions.

**Location:** `src/caesar_cipher/adapters/`

**Characteristics:**
- Implement port interfaces
- Handle side effects (file I/O, console output)
- Isolate external dependencies (Rich, Typer)
- Return Result types for operations that can fail

**Adapters:**

#### File I/O (`adapters/file_io.py`)
- `FileTextInput` - reads from files
- `FileTextOutput` - writes to files
- `StdinTextInput` - reads from stdin
- `ArgumentTextInput` - provides command-line arguments

**Error Handling:** All I/O operations return `Result[T, IOError]` with rich context.

#### Console (`adapters/console.py`)
- `ConsoleOutput` - Rich-based formatting
- Isolates Rich library to single module
- Formats tables, errors, and colored output

#### CLI (`adapters/cli.py`)
- Typer-based command-line interface
- Delegates to domain services
- Handles user input validation
- Pattern matches on Result types for error handling

### 4. Composition Root

**Purpose:** Single place where all dependencies are wired together.

**Location:** `src/caesar_cipher/composition/container.py`

**Function:** `compose_application()`
1. Creates concrete implementations
2. Injects dependencies
3. Returns fully configured application

**Design Decision:** Manual dependency injection (no framework) keeps it simple and explicit.

## Error Handling Strategy

### Result Type Pattern

Instead of exceptions for expected failures, we use Result types:

```python
Result[T, E] = Ok[T] | Err[E]
```

**Benefits:**
- Errors are explicit in function signatures
- Type-safe error handling
- Forces callers to handle errors
- No hidden control flow

**When to use Result:**
- File I/O operations
- Validation
- Parsing
- Any operation with expected failure modes

**When to use Exceptions:**
- Programming errors (assertions)
- Unrecoverable errors
- System failures

### Error Hierarchy

```
DomainError (base)
├── ValidationError - invalid input
├── CipherError - cipher operation failures
├── AnalysisError - frequency analysis failures
└── IOError - file/network I/O failures
```

**Rich Context:** All errors capture operation, inputs, and state for debugging.

## Data Flow

### Encryption Flow
```
User Input (CLI)
  → ArgumentTextInput.read_text() → Result[str, IOError]
  → PlainText (type wrapper)
  → CipherService.encrypt_text(plaintext, shift)
    → PureCipherEngine.encrypt() → CipherText
  → FileTextOutput.write_text() or ConsoleOutput.print_success()
```

### Cracking Flow
```
User Input (CLI)
  → Read ciphertext
  → CipherService.crack_cipher(ciphertext, analyzer, top_n)
    → Try all 26 shifts
    → EnglishFrequencyAnalyzer.analyze() for each
    → Sort by score
    → Return top N results
  → ConsoleOutput.format_crack_results()
```

## Design Decisions

### 1. Hexagonal Architecture

**Rationale:** Separates business logic from infrastructure, making the core testable without I/O.

**Trade-off:** More files and indirection, but better maintainability and testability.

**Benefit:** Can swap CLI for web API without changing domain logic.

### 2. Functional Core / Imperative Shell

**Rationale:** Pure functions are easier to test, reason about, and parallelize.

**Trade-off:** Must pass data explicitly (no global state).

**Benefit:** Core logic has zero I/O dependencies.

### 3. Immutable Value Objects

**Rationale:** Prevents bugs from unexpected mutations.

**Trade-off:** Must create new instances for changes.

**Benefit:** Thread-safe, easier to reason about, no defensive copying.

### 4. NewType for Domain Primitives

**Rationale:** Prevents mixing PlainText and CipherText accidentally.

**Trade-off:** Runtime overhead is zero (just type checking).

**Benefit:** Catches errors at type-check time, not runtime.

### 5. Result Types Over Exceptions

**Rationale:** Makes error handling explicit and type-safe.

**Trade-off:** More verbose than exceptions.

**Benefit:** No hidden control flow, forces error handling.

## Testing Strategy

### Test Organization

```
tests/
├── test_new_cipher.py       # Pure cipher functions
├── test_new_analyzer.py     # Frequency analysis
├── test_domain_service.py   # Business logic
└── test_*.py                # Legacy tests (kept for reference)
```

### Testing Principles

1. **Unit Tests** - Test pure functions in isolation
2. **Integration Tests** - Test adapter interactions
3. **Property Tests** - Test universal properties (optional)

### Test Coverage

- Core functions: 100% (pure, easy to test)
- Domain services: High coverage
- Adapters: Integration tests for I/O paths

## Extension Points

The architecture makes these extensions easy:

### 1. New Cipher Algorithms
- Implement `CipherEnginePort`
- Change instantiation in composition root
- No other code changes needed

### 2. New Input/Output Sources
- Implement `TextInputPort` / `TextOutputPort`
- Examples: HTTP API, database, message queue

### 3. New Analysis Methods
- Implement `FrequencyAnalyzerPort`
- Examples: N-gram analysis, dictionary matching

### 4. New UI
- Implement new adapter (web, GUI, TUI)
- Reuse all domain logic

## Performance Characteristics

### Cipher Operations
- **Time:** O(n) where n is text length
- **Space:** O(n) for result string
- **Optimization:** Generator expressions for memory efficiency

### Frequency Analysis
- **Time:** O(n) for counting + O(26) for chi-squared = O(n)
- **Space:** O(26) for letter counts
- **No optimization needed** - already efficient

### Cracking
- **Time:** O(26 * n) where n is text length
- **Could parallelize** but 26 iterations is trivial
- **Design choice:** Prefer simplicity over premature optimization

## Code Style Signature

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names over abbreviations

### Documentation Style
- Docstrings include: purpose, args, returns, examples, design decisions
- Comments explain "why" not "what"
- ASCII diagrams for complex flows
- Mathematical properties documented

### Type Annotations
- All public functions fully annotated
- Domain-specific type aliases (PlainText, CipherText)
- Protocol classes for interfaces
- Generic types for Result[T, E]

### Module Organization
- By feature/domain, not technical layer
- Clear separation: core, domain, ports, adapters, composition
- Each module has single responsibility

## Author's Philosophy

**"Explicit is better than implicit. Simple is better than complex. Testable is better than clever."**

This architecture prioritizes:
1. **Clarity** - Code should be self-documenting
2. **Testability** - Pure functions, dependency injection
3. **Maintainability** - Loose coupling, high cohesion
4. **Reusability** - Patterns applicable across projects

---

**Author:** Tanatswa D. Muskwe  
**License:** MIT  
**Last Updated:** March 2026
