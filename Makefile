start-db:
	docker compose up -d postgres

migrate:
	alembic upgrade head

start-app:
	docker compose up --build -d script

stop:
	docker compose down
