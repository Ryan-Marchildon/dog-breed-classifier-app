# Build an image that can do training and inference in SageMaker
# This is a Python 2 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM ubuntu:16.04

MAINTAINER Ryan Marchildon <ryan.marchildon@utoronto.ca>

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# *** Install all of the python packages ***
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy==1.14.5 scipy scikit-learn pandas flask gevent gunicorn
RUN pip install tensorflow
RUN pip install keras

# link scipy/numpy libraries to remove overlap and save space
RUN (cd /usr/local/lib/python2.7/dist-packages/scipy/.libs; rm *; ln ../../numpy/.libs/* .)

# remove the pip install caches to save space
RUN rm -rf /root/.cache


# *** Set Environment Variables ***
# Notes: PYTHONUNBUFFERED keeps Python from buffering our standard output stream, 
# which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"


# *** Set up the program in the image ***
COPY dog_breed_nn /opt/program
WORKDIR /opt/program

