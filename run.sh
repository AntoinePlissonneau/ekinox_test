#!/bin/bash

docker build -f Dockerfile -t ekinox_test .
docker run  -p 8501:8501 --rm ekinox_test
