# Check for typos in texts across the codebase
check-spelling:
	codespell

# Run Vale linter over the docs
vale:
	vale sync
	vale docs/

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

# Run docs checks: spelling and linting, this can be ran against a single Python version
docs-checks:
	make check-spelling
	make vale

# Run Python checks, in CI this should be ran against all supported Python versions
python-checks:
	pre-commit run --all-files
	make type-checking
	make unit-tests

# Run all code quality checks: static and dynamic tests
all-checks:
	make python-checks
	make docs-checks

# Serve documentation website locally
serve-docs:
	mkdocs serve

# Count lines of code in the project and get output in the command line
count-lines:
	uv run lines_counter.py
