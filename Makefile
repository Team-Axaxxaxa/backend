start-db:
	docker compose up -d postgres

migrate:
	alembic upgrade head

start-app:
	docker compose up --build -d script

stop:
	docker compose down

restart-app:
	docker compose down script
	docker compose rm -f script
	docker compose up --build -d script

logs:
	docker compose logs
