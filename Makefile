up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200 api

test:
	docker compose exec api pytest -q

test-unit:
	docker compose exec api pytest -q app/tests/unit

test-int:
	docker compose exec api pytest -q app/tests/integration
