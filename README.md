# Caesar Cipher CLI - Architecture Showcase

**Author:** Tanatswa D. Muskwe
**Architecture:** Hexagonal (Ports & Adapters)  
**License:** MIT

A command-line tool for encrypting, decrypting, and cracking Caesar cipher messages with frequency analysis.

**This project showcases a personalized coding architecture featuring clean code principles, domain-driven design, and functional programming patterns.**

## 🎯 What Makes This Special

This isn't just a Caesar cipher - it's a **complete architectural template** demonstrating:

- **Hexagonal Architecture** (Ports & Adapters) - clean separation of concerns
- **Functional Core / Imperative Shell** - pure business logic isolated from I/O
- **Result Types** - explicit error handling without exceptions
- **Immutable Value Objects** - domain modeling with validated invariants
- **Dependency Injection** - loose coupling via Protocol interfaces
- **Comprehensive Documentation** - design decisions explained throughout

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Adapters (Shell)                │
│  CLI │ File I/O │ Console                │
├─────────────────────────────────────────┤
│         Ports (Interfaces)              │
│  Protocols defining contracts           │
├─────────────────────────────────────────┤
│      Domain Core (Functional)           │
│  Pure business logic, no I/O            │
│  Value Objects │ Services                │
└─────────────────────────────────────────┘
```

**See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.**

## ✨ Features

- **Encrypt** text with a configurable shift key
- **Decrypt** messages when you know the key
- **Crack** encrypted text using brute force and statistical frequency analysis
- Support for file I/O and stdin/stdout piping
- Rich terminal output with colored text and formatted tables
- **43 passing tests** with performance benchmarks
- **Reusable templates** for applying this architecture to other projects

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- pip

### Install from Source

```bash
# Clone the repository
git clone https://github.com/blAzinggrEEnONI/caesar_cipher.git
cd caesar_cipher

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## 🚀 Usage

```bash
# Install the package
pip3 install -e .

# Or for development with testing tools
pip3 install -e ".[dev]"

# Using Justfile
just install
# or
just dev-install
```

## Usage

### Encrypt

```bash
# Basic encryption
caesar-cipher encrypt "HELLO WORLD" --key 3

# From file
caesar-cipher encrypt --input-file message.txt --key 5

# To file
caesar-cipher encrypt "SECRET" --key 7 --output-file encrypted.txt

# Using Justfile
just encrypt "HELLO" 3
```

### Decrypt

```bash
# Basic decryption
caesar-cipher decrypt "KHOOR ZRUOG" --key 3

# From stdin
echo "KHOOR" | caesar-cipher decrypt --key 3

# Using Justfile
just decrypt "KHOOR" 3
```

### Crack

```bash
# Brute force with frequency analysis
caesar-cipher crack "KHOOR ZRUOG"

# Show top 3 candidates
caesar-cipher crack "KHOOR ZRUOG" --top 3

# Show all 26 possibilities
caesar-cipher crack "KHOOR ZRUOG" --all

# Using Justfile
just crack "KHOOR ZRUOG"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=caesar_cipher --cov-report=html

# Run performance tests
pytest tests/test_performance.py -v -s

# Type checking
mypy src/

# Linting
ruff check src/
```

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed architecture documentation
- **[docs/decisions/](docs/decisions/)** - Architecture Decision Records (ADRs)

##  Key Concepts

### Result Types
Explicit error handling without exceptions:
```python
match result:
    case Ok(value):
        process(value)
    case Err(error):
        handle_error(error)
```

### Immutable Value Objects
Domain concepts with validated invariants:
```python
@dataclass(frozen=True)
class Shift:
    value: int
    
    @staticmethod
    def create(value: int) -> Result['Shift', ValidationError]:
        normalized = value % 26
        return Ok(Shift(value=normalized))
```

### Dependency Injection
Loose coupling via Protocol interfaces:
```python
class CipherService:
    def __init__(self, engine: CipherEnginePort):
        self._engine = engine
```

## 📊 Project Statistics

- **Lines of Code:** ~2,500 (excluding tests)
- **Test Coverage:** 43 tests, all passing ✓
- **Documentation:** Architecture design and ADRs
- **ADRs:** 4 architecture decision records
- **Performance:** All operations < 100ms for typical use

## 🤝 Contributing

This is a personal coding style showcase, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 👤 Author

**Tanatswa D. Muskwe**

- GitHub: [@blAzinggrEEnONI](https://github.com/blAzinggrEEnONI)
- Email: tanatswadmu@gmail.com
- Project: Caesar Cipher CLI - Architecture Showcase

## 🌟 Acknowledgments

This architecture is inspired by:
- Hexagonal Architecture (Alistair Cockburn)
- Domain-Driven Design (Eric Evans)
- Functional Core, Imperative Shell (Gary Bernhardt)
- Railway Oriented Programming (Scott Wlaschin)

---

*"Code is read more often than it is written. Make it clear, make it testable, make it yours."*
