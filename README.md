#  Object Detection Service

```sh
# to run inside "." folder
docker build -t vladimirkazan/ml-object-detection:latest docker/.
# 8888 jupyter, 5000 flask
docker run -it -v $(pwd):/home/src -p 80:80 -p 4200:4200 -p 8888:8888 -p 5000:5000 --name or vladimirkazan/ml-object-detection:latest

# inside docker
jupyter notebook --ip=* --allow-root --no-browser --port=8888 --notebook-dir=/home/

# test 
cd /home/models/research 
python object_detection/builders/model_builder_test.py
```
