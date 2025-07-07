start-db:
	docker compose up postgres

migrate:
	alembic upgrade head