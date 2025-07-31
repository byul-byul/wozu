# Makefile for WOZU FastAPI project

# ─────────────────────────────────────────────────────────────
# 🚀 Basic docker-compose commands
# ─────────────────────────────────────────────────────────────

up:
	docker-compose up

build:
	docker-compose build

detach:
	docker-compose up -d

bup:
	docker-compose up --build

down:
	docker-compose down

# ─────────────────────────────────────────────────────────────
# 🧹 Cleaning commands
# ─────────────────────────────────────────────────────────────

clean: down
	bash -c "shopt -s globstar && sudo rm -rf fastapi/**/__pycache__ fastapi/**/*.pyc"

fclean: clean
	docker volume prune -f

# ─────────────────────────────────────────────────────────────
# 🔍 Debugging and shell access
# ─────────────────────────────────────────────────────────────

logs:
	docker-compose logs -f fastapi

shell:
	docker-compose exec fastapi bash

psql:
	docker-compose exec db psql -U postgres

# ─────────────────────────────────────────────────────────────
# 🧱 Alembic (DB Migrations)
# ─────────────────────────────────────────────────────────────

migrate:
	docker-compose exec fastapi alembic upgrade head

revision:
	docker-compose exec fastapi alembic revision --autogenerate -m "$(msg)"

downgrade:
	docker-compose exec fastapi alembic downgrade -1

reset-db:
	@echo "⚠ WARNING: This will delete DB volumes. Press CTRL+C to abort..."
	sleep 30
	docker-compose down -v
	docker-compose up --build

# ─────────────────────────────────────────────────────────────
# 🌐 Ngrok & dynamic email base url updates
# ─────────────────────────────────────────────────────────────

ngrok:
	bash scripts/start_ngrok.sh

runng:
	make ngrok
	make run

buildng:
	make ngrok
	make build