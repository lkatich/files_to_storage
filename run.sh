#!/usr/bin/env bash

mkdir files
mkdir storage

docker build -f docker/Dockerfile -t fts .
docker run -v $PWD/files:/home/app/files -v $PWD/storage:/home/app/storage fts
