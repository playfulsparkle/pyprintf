.PHONY: test lint format install uninstall coverage help

# Default target when just running 'make'
help:
	@echo "Available commands:"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with Black (if installed)"
	@echo "  make coverage     - Generate test coverage report"
	@echo "  make install      - Install the package"
	@echo "  make uninstall    - Uninstall the package"
	@echo "  make check        - Run both lint and test"

test:
	pytest tests/

lint:
	flake8 src/ tests/

format:
	black src/ tests/ || echo "Black not installed. Run 'pip install black' to enable formatting."

coverage:
	pytest --cov=pyprintf tests/ --cov-report=term --cov-report=html
	@echo "HTML coverage report generated in htmlcov/"

install:
	pip install .

uninstall:
	pip uninstall -y pyprintf

check: lint test