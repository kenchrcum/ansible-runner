#!/bin/bash

# Build script for ansible-runner Docker images
# Builds images with different Ansible versions
# Use --push to push images after building

PUSH=false
if [ "$1" = "--push" ]; then
    PUSH=true
fi

IMAGE_NAME="kenchrcum/ansible-runner"
#ANSIBLE_VERSIONS=("12")
ANSIBLE_VERSIONS=("2.9" "2.10" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "latest")

for version in "${ANSIBLE_VERSIONS[@]}"; do
    echo "Building image for Ansible version: $version"

    if [ "$version" = "latest" ]; then
        TAG="$IMAGE_NAME:latest"
    else
        TAG="$IMAGE_NAME:$version"
    fi

    docker build --build-arg ANSIBLE_VERSION=$version -t $TAG .

    if [ $? -eq 0 ]; then
        echo "Successfully built $TAG"
        if [ "$PUSH" = true ]; then
            echo "Pushing $TAG"
            docker push $TAG
            if [ $? -ne 0 ]; then
                echo "Failed to push $TAG"
                exit 1
            fi
        fi
    else
        echo "Failed to build $TAG"
        exit 1
    fi
done

echo "All images processed successfully!"
