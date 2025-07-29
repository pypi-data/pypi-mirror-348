# Check for typos in texts across the codebase
check-spelling:
	codespell

# Run a linter and a code formatter
lint:
	ruff check --fix
	ruff format

# Run a static type checker
type-checking:
	mypy .

# Run all unit tests
unit-tests:
	pytest .

# Run all code quality checks: static and dynamic tests
all-checks:
	make check-spelling
	pre-commit run --all-files
	make type-checking
	make unit-tests

# Serve documentation website locally
serve-docs:
	mkdocs serve

# Count lines of code in the project and get output in the command line
count-lines:
	uv run lines_counter.py
