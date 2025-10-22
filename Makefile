.PHONY: format lint check test all clean help

help:
	@echo "Available commands:"
	@echo "  make format  - Format all Python files with Black"
	@echo "  make lint    - Run flake8 linter"
	@echo "  make check   - Check formatting without making changes"
	@echo "  make test    - Run pytest"
	@echo "  make all     - Format and lint code"
	@echo "  make clean   - Remove Python cache files"

format:
	@echo "Formatting code with Black..."
	black src/

lint:
	@echo "Running flake8 linter..."
	flake8 src/ --max-line-length=88

check:
	@echo "Checking code formatting..."
	black --check src/

test:
	@echo "Running tests..."
	pytest

all: format lint
	@echo "✓ Code formatted and linted successfully!"

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

