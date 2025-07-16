# Makefile for WOZU FastAPI project

# ─────────────────────────────────────────────────────────────
# 🚀 Basic docker-compose commands
# ─────────────────────────────────────────────────────────────

run:
	docker-compose up

build:
	docker-compose up --build

detach:
	docker-compose up -d

bdetach:
	docker-compose up -d --build

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
# 🔄 DB & Alembic
# ─────────────────────────────────────────────────────────────

migrate:
	docker-compose exec fastapi alembic upgrade head

reset-db:
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