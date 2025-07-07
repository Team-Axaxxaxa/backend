start-db:
	docker compose up postgres

migrate:
	alembic upgrade head

start-app:
	docker compose up script

stop:
	docker compose down
