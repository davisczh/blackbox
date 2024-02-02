#!/bin/bash

# Step 1: Build the Docker image (if necessary)
docker build -t blackboxtransfer -f Dockerfile .

docker run -it --rm \
    --network host \
    --privileged \
    -v "$(pwd)/blackboxes:/app/blackboxes" \
    blackboxtransfer
