FROM continuumio/miniconda3

WORKDIR usr/src/app

# Copy everything into the container, into WORKDIR
COPY . .

# Install make and gcc
RUN apt-get update &&  \
    apt-get install -y make && \
    apt-get install -y gcc

# Create conda env and install dependencies
RUN conda env create -f environment.yml

# Build cutils.c
RUN make cutils
