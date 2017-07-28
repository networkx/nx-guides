FROM andrewosh/binder-base

MAINTAINER Mridul Seth <seth.mridul@gmail.com>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y libgraphviz-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y graphviz

# RUN add-apt-repository ppa:elvstone/vtk7
# RUN apt-get update
# RUN apt-get install vtk7
# RUN apt-get install -y python-vtk

USER main

ADD requirements.txt requirements.txt

# Install requirements for Python 2
RUN pip install -r requirements.txt

# Install requirements for Python 3
RUN /home/main/anaconda/envs/python3/bin/pip install -r requirements.txt
