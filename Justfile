default:
    @just --list

install:
    pip3 install -e .

dev-install:
    pip3 install -e ".[dev]"

test:
    pytest tests/ -v

lint:
    ruff check src/ tests/

lint-fix:
    ruff check --fix src/ tests/

format:
    ruff format src/ tests/

typecheck:
    mypy src/

check-all: lint typecheck test

clean:
    rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

encrypt TEXT KEY="3":
    caesar-cipher encrypt "{{TEXT}}" --key {{KEY}}

decrypt TEXT KEY="3":
    caesar-cipher decrypt "{{TEXT}}" --key {{KEY}}

crack TEXT:
    caesar-cipher crack "{{TEXT}}"
