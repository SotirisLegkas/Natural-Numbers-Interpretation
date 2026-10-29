#!/usr/bin/env bash

set -e

IMAGE_NAME="phone-number-app"

echo "Running tests..."
docker run --rm "$IMAGE_NAME" pytest -v