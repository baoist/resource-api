# Project Setup

```
docker-machine create -d virtualbox dev
eval "$(docker-machine env dev)"
```

```
docker-compose up
psql -h $(docker-machine ip dev) -U postgres -c "CREATE DATABASE \"resource-api\";"
docker-compose run web alembic upgrade head
```
