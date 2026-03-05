.PHONY: setup up down logs smoke

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "[setup] .env wurde aus .env.example erstellt. Bitte AWS Credentials eintragen."; \
	else \
		echo "[setup] .env existiert bereits."; \
	fi

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

smoke:
	@curl -fsS http://localhost:8000/health >/dev/null && echo "[smoke] API erreichbar auf :8000"
	@curl -fsS http://localhost:3000 >/dev/null && echo "[smoke] Frontend erreichbar auf :3000"
