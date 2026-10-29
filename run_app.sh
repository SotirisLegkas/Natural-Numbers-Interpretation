#!/usr/bin/env bash

set -e

IMAGE_NAME="phone-number-app"

echo "Starting phone number application..."
docker run -it --rm "$IMAGE_NAME"