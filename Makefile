.PHONY: up down build restart logs pull update

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

restart:
	docker compose restart

logs:
	docker compose logs -f

pull:
	git pull

update:
	git pull && docker compose up -d --build
