```
docker build -t resource-api .
docker run -name resouce-api-instance -p 5000:5000 -i -t --rm -v $(pwd)/api:/srv/app/api resource-api
```
