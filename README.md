

# Install dependencies
pip install poetry
poetry install

# Run Tests
poetry run pytest

# Run CLI
poetry run python3 src/portfolio_manager/cli.py