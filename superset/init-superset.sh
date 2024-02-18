#!/bin/bash

docker compose exec -it superset superset fab create-admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --username admin \
  --password admin

docker compose exec -it superset superset db upgrade

docker compose exec -it superset superset init