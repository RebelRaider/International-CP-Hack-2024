up:
	poetry run uvicorn app:app --reload --port 8000

.PHONY: migrate-rev
migrate-rev:
	@read -p "Enter the name of the revision: " name; \
	poetry run alembic revision --autogenerate -m $$name

.PHONY: migrate-up
migrate-up:
	@read -p "Enter the revision to upgrade to: " rev; \
	poetry run alembic upgrade $$rev

.PHONY: local
local:
	docker compose -f docker-compose.local.yml up

.PHONY: test
test:
	poetry run pytest
