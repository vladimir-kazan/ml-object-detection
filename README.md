#  Object Recognition Service

```sh
# to run inside "." folder
docker build -t object-recognition:latest docker/.
docker run -it -v $(pwd)/src:/home/src -p 8888:8888 --name or object-recognition

# inside docker
jupyter notebook --ip=* --allow-root --no-browser --port 8888
```
