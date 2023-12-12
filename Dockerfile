FROM continuumio/miniconda3

WORKDIR usr/src/app

# Copy everything into the container, into WORKDIR
COPY . .

# Install dependencies
RUN conda env create -f environment.yml
