.PHONY: up down init logs shell add-connection trigger clean

AIRFLOW_UID ?= $(shell id -u)
export AIRFLOW_UID

up:
	docker compose up -d

down:
	docker compose down

init:
	docker compose up airflow-init

logs:
	docker compose logs -f

logs-scheduler:
	docker compose logs -f airflow-scheduler

shell:
	docker compose exec airflow-webserver bash

add-connection:
	docker compose exec airflow-webserver airflow connections add \
		postgres_default \
		--conn-type postgres \
		--conn-host postgres \
		--conn-login airflow \
		--conn-password airflow \
		--conn-port 5432 \
		--conn-schema airflow || true

trigger:
	docker compose exec airflow-webserver airflow dags trigger hw6_etl_pipeline

unpause:
	docker compose exec airflow-webserver airflow dags unpause hw6_etl_pipeline

status:
	docker compose exec airflow-webserver airflow dags list-runs -d hw6_etl_pipeline

clean:
	docker compose down -v
	rm -rf output/*.csv

