.PHONY: smoke up down
smoke:
	docker compose --profile deps up -d
	curl -fsS http://localhost:7701/health
	docker compose --profile hub up -d --build
	curl -fsS http://localhost:8000/health

up:
	docker compose --profile deps --profile hub up -d

down:
	docker compose down -v
