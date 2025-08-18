install:  ## Install project dependencies
	@uv pip install -r requirements.txt

install-prod:  ## Install only production dependencies
	@uv pip install -r requirements/prod.txt

install-dev:  ## Install development dependencies (includes production)
	@uv pip install -r requirements/dev.txt

lint:  ## Run isort, black and flake8 on app/ directory
	@echo "🔧 Sorting imports with isort..."
	@isort app/
	@echo "🧹 Removing trailing whitespace..."
	@find app/ -type f -name "*.py" -exec sed -i 's/[ \t]*$$//' {} +
	@echo "🎨 Formatting code with black..."
	@black app/
	@echo "🔍 Checking code quality with flake8..."
	@flake8 app/
	@echo "✅ Linting completed!"

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install install-prod install-dev lint help
