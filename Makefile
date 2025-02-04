.PHONY: help install test test-e2e test-all lint format run docker-build docker-up docker-down clean pre-commit

help:
	@echo "Available commands:"
	@echo "  make test         Run unit tests"
	@echo "  make test-e2e     Run end-to-end tests"
	@echo "  make test-all     Run all tests (unit + e2e)"
	@echo "  make lint         Run linting"
	@echo "  make format       Format code"
	@echo "  make pre-commit   Run pre-commit checks"
	@echo "  make run          Run development server"
	@echo "  make docker-build Build Docker images"
	@echo "  make docker-up    Start Docker containers"
	@echo "  make docker-down  Stop Docker containers"
	@echo "  make clean        Clean up cache files"

test:
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && python -m pytest tests/test_api.py -v --cov=app --cov-report=term-missing"

test-e2e:
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && python -m pytest tests/test_e2e.py -v -s"

test-all:
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && python -m pytest tests/ -v --cov=app --cov-report=term-missing"

lint:
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && flake8 app/ tests/"
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && mypy app/ tests/"

format:
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && black --line-length 79 app/ tests/"
	docker compose run --rm api sh -c "pip install -r requirements-dev.txt && isort app/ tests/"

run:
	docker compose up

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

pre-commit:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name ".DS_Store" -delete
