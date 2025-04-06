.PHONY: run-db down-db


run-db:
	docker-compose up

down-db:
	docker-compose down
