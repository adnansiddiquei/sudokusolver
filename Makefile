IMAGE_NAME=sudokusolver
CONTAINER_NAME=sudokusolver_container

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run docker container with sudokusolver/inputs and sudokusolver/outputs mounted as volumes
run: build
	docker run -it --name $(CONTAINER_NAME) \
	-v "$(PWD)/sudokusolver/inputs":/usr/src/app/sudokusolver/inputs \
	-v "$(PWD)/sudokusolver/outputs":/usr/src/app/sudokusolver/outputs \
	-v "$(PWD)/docs/build":/usr/src/app/docs/build \
	$(IMAGE_NAME) /bin/bash

# Stop and remove the container
clean:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Remove the Docker image
clean-image:
	docker rmi $(IMAGE_NAME)
