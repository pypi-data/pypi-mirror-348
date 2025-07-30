# Variables
PACKAGE_NAME := zendata
PYPI_REPOSITORY := pypi  # Change to testpypi if publishing to the test index

# Targets
.PHONY: help install test build publish clean

help:
	@echo "Available targets:"
	@echo "  install   : Install project dependencies"
	@echo "  test      : Run unit tests with pytest"
	@echo "  build     : Build the package using uv"
	@echo "  publish   : Publish the package to $(PYPI_REPOSITORY)"
	@echo "  clean     : Remove build artifacts"

install:
	@echo "🔧 Installing dependencies..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync --group test

test: install
	@echo "🧪 Running tests..."
	uv run pytest --cov=src --cov-report=term-missing tests/

build:
	@echo "📦 Building the package..."
	uv build

publish:
	@echo "🚀 Publishing to $(PYPI_REPOSITORY)..."
	uv publish --index $(PYPI_REPOSITORY) --token $$PYPI_TOKEN

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build dist *.egg-info
