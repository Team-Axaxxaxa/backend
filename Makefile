start-db:
	docker compose up -d postgres

migrate:
	docker compose up --build migrator

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
