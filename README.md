# Project Setup
# _____________

```
docker-compose build
docker-compose run postgres createdb resource-api
docker-compose run web alembic upgrade head
```
