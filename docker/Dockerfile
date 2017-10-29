# docker build -t object-recognition:latest .
# docker run -it -v $(pwd)/src:/home/src --name or object-recognition
FROM conda/miniconda3

LABEL Author="Vladimir Kuznetsov <vladimir.kazansky@gmail.com>"
LABEL Description="Object recognition web-service"
LABEL Version="1.0"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      apt-utils

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      git \
      openssh-client \
      vim \
      && \
      apt-get autoclean && \
      rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

# for conda and python
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgl1-mesa-glx \
      && \
      apt-get autoclean && \
      rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

RUN conda update -y conda
RUN conda create -y -n py36 python=3.6

RUN echo "source activate py36" >> ~/.bashrc
RUN bash -c "source activate py36 && conda install -y tensorflow jupyter notebook"
RUN bash -c "source activate py36 && conda install -y matplotlib notebook"
RUN bash -c "source activate py36 && conda install -y pillow lxml"
#  google repo
RUN cd /home && git clone https://github.com/tensorflow/models.git
RUN bash -c "source activate py36 && cd /home/models/research && protoc object_detection/protos/*.proto --python_out=."
RUN echo "export PYTHONPATH=/home/models/research:/home/models/research/slim" >> ~/.bashrc

# TODO: remove it after adding compilation
# RUN echo "export TF_CPP_MIN_LOG_LEVEL=2" >> ~/.bashrc
ENV TF_CPP_MIN_LOG_LEVEL 2

ADD ./object-recognition-start /usr/bin/
RUN chmod +x /usr/bin/object-recognition-start

ENTRYPOINT ["/usr/bin/object-recognition-start"]

# https://www.tensorflow.org/install/install_sources
# https://docs.bazel.build/versions/master/install-ubuntu.html
# bazel build --config opt --copt=-msse4.1 --copt=-msse4.2 --copt=-mavx --copt=-mavx2 --copt=-mfma //tensorflow/tools/pip_package:build_pip_package
# https://github.com/tensorflow/serving/blob/master/tensorflow_serving/tools/docker/Dockerfile.devel