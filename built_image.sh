#!/usr/bin/env bash

set -e

IMAGE_NAME="phone-number-app"

echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "Build completed successfully."