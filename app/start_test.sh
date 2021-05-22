#! /bin/bash
set -e

# docker stop test-db
# docker stop test-redis
# docker rm test-db
# docker rm test-redis

# docker run --name=test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 -d postgres:10
# docker run --name test-redis -d -p 6378:6379 redis

docker start test-db
docker start test-redis