db:
	docker-compose --env-file .env -f docker/docker-compose-dev.yml --project-directory . up --build -d
	
deploy: db
	docker-compose --env-file .env.deploy -f docker/docker-compose.yml --project-directory . up --build -d

install:
	poetry install --no-root

dev: install db
	poetry run uvicorn main:app --reload
	
revision:
	poetry run alembic revision --autogenerate

up: revision
	poetry run alembic upgrade head

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

