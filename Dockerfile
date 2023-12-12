FROM continuumio/miniconda3

WORKDIR usr/src/app

# Copy everything into the container, into WORKDIR
COPY . .

# Install make
RUN apt-get update && apt-get install -y make

# Create conda env and install dependencies
RUN conda env create -f environment.yml
